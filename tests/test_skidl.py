import shutil

import pytest

from codetocad import Circuit, capacitor, led, resistor, voltage_source

pytest.importorskip("skidl")

from codetocad_integrations.skidl import (  # noqa: E402
    export_netlist,
    to_netlistsvg_json,
    to_skidl,
)


def _rc_lowpass():
    circuit = Circuit("rc_lowpass")
    v1 = circuit.add(voltage_source(dc=5))
    r1 = circuit.add(resistor("1.6k"))
    c1 = circuit.add(capacitor("100n"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], c1[1], name="VOUT")
    circuit.connect(c1[2], v1["-"], circuit.gnd)
    return circuit


def test_to_skidl_builds_parts_and_nets():
    circuit = _rc_lowpass()
    sk = to_skidl(circuit)
    refs = {part.ref for part in sk.parts}
    assert {"V1", "R1", "C1"} <= refs
    net_names = {net.name for net in sk.nets}
    assert {"VIN", "VOUT"} <= net_names


def test_export_netlist_has_refs_values_and_footprints(tmp_path):
    circuit = _rc_lowpass()
    path = tmp_path / "rc.net"
    text = export_netlist(circuit, str(path))
    assert path.exists()
    assert "R1" in text and "C1" in text
    assert "1.6k" in text or "1K6" in text.upper()
    assert "Resistor_THT" in text  # footprint made it into the netlist


def test_netlistsvg_json_maps_symbols_and_labels():
    circuit = _rc_lowpass()
    module = to_netlistsvg_json(circuit)["modules"]["rc_lowpass"]
    cells = module["cells"]
    # Symbols come from the analog skin, labels ride in attributes (so the
    # "1.6k" period can't corrupt the yosys-style cell name).
    assert cells["R1"]["type"] == "r_h"
    assert cells["R1"]["attributes"] == {"ref": "R1", "value": "1.6k"}
    assert cells["V1"]["type"] == "v"
    assert any(c["type"] == "gnd" for c in cells.values())
    # Every cell key is period-free.
    assert all("." not in key for key in cells)


def test_led_uses_led_symbol():
    circuit = Circuit("led")
    v1 = circuit.add(voltage_source(dc=5))
    r1 = circuit.add(resistor(150))
    d1 = circuit.add(led())
    circuit.connect(v1["+"], r1[1], name="VCC")
    circuit.connect(r1[2], d1["A"], name="VLED")
    circuit.connect(d1["K"], v1["-"], circuit.gnd)
    cells = to_netlistsvg_json(circuit)["modules"]["led"]["cells"]
    assert cells["D1"]["type"].startswith("d_led")


@pytest.mark.skipif(shutil.which("netlistsvg") is None, reason="netlistsvg not installed")
def test_export_schematic_writes_svg(tmp_path):
    from codetocad_integrations.skidl import export_schematic

    path = tmp_path / "rc.svg"
    export_schematic(_rc_lowpass(), str(path))
    assert path.exists()
    content = path.read_text()
    assert content.lstrip().startswith("<svg") or "<svg" in content[:200]
