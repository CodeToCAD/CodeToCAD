"""A 9V -> 6V resistive voltage divider captured as a CodeToCAD Circuit.

Exports the KiCad netlist (voltage_divider.net), the BOM XML
(voltage_divider.xml) and a schematic SVG (voltage_divider.svg), and runs
skidl's electrical rules check.

Requires the skidl extra and netlistsvg (see the examples README).
Run:  python voltage_divider.py
"""

from codetocad import Circuit, resistor, voltage_source
from codetocad_integrations.skidl import (
    erc,
    export_netlist,
    export_schematic,
    export_xml,
)


def build_circuit() -> Circuit:
    circuit = Circuit("voltage_divider")
    v1 = circuit.add(voltage_source(dc=9))
    r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], r2[1], name="VOUT")
    circuit.connect(r2[2], v1["-"], circuit.gnd)
    return circuit


def main() -> None:
    circuit = build_circuit()
    assert circuit.validate() == []
    erc(circuit)
    export_netlist(circuit, "voltage_divider.net")
    export_xml(circuit, "voltage_divider.xml")
    export_schematic(circuit, "voltage_divider.svg")
    print("wrote voltage_divider.net, voltage_divider.xml, voltage_divider.svg")


if __name__ == "__main__":
    main()
