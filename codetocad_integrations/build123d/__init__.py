"""Build123D integration: federate CodeToCAD parts to Build123D/OpenCascade.

Usage::

    from codetocad_integrations.build123d import make_cube

    cube = make_cube("10cm", "10cm", "5cm")
    cube.hole(cube.top_center, radius_or_shape="4cm", amount="5cm")
    cube.export("my_cube.stl")

All CodeToCAD operations (booleans, shell, fillet, chamfer, hole, transform)
are replayed on real Build123D solids, and geometry queries/analysis use the
native OpenCascade topology.
"""

from codetocad_integrations.build123d.parts import (
    ElectricalComponent,
    Part2D,
    Part3D,
    adapt,
    make_box,
    make_capacitor,
    make_circle,
    make_cube,
    make_cylinder,
    make_fastener,
    make_import,
    make_led,
    make_rectangle,
    make_resistor,
    make_sphere,
    make_text,
)

__all__ = [
    "Part2D",
    "Part3D",
    "ElectricalComponent",
    "adapt",
    "make_cube",
    "make_box",
    "make_cylinder",
    "make_sphere",
    "make_import",
    "make_rectangle",
    "make_circle",
    "make_text",
    "make_led",
    "make_resistor",
    "make_capacitor",
    "make_fastener",
]
