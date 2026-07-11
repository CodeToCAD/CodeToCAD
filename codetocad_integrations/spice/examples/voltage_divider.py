"""SPICE simulation of a 9V -> 6V resistive voltage divider.

Solves the DC operating point (VOUT = 9 * 20k/30k = 6V), sweeps the supply
from 0 to 9V, and plots the transfer curve to voltage_divider_sweep.png.

Requires the spice extra and ngspice (see the examples README).
Run:  python voltage_divider.py
"""

from codetocad import Circuit, resistor, voltage_source
from codetocad_integrations.spice import simulate


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
    sim = simulate(circuit)
    print("netlist:\n" + sim.netlist())

    op = sim.operating_point()
    print("operating point:")
    print(op)
    assert abs(op.voltage("VOUT") - 6.0) < 1e-9

    v1 = circuit.get_component("V1")
    sweep = sim.dc_sweep(v1, 0, 9, 0.1)
    sweep.plot(
        "voltage_divider_sweep.png",
        x="v-sweep",
        y=["VIN", "VOUT"],
        title="Voltage divider transfer (VOUT = 2/3 VIN)",
        xlabel="supply voltage [V]",
        ylabel="node voltage [V]",
    )
    print("wrote voltage_divider_sweep.png")


if __name__ == "__main__":
    main()
