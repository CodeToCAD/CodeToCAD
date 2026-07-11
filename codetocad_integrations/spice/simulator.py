"""The ngspice-backed SPICE simulation implementation.

Pipeline: Circuit -> SPICE netlist -> ngspice batch run (ASCII rawfile) ->
numpy result vectors. Units are SI: volts, amps, ohms, farads, henries,
seconds, hertz.
"""

from __future__ import annotations

import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from codetocad.ecad import (
    Circuit,
    ComponentType,
    ElectricalComponent,
    Net,
    format_si,
)


def find_ngspice() -> str:
    """Locate the ngspice executable."""
    override = os.environ.get("CODETOCAD_NGSPICE")
    if override:
        return override
    found = shutil.which("ngspice")
    if found:
        return found
    home_install = Path.home() / ".codetocad" / "ngspice" / "bin" / "ngspice"
    if home_install.exists():
        return str(home_install)
    raise FileNotFoundError(
        "ngspice not found. Set CODETOCAD_NGSPICE to its path, put ngspice "
        "on the PATH, or install it with e.g.\n"
        "  brew install ngspice          (macOS)\n"
        "  apt install ngspice           (Debian/Ubuntu)\n"
        "  micromamba create -p ~/.codetocad/ngspice -c conda-forge ngspice"
    )


# -- netlist generation --


def _node_names(circuit: Circuit) -> dict[int, str]:
    """SPICE node name per net: ground nets are node 0, other nets keep
    their (sanitized) name."""
    names = {}
    for net in circuit.nets:
        if net.is_ground:
            names[id(net)] = "0"
        else:
            safe = "".join(
                ch if ch.isalnum() or ch in "_+-" else "_" for ch in net.name or ""
            )
            names[id(net)] = safe or f"n{len(names)}"
    return names


def _element_name(component: ElectricalComponent) -> str:
    """SPICE element names must start with the element letter."""
    prefix = component.component_type.spice_prefix
    reference = component.reference or component.component_type.ref_prefix
    if reference.upper().startswith(prefix.upper()):
        return reference
    return f"{prefix}{reference}"


def _diode_model_card(component: ElectricalComponent, model_name: str) -> str:
    """Derive a diode ``.model`` from the component's forward voltage: the
    saturation current is chosen so the diode drops ``forward_voltage`` at
    10 mA."""
    forward_voltage = component.forward_voltage or 0.7
    emission = 2.0 if component.component_type is ComponentType.LED else 1.5
    thermal = 0.02585  # volts at room temperature
    saturation = 0.010 / math.exp(forward_voltage / (emission * thermal))
    return (
        f".model {model_name} D(IS={saturation:.3e} N={emission:g} RS=0.5)"
    )


def _source_spec(component: ElectricalComponent) -> str:
    parts = []
    if component.dc is not None:
        parts.append(f"DC {component.dc:g}")
    if component.ac is not None:
        parts.append(f"AC {component.ac:g}")
    if component.waveform is not None:
        parts.append(component.waveform)
    if not parts:
        parts.append("DC 0")
    return " ".join(parts)


