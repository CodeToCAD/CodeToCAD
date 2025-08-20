"""
Sketch and wire operations for build123d.
"""

from typing import List, Tuple, Optional
import build123d as bd
from codetocad.core.dimensions.length_expression import LengthType, LengthExpression


def create_sketch_context() -> bd.BuildSketch:
    """Create a build123d sketch context."""
    return bd.BuildSketch()


def create_line_context() -> bd.BuildLine:
    """Create a build123d line context."""
    return bd.BuildLine()


def add_line_to_sketch(
    sketch_context: bd.BuildSketch, start: Tuple[float, float], end: Tuple[float, float]
) -> None:
    """Add a line to a sketch context."""
    with sketch_context:
        bd.Line(bd.Vector(*start, 0), bd.Vector(*end, 0))


def add_rectangle_to_sketch(
    sketch_context: bd.BuildSketch,
    width: LengthType,
    height: LengthType,
    center: Tuple[float, float] = (0, 0),
) -> None:
    """Add a rectangle to a sketch context."""
    w = float(LengthExpression(width))
    h = float(LengthExpression(height))

    with sketch_context:
        bd.Rectangle(w, h, align=(bd.Align.CENTER, bd.Align.CENTER))


def add_circle_to_sketch(
    sketch_context: bd.BuildSketch,
    radius: LengthType,
    center: Tuple[float, float] = (0, 0),
) -> None:
    """Add a circle to a sketch context."""
    r = float(LengthExpression(radius))

    with sketch_context:
        bd.Circle(r)


def add_arc_to_sketch(
    sketch_context: bd.BuildSketch,
    start_angle: float,
    end_angle: float,
    radius: LengthType,
    center: Tuple[float, float] = (0, 0),
) -> None:
    """Add an arc to a sketch context."""
    r = float(LengthExpression(radius))

    with sketch_context:
        bd.Arc(
            center=bd.Vector(*center, 0),
            radius=r,
            start_angle=start_angle,
            arc_size=end_angle - start_angle,
        )


def add_spline_to_sketch(
    sketch_context: bd.BuildSketch, points: List[Tuple[float, float]]
) -> None:
    """Add a spline through points to a sketch context."""
    vertices = [bd.Vector(*point, 0) for point in points]

    with sketch_context:
        bd.Spline(*vertices)


def close_wire_in_sketch(sketch_context: bd.BuildSketch) -> None:
    """Close the current wire in a sketch context."""
    # In build123d, wires are typically closed automatically when needed
    # This is a placeholder for explicit closing if needed
    pass


def get_sketch_wires(sketch_context: bd.BuildSketch) -> List[bd.Wire]:
    """Get all wires from a sketch context."""
    if hasattr(sketch_context, "wires"):
        return sketch_context.wires
    elif hasattr(sketch_context, "sketch"):
        return sketch_context.sketch.wires()
    else:
        return []


def get_sketch_faces(sketch_context: bd.BuildSketch) -> List[bd.Face]:
    """Get all faces from a sketch context."""
    if hasattr(sketch_context, "faces"):
        return sketch_context.faces
    elif hasattr(sketch_context, "sketch"):
        return sketch_context.sketch.faces()
    else:
        return []


def make_face_from_sketch(sketch_context: bd.BuildSketch) -> bd.Face:
    """Create a face from a sketch context."""
    faces = get_sketch_faces(sketch_context)
    if faces:
        return faces[0]

    wires = get_sketch_wires(sketch_context)
    if wires:
        return bd.Face.make_from_wires(wires[0])

    raise ValueError("No wires or faces found in sketch context")


def extrude_sketch(sketch_context: bd.BuildSketch, distance: LengthType) -> bd.Solid:
    """Extrude a sketch to create a solid."""
    dist = float(LengthExpression(distance))
    face = make_face_from_sketch(sketch_context)
    return bd.Solid.extrude(face, bd.Vector(0, 0, dist))


def revolve_sketch(
    sketch_context: bd.BuildSketch,
    axis: bd.Vector = bd.Vector(0, 0, 1),
    angle: float = 360,
) -> bd.Solid:
    """Revolve a sketch around an axis to create a solid."""
    face = make_face_from_sketch(sketch_context)
    return bd.Solid.revolve(face, axis, angle)
