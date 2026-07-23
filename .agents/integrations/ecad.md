# ECAD: skidl (schematics) & spice (circuit simulation)

Describe a circuit **once** as a `codetocad.Circuit` of components + nets (see
[core-classes.md](../core-classes.md)), then federate it two ways. The same
components are `Part3D`s with `Footprint`s, so they also drop into a board
assembly.

```python
from codetocad import Circuit, resistor, voltage_source

circuit = Circuit("divider")
v1 = circuit.add(voltage_source(dc=9))
r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
circuit.connect(v1["+"], r1[1], name="VIN")
circuit.connect(r1[2], r2[1], name="VOUT")
circuit.connect(r2[2], v1["-"], circuit.gnd)
```

## skidl — `codetocad_integrations.skidl`

Converts a `Circuit` into a [skidl](https://github.com/devbisme/skidl) circuit to
run ERC and write KiCad netlists/XML, and renders schematic SVGs with standard
analog symbols via [netlistsvg](https://github.com/nturley/netlistsvg).

Install: `uv sync --extra skidl` **and** `npm install -g netlistsvg`.

Public: `to_skidl`, `export_netlist`, `export_xml`, `erc`, `export_schematic`,
`to_netlistsvg_json`, `find_netlistsvg`.

```python
from codetocad_integrations.skidl import export_netlist, export_schematic
export_netlist(circuit, "divider.net")     # KiCad netlist (with footprints)
export_schematic(circuit, "divider.svg")   # schematic SVG (netlistsvg)
```

## spice — `codetocad_integrations.spice`

Builds a SPICE netlist from the `Circuit` (diode/LED models derived from each
component's electrical properties) and runs it with
[ngspice](https://ngspice.sourceforge.io). Results come back as numpy vectors
with `plot()`/`bode()` helpers.

Install: `uv sync --extra spice` **and** ngspice (`brew install ngspice` /
`apt install ngspice`).

Public: `simulate` → `SpiceSimulation`, `to_netlist`, `find_ngspice`, and result
types `SpiceResults`, `OperatingPointResults`, `DCSweepResults`,
`TransientResults`, `ACAnalysisResults`.

```python
from codetocad_integrations.spice import simulate
sim = simulate(circuit)
op = sim.operating_point()
print(op.voltage("VOUT"))            # 6.0
# also: sim.dc_sweep(...), sim.transient(...), sim.ac(...) → .plot()/.bode()
```

Examples: [skidl](../../codetocad_integrations/skidl/examples/),
[spice](../../codetocad_integrations/spice/examples/).