def to_netlist(circuit: Circuit, analyses: list[str] | tuple[str, ...] = ()) -> str:
    """Generate a SPICE netlist for ``circuit``. ``analyses`` are extra
    dot-cards (e.g. ``[".op"]``) placed before ``.end``."""
    unconnected = circuit.unconnected_pins()
    if unconnected:
        raise ValueError(f"Circuit has unconnected pins: {unconnected}")
    nodes = _node_names(circuit)
    lines = [f"* {circuit.name}"]
    models: dict[str, str] = {}

    for component in circuit.components:
        prefix = component.component_type.spice_prefix
        if prefix is None:
            raise ValueError(
                f"{component.reference or component.name} "
                f"({component.component_type.value}) has no SPICE primitive; "
                "set spice_model or exclude it from simulation"
            )
        name = _element_name(component)
        pin_nodes = [nodes[id(pin.net)] for pin in component.pins]
        terminals = " ".join(pin_nodes)

        if prefix == "R":
            lines.append(f"{name} {terminals} {format_si(component.resistance)}")
        elif prefix == "C":
            lines.append(f"{name} {terminals} {format_si(component.capacitance)}")
        elif prefix == "L":
            lines.append(f"{name} {terminals} {format_si(component.inductance)}")
        elif prefix == "D":
            if component.spice_model and component.spice_model.lstrip().startswith("."):
                # A full .model card: reference it by its declared name.
                model_name = component.spice_model.split()[1]
                models[model_name] = component.spice_model.strip()
            elif component.spice_model:
                model_name = component.spice_model
            else:
                model_name = f"D_{name}"
                models[model_name] = _diode_model_card(component, model_name)
            lines.append(f"{name} {terminals} {model_name}")
        elif prefix in ("V", "I"):
            lines.append(f"{name} {terminals} {_source_spec(component)}")
        elif prefix == "Q":
            if not component.spice_model:
                raise ValueError(
                    f"{name}: transistors need a spice_model (.model card or name)"
                )
            if component.spice_model.lstrip().startswith("."):
                model_name = component.spice_model.split()[1]
                models[model_name] = component.spice_model.strip()
            else:
                model_name = component.spice_model
            lines.append(f"{name} {terminals} {model_name}")
        elif prefix == "X":
            if not component.spice_model:
                raise ValueError(f"{name}: ICs need a spice_model (.subckt card)")
            subckt_name = component.spice_model.split()[1]
            models[subckt_name] = component.spice_model.strip()
            lines.append(f"{name} {terminals} {subckt_name}")

    lines.extend(models[key] for key in sorted(models))
    lines.extend(analyses)
    lines.append(".end")
    return "\n".join(lines) + "\n"


# -- rawfile parsing --


def _parse_rawfile(path: Path) -> tuple[str, list[str], dict[str, np.ndarray]]:
    """Parse an ASCII ngspice rawfile into named numpy vectors."""
    lines = path.read_text().splitlines()
    plotname = ""
    is_complex = False
    variables: list[str] = []
    n_variables = n_points = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("Plotname:"):
            plotname = line.split(":", 1)[1].strip()
        elif line.startswith("Flags:"):
            is_complex = "complex" in line.lower()
        elif line.startswith("No. Variables:"):
            n_variables = int(line.split(":")[1])
        elif line.startswith("No. Points:"):
            n_points = int(line.split(":")[1])
        elif line.startswith("Variables:"):
            for offset in range(1, n_variables + 1):
                variables.append(lines[index + offset].split()[1])
            index += n_variables
        elif line.startswith("Values:"):
            index += 1
            break
        index += 1

    tokens = " ".join(lines[index:]).split()
    dtype = complex if is_complex else float
    data = np.zeros((n_points, n_variables), dtype=dtype)

    def parse(token: str):
        if is_complex:
            real, _, imaginary = token.partition(",")
            return complex(float(real), float(imaginary))
        return float(token)

    position = 0
    for point in range(n_points):
        position += 1  # skip the point index
        for variable in range(n_variables):
            data[point, variable] = parse(tokens[position])
            position += 1

    vectors = {name: data[:, i] for i, name in enumerate(variables)}
    return plotname, variables, vectors


# -- results --


