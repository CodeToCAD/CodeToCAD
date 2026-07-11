"""SPICE simulation of an RC low-pass filter (fc = 1/2piRC ~ 1 kHz).

Runs an AC sweep from 10 Hz to 1 MHz and renders the Bode plot
(rc_lowpass_bode.png), checking the -3dB corner lands at the analytic
cutoff, then drives the filter with a 100 Hz square wave and plots the
time-domain RC charge/discharge response (rc_lowpass_step.png).

Requires the spice extra and ngspice (see the examples README).
Run:  python rc_lowpass.py
"""

import math

import numpy as np

from codetocad import Circuit, capacitor, resistor, voltage_source
from codetocad_integrations.spice import simulate

RESISTANCE = 1600.0  # ohms
CAPACITANCE = 100e-9  # farads


def build_circuit() -> Circuit:
    circuit = Circuit("rc_lowpass")
    v1 = circuit.add(voltage_source(ac=1, waveform="PULSE(0 1 0 1u 1u 5m 10m)"))
    r1 = circuit.add(resistor(RESISTANCE))
    c1 = circuit.add(capacitor(CAPACITANCE))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], c1[1], name="VOUT")
    circuit.connect(c1[2], v1["-"], circuit.gnd)
    return circuit


def main() -> None:
    circuit = build_circuit()
    sim = simulate(circuit)

    cutoff = 1 / (2 * math.pi * RESISTANCE * CAPACITANCE)
    ac = sim.ac(10, "1meg", points_per_decade=30)
    gain_db = ac.magnitude_db("VOUT")
    measured = ac.frequency[np.argmin(np.abs(gain_db + 3.0))]
    print(f"corner frequency: {measured:.0f} Hz (analytic {cutoff:.0f} Hz)")
    ac.bode(
        "rc_lowpass_bode.png",
        "VOUT",
        title=f"RC low-pass Bode plot (fc ~ {cutoff:.0f} Hz)",
    )

    tran = sim.transient("20u", "20m")
    tran.plot(
        "rc_lowpass_step.png",
        x="time",
        y=["VIN", "VOUT"],
        title="RC low-pass response to a 100 Hz square wave",
        xlabel="time [s]",
        ylabel="voltage [V]",
    )
    print("wrote rc_lowpass_bode.png and rc_lowpass_step.png")


if __name__ == "__main__":
    main()
