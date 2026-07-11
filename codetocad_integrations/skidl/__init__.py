"""skidl integration: schematic capture for CodeToCAD Circuits.

``to_skidl(circuit)`` converts a ``codetocad.Circuit`` into a
`skidl <https://github.com/devbisme/skidl>`_ ``Circuit``; on top of that:

- ``export_netlist(circuit, path)`` writes a KiCad netlist (component
  footprints included, so the board can be laid out in KiCad's pcbnew),
- ``export_xml(circuit, path)`` writes the netlist as XML (for BOM tools),
- ``erc(circuit)`` runs skidl's electrical rules check,
- ``export_schematic(circuit, path)`` renders a schematic SVG using
  netlistsvg with standard analog symbols::

    from codetocad import Circuit, resistor, voltage_source
    from codetocad_integrations.skidl import export_netlist, export_schematic

    circuit = Circuit("divider")
    v1 = circuit.add(voltage_source(dc=9))
    r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
    circuit.connect(v1["+"], r1[1], name="VIN")
    circuit.connect(r1[2], r2[1], name="VOUT")
    circuit.connect(r2[2], v1["-"], circuit.gnd)

    export_netlist(circuit, "divider.net")
    export_schematic(circuit, "divider.svg")

Requires the skidl extra (``uv sync --extra skidl``). Schematic SVGs also
need `netlistsvg <https://github.com/nturley/netlistsvg>`_
(``npm install -g netlistsvg``, requires Node.js). Because every circuit
component carries a ``Footprint`` with a placeholder 3D body, the same
components are Part3Ds that can be placed straight into board assemblies.
"""

from codetocad_integrations.skidl.ecad import (
    erc,
    export_netlist,
    export_xml,
    to_skidl,
)
from codetocad_integrations.skidl.schematic import (
    export_schematic,
    find_netlistsvg,
    to_netlistsvg_json,
)

__all__ = [
    "to_skidl",
    "export_netlist",
    "export_xml",
    "erc",
    "export_schematic",
    "to_netlistsvg_json",
    "find_netlistsvg",
]