class SpiceResults:
    """Named result vectors of an ngspice analysis. Index with the raw
    vector name (``results["v(vout)"]``) or just a net/source name
    (``results["VOUT"]``, ``results["V1"]``)."""

    def __init__(self, analysis: str, variables: list[str], data: dict[str, np.ndarray]):
        self.analysis = analysis
        self.variables = variables
        self.data = data

    def _lookup(self, key) -> str:
        if isinstance(key, Net):
            key = "0" if key.is_ground else key.name
        wanted = str(key).lower()
        for candidate in (wanted, f"v({wanted})", f"{wanted}#branch", f"i({wanted})"):
            if candidate in self.data:
                return candidate
        raise KeyError(f"No vector {key!r}; available: {self.variables}")

    def __getitem__(self, key) -> np.ndarray:
        return self.data[self._lookup(key)]

    def voltage(self, net: Net | str) -> np.ndarray:
        """Node voltage vector for a net (volts)."""
        return self[net]

    def current(self, source: ElectricalComponent | str) -> np.ndarray:
        """Branch current vector through a voltage source (amps, flowing
        into the ``+`` terminal per SPICE convention)."""
        reference = source.reference if isinstance(source, ElectricalComponent) else source
        return self[reference]

    def plot(
        self,
        path: str,
        x: str,
        y: list[str] | str,
        *,
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None,
        logx: bool = False,
    ) -> str:
        """Plot result vectors to an image file. Requires matplotlib."""
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        figure, axes = plt.subplots(figsize=(8, 4.5))
        x_values = np.real(self[x])
        signals = [y] if isinstance(y, str) else y
        for signal in signals:
            axes.plot(x_values, np.real(self[signal]), label=str(signal))
        if logx:
            axes.set_xscale("log")
        axes.set_xlabel(xlabel or x)
        axes.set_ylabel(ylabel or ", ".join(str(s) for s in signals))
        axes.grid(True, alpha=0.4)
        if len(signals) > 1:
            axes.legend()
        axes.set_title(title or f"{self.analysis}")
        figure.tight_layout()
        figure.savefig(path, dpi=150)
        plt.close(figure)
        return path


class OperatingPointResults(SpiceResults):
    """DC operating point: every vector has a single value."""

    def voltage(self, net: Net | str) -> float:
        return float(np.real(self[net][0]))

    def current(self, source: ElectricalComponent | str) -> float:
        reference = source.reference if isinstance(source, ElectricalComponent) else source
        return float(np.real(self[reference][0]))

    def __str__(self):
        rows = []
        for name in self.variables:
            value = float(np.real(self.data[name][0]))
            unit = "A" if name.endswith("#branch") or name.startswith("i(") else "V"
            rows.append(f"{name:>20} = {format_si(value)}{unit}")
        return "\n".join(rows)


class DCSweepResults(SpiceResults):
    @property
    def sweep(self) -> np.ndarray:
        """The swept source values (first result vector)."""
        return np.real(self.data[self.variables[0]])


class TransientResults(SpiceResults):
    @property
    def time(self) -> np.ndarray:
        """Time points in seconds."""
        return np.real(self.data["time"])


class ACAnalysisResults(SpiceResults):
    """AC small-signal sweep; vectors are complex."""

    @property
    def frequency(self) -> np.ndarray:
        """Frequency points in hertz."""
        return np.real(self.data["frequency"])

    def magnitude_db(self, signal) -> np.ndarray:
        return 20 * np.log10(np.abs(self[signal]))

    def phase_deg(self, signal) -> np.ndarray:
        return np.degrees(np.angle(self[signal]))

    def bode(self, path: str, signal, *, title: str | None = None) -> str:
        """Plot magnitude (dB) and phase (degrees) of ``signal`` over
        frequency to an image file. Requires matplotlib."""
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        figure, (mag_axes, phase_axes) = plt.subplots(
            2, 1, sharex=True, figsize=(8, 6)
        )
        mag_axes.semilogx(self.frequency, self.magnitude_db(signal))
        mag_axes.set_ylabel("magnitude [dB]")
        mag_axes.grid(True, which="both", alpha=0.4)
        mag_axes.set_title(title or f"Bode plot of {signal}")
        phase_axes.semilogx(self.frequency, self.phase_deg(signal))
        phase_axes.set_ylabel("phase [deg]")
        phase_axes.set_xlabel("frequency [Hz]")
        phase_axes.grid(True, which="both", alpha=0.4)
        figure.tight_layout()
        figure.savefig(path, dpi=150)
        plt.close(figure)
        return path


