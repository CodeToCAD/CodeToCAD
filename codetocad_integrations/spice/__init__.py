"""SPICE integration: circuit simulation of CodeToCAD Circuits with ngspice.

``simulate(circuit)`` builds a SPICE netlist from a ``codetocad.Circuit``
(resistors, capacitors, inductors, diodes/LEDs and sources map to SPICE
primitives; diode models are derived from each component's electrical
properties) and runs it with the `ngspice <https://ngspice.sourceforge.io>`_
simulator in batch mode::

    from codetocad import Circuit, resistor, voltage_source
    from codetocad_integrations.spice import simulate

    circuit = Circuit("divider")
    v1 = circuit.add(voltage_source(dc=9))
    r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], r2[1], name="VOUT")
    circuit.connect(r2[2], v1["-"], circuit.gnd)

    sim = simulate(circuit)
    op = sim.operating_point()
    print(op.voltage("VOUT"))                      # 6.0
    ac = sim.ac("1", "1meg")                       # frequency sweep
    tran = sim.transient("10u", "5m")              # time-domain
    sweep = sim.dc_sweep(v1, 0, 9, 0.1)            # source sweep

Results are numpy arrays with ``plot()``/``bode()`` helpers (matplotlib).
The ngspice executable is auto-discovered from ``CODETOCAD_NGSPICE``, the
PATH, or ``~/.codetocad/ngspice/bin/ngspice`` — install it with e.g.
``brew install ngspice`` (macOS) or ``apt install ngspice`` (Debian/Ubuntu).
"""

from codetocad_integrations.spice.simulator import (
    ACAnalysisResults,
    DCSweepResults,
    OperatingPointResults,
    SpiceResults,
    SpiceSimulation,
    TransientResults,
    find_ngspice,
    simulate,
    to_netlist,
)

__all__ = [
    "simulate",
    "SpiceSimulation",
    "to_netlist",
    "find_ngspice",
    "SpiceResults",
    "OperatingPointResults",
    "DCSweepResults",
    "TransientResults",
    "ACAnalysisResults",
]
