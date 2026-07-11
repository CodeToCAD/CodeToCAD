"""SPICE simulation of an LED driven from 5V through a 150 ohm resistor.

The LED's SPICE diode model is derived from the component's
forward_voltage (2V at 10 mA). The operating point lands near
(5V - 2V) / 150 ohm = 20 mA; sweeping the supply from 0 to 5V plots the
LED current and the diode turn-on knee (led_driver_current.png).

Requires the spice extra and ngspice (see the examples README).
Run:  python led_driver.py
"""

from codetocad import Circuit, led, resistor, voltage_source
from codetocad_integrations.spice import simulate


def build_circuit() -> Circuit:
    circuit = Circuit("led_driver")
    battery = circuit.add(voltage_source(dc=5))
    r1 = circuit.add(resistor(150))
    d1 = circuit.add(led())  # forward_voltage=2.0, current_limit=20mA
    circuit.connect(battery["+"], r1[1], name="VCC")
    circuit.connect(r1[2], d1["A"], name="VLED")
    circuit.connect(d1["K"], battery["-"], circuit.gnd)
    return circuit


def main() -> None:
    circuit = build_circuit()
    sim = simulate(circuit)
    print("netlist:\n" + sim.netlist())

    op = sim.operating_point()
    battery, d1 = circuit.get_component("V1"), circuit.get_component("D1")
    current = -op.current(battery)  # into V1's + terminal, so negate
    print(f"LED current: {current * 1000:.1f} mA (target ~20 mA)")
    print(f"LED forward drop: {op.voltage('VLED'):.2f} V")
    if current > (d1.current_limit or 0):
        print("warning: LED current exceeds its rated limit!")

    sweep = sim.dc_sweep(battery, 0, 5, 0.05)
    led_current_ma = -1000 * sweep.current(battery)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(figsize=(8, 4.5))
    axes.plot(sweep.sweep, led_current_ma)
    axes.axhline(1000 * d1.current_limit, color="tab:red", linestyle="--", label="LED current limit")
    axes.set_xlabel("supply voltage [V]")
    axes.set_ylabel("LED current [mA]")
    axes.set_title("LED current vs supply (turn-on knee at ~2 V)")
    axes.grid(True, alpha=0.4)
    axes.legend()
    figure.tight_layout()
    figure.savefig("led_driver_current.png", dpi=150)
    print("wrote led_driver_current.png")


if __name__ == "__main__":
    main()
