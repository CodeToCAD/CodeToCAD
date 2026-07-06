"""
Solid operations for build123d - extrude, revolve, loft, sweep, boolean operations, etc.
"""

import math
import build123d as bd
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.dimensions.angle import Angle, AngleType


def extrude_wire(
    wire: "bd.Wire | bd.Sketch | bd.Face",
    height: LengthType,
    draft_angle: AngleType = 0,
) -> bd.Part:
    """Extrude a wire/sketch/face to create a 3D solid.

    Handles sketches with multiple faces (e.g., text where each letter
    is a separate face with holes properly defined) by extruding all faces
    and combining them.
    """
    h = float(LengthExp(height))
    draft = math.degrees(Angle(draft_angle).value)  # build123d uses degrees

    # Handle Sketch (e.g., text, complex shapes)
    if isinstance(wire, bd.Sketch):
        # Use faces() instead of wires() to properly handle holes in letters
        # Each face already has inner wires (holes) properly defined
        faces = wire.faces()
        if len(faces) == 1:
            # Single face - extrude normally
            if draft != 0:
                return bd.extrude(faces[0], h, taper=draft)
            return bd.extrude(faces[0], h)
        else:
            # Multiple faces - extrude each and combine
            # Each face preserves its holes (e.g., the hole in "O", "P", etc.)
            solids = []
            for face in faces:
                if draft != 0:
                    solid = bd.extrude(face, h, taper=draft)
                else:
                    solid = bd.extrude(face, h)
                solids.append(solid)
            # Combine all extruded solids
            if len(solids) == 1:
                return solids[0]
            result = solids[0]
            for s in solids[1:]:
                result = result + s
            return result

    # Handle Wire
    if isinstance(wire, bd.Wire):
        face = bd.Face(wire)
    else:
        face = wire

    if draft != 0:
        return bd.extrude(face, h, taper=draft)
    return bd.extrude(face, h)


def revolve_wire(
    wire: "bd.Wire | bd.Sketch | bd.Face",
    axis: "bd.Axis | tuple[tuple[float, float, float], tuple[float, float, float]]",
    angle: AngleType,
) -> bd.Part:
    """Revolve a wire/sketch/face around an axis to create a 3D solid."""
    angle_deg = math.degrees(Angle(angle).value)  # build123d uses degrees

    # Get face from wire/sketch if needed
    if isinstance(wire, bd.Sketch):
        face = wire.face()
    elif isinstance(wire, bd.Wire):
        face = bd.Face(wire)
    else:
        face = wire

    if isinstance(axis, tuple):
        # Create axis from origin and direction
        origin, direction = axis
        axis = bd.Axis(origin, direction)

    return bd.revolve(face, axis, angle_deg)


def loft_wires(
    wires: "list[bd.Wire | bd.Sketch | bd.Face]",
    ruled: bool = False,
) -> bd.Part:
    """Create a 3D solid by lofting between profiles."""
    # Get faces/wires from sketches if needed
    sections = []
    for w in wires:
        if isinstance(w, bd.Sketch):
            sections.append(w.face())
        elif isinstance(w, bd.Wire):
            sections.append(bd.Face(w))
        else:
            sections.append(w)

    return bd.loft(sections, ruled=ruled)


def sweep_wire(
    profile: "bd.Wire | bd.Sketch | bd.Face",
    path: "bd.Wire | bd.Edge",
) -> bd.Part:
    """Sweep a profile along a path to create a 3D solid."""
    # Get face from wire/sketch if needed
    if isinstance(profile, bd.Sketch):
        face = profile.face()
    elif isinstance(profile, bd.Wire):
        face = bd.Face(profile)
    else:
        face = profile

    return bd.sweep(face, path)


def fillet_edges(
    solid: "bd.Part | bd.Solid",
    edges: "list[bd.Edge] | None",
    radius: LengthType,
) -> bd.Part:
    """Apply fillet to edges of a solid."""
    r = float(LengthExp(radius))

    if edges is None:
        # Fillet all edges
        return bd.fillet(solid.edges(), r)
    return bd.fillet(edges, r)


def chamfer_edges(
    solid: "bd.Part | bd.Solid",
    edges: "list[bd.Edge] | None",
    distance: LengthType,
) -> bd.Part:
    """Apply chamfer to edges of a solid."""
    d = float(LengthExp(distance))

    if edges is None:
        # Chamfer all edges
        return bd.chamfer(solid.edges(), d)
    return bd.chamfer(edges, d)


def mirror_solid(
    solid: "bd.Part | bd.Solid",
    plane: bd.Plane,
) -> bd.Part:
    """Mirror a solid across a plane."""
    return bd.mirror(solid, about=plane)


def pattern_linear(
    solid: "bd.Part | bd.Solid",
    count: int,
    spacing: LengthType,
    axis: bd.Axis,
) -> "list[bd.Part]":
    """Create a linear pattern of solids."""
    s = float(LengthExp(spacing))

    # Create locations for the pattern
    locations = [bd.Location(axis.direction * (i * s)) for i in range(count)]

    return [solid.moved(loc) for loc in locations]


def pattern_polar(
    solid: "bd.Part | bd.Solid",
    count: int,
    axis: bd.Axis,
    angle: AngleType = "360deg",
) -> "list[bd.Part]":
    """Create a polar/circular pattern of solids."""
    total_angle = math.degrees(Angle(angle).value)
    angle_step = total_angle / count

    results = []
    for i in range(count):
        rotation = bd.Rotation(axis.direction, angle_step * i)
        results.append(solid.moved(bd.Location(rotation)))

    return results


def create_torus(
    major_radius: LengthType,
    minor_radius: LengthType,
) -> bd.Part:
    """Create a torus solid."""
    major_r = float(LengthExp(major_radius))
    minor_r = float(LengthExp(minor_radius))
    return bd.Torus(major_r, minor_r)


def create_cone(
    radius: LengthType,
    height: LengthType,
    top_radius: LengthType = 0,
) -> bd.Part:
    """Create a cone solid."""
    r = float(LengthExp(radius))
    h = float(LengthExp(height))
    top_r = float(LengthExp(top_radius))
    return bd.Cone(r, top_r, h)
