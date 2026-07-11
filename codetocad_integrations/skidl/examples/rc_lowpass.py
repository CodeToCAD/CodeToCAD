"""An RC low-pass filter (fc = 1/2piRC ~ 1 kHz) as a CodeToCAD Circuit.

Exports the KiCad netlist (rc_lowpass.net) and a schematic SVG
(rc_lowpass.svg). The same circuit is frequency- and time-domain simulated
in codetocad_integrations/spice/examples/rc_lowpass.py.

Requires the skidl extra and netlistsvg (see the examples README).
Run:  python rc_lowpass.py
"""

from codetocad import Circuit, capacitor, resistor, voltage_source
from codetocad_integrations.skidl import export_netlist, export_schematic


def build_circuit() -> Circuit:
    circuit = Circuit("rc_lowpass")
    v1 = circuit.add(voltage_source(ac=1, waveform="PULSE(0 1 0 1u 1u 2.5m 5m)"))
    r1 = circuit.add(resistor("1.6k"))
    c1 = circuit.add(capacitor("100n"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], c1[1], name="VOUT")
    circuit.connect(c1[2], v1["-"], circuit.gnd)
    return circuit


def main() -> None:
    circuit = build_circuit()
    assert circuit.validate() == []
    export_netlist(circuit, "rc_lowpass.net")
    export_schematic(circuit, "rc_lowpass.svg")
    print("wrote rc_lowpass.net and rc_lowpass.svg")


if __name__ == "__main__":
    main()