# -- simulation --


def _spice_number(value: float | str) -> str:
    """Analysis parameters accept floats (SI units) or SPICE strings
    such as ``"10u"``."""
    return value if isinstance(value, str) else f"{value:g}"


class SpiceSimulation:
    """Runs ngspice analyses of a Circuit. Create one with ``simulate()``."""

    def __init__(
        self,
        circuit: Circuit,
        *,
        ngspice_path: str | None = None,
        output_dir: str | Path | None = None,
    ):
        self.circuit = circuit
        self.ngspice_path = ngspice_path
        self.output_dir = Path(
            output_dir
            if output_dir is not None
            else tempfile.mkdtemp(prefix="codetocad_spice_")
        ).resolve()

    def netlist(self) -> str:
        """The circuit's SPICE netlist (without analysis cards)."""
        return to_netlist(self.circuit)

    def _run(self, analysis: str, results_class):
        ngspice = self.ngspice_path or find_ngspice()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        raw_path = self.output_dir / "results.raw"
        raw_path.unlink(missing_ok=True)
        control = "\n".join(
            [
                ".control",
                "set filetype=ascii",
                analysis,
                f"write {raw_path}",
                ".endc",
            ]
        )
        netlist_path = self.output_dir / f"{self.circuit.name or 'circuit'}.cir"
        netlist_path.write_text(to_netlist(self.circuit, analyses=[control]))
        log_path = self.output_dir / "ngspice.log"
        result = subprocess.run(
            [ngspice, "-b", "-o", str(log_path), str(netlist_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not raw_path.exists():
            log = log_path.read_text() if log_path.exists() else result.stderr
            raise RuntimeError(
                f"ngspice failed for {analysis!r} (exit {result.returncode}):\n"
                + "\n".join(log.splitlines()[-15:])
            )
        _, variables, vectors = _parse_rawfile(raw_path)
        return results_class(analysis, variables, vectors)

    def operating_point(self) -> OperatingPointResults:
        """DC operating point (``op``): node voltages and source currents."""
        return self._run("op", OperatingPointResults)

    def dc_sweep(
        self,
        source: ElectricalComponent | str,
        start: float | str,
        stop: float | str,
        step: float | str,
    ) -> DCSweepResults:
        """Sweep a source's DC value (``dc``)."""
        reference = source.reference if isinstance(source, ElectricalComponent) else source
        card = (
            f"dc {reference} {_spice_number(start)} "
            f"{_spice_number(stop)} {_spice_number(step)}"
        )
        return self._run(card, DCSweepResults)

    def transient(
        self,
        step: float | str,
        stop: float | str,
        start: float | str = 0.0,
    ) -> TransientResults:
        """Time-domain analysis (``tran``); times in seconds or SPICE
        strings such as ``"10u"``."""
        card = (
            f"tran {_spice_number(step)} {_spice_number(stop)} "
            f"{_spice_number(start)}"
        )
        return self._run(card, TransientResults)

    def ac(
        self,
        start_frequency: float | str,
        stop_frequency: float | str,
        points_per_decade: int = 20,
    ) -> ACAnalysisResults:
        """AC small-signal sweep (``ac dec``); sources need ``ac=`` set."""
        card = (
            f"ac dec {points_per_decade} {_spice_number(start_frequency)} "
            f"{_spice_number(stop_frequency)}"
        )
        return self._run(card, ACAnalysisResults)


def simulate(
    circuit: Circuit,
    *,
    ngspice_path: str | None = None,
    output_dir: str | Path | None = None,
) -> SpiceSimulation:
    """Create an ngspice simulation of ``circuit``; run analyses with
    ``operating_point()``, ``dc_sweep()``, ``transient()`` and ``ac()``."""
    return SpiceSimulation(circuit, ngspice_path=ngspice_path, output_dir=output_dir)
