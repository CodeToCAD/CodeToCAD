"""
Build123d implementation of Shape class.
"""

import math

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.enums.axis import Axis
from codetocad.core.enums.plane import Plane
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType, LengthExp
import codetocad.integrations.build123d.cad.draw as Draw
import codetocad.integrations.build123d.cad.transform as Transform


from codetocad.integrations.build123d.adapter.solid_operations import (
    extrude_wire,
    revolve_wire,
    loft_wires,
    sweep_wire,
    fillet_edges,
    chamfer_edges,
    mirror_solid,
    pattern_linear,
    pattern_polar,
    create_torus,
    create_cone,
)
from codetocad.integrations.build123d.adapter.geometry import (
    union as boolean_union,
    difference as boolean_difference,
    intersection as boolean_intersection,
)
from codetocad.integrations.build123d.adapter.export import (
    export_step,
    export_stl,
    import_step,
    import_stl,
)


def extrude(
    edge: Edge,
    height: LengthType,
    draft_angle: AngleType = 0,
    subtract: list[Edge] | None = None,
    plane: "Plane | Edge" = Plane.XY,
) -> Solid:
    """Extrude a 2D shape into a 3D solid.

    Args:
        edge: The 2D shape to extrude
        height: The extrusion height
        draft_angle: Optional draft angle for the extrusion
        subtract: Optional list of edges to subtract from the result
        plane: The plane to extrude from (default: XY) or an Edge representing a Face

    Returns:
        A 3D solid
    """
    native = edge.get_native()

    # If edge has no native but has sub_edges, combine sub_edge natives into a Wire
    if native is None and edge.sub_edges:
        native_edges = []
        for sub in edge.sub_edges:
            sub_native = sub.get_native()
            if sub_native is not None:
                native_edges.append(sub_native)
        if native_edges:
            # Combine edges into a Curve (Wire)
            native = bd.Curve() + native_edges

    if native is None:
        raise ValueError("Edge has no native build123d object")

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane for extrusion
        native_face = plane.get_native("face")
        if native_face is not None:
            # Create a plane from the face
            face_plane = bd.Plane(native_face)
            # Transform the wire to the face's plane before extruding
            native = face_plane * native

    result = extrude_wire(native, height, draft_angle)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def revolve(
    edge: Edge,
    around: Edge,
    angle: AngleType,
    subtract: list[Edge] | None = None,
    plane: "Plane | Edge" = Plane.XY,
) -> Solid:
    """Revolve a 2D shape around an axis to create a 3D solid.

    Args:
        edge: The 2D shape to revolve
        around: The axis to revolve around
        angle: The angle of revolution
        subtract: Optional list of edges to subtract from the result
        plane: The plane to revolve from (default: XY) or an Edge representing a Face

    Returns:
        A 3D solid
    """
    native = edge.get_native()
    if native is None:
        raise ValueError("Edge has no native build123d object")

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane
        native_face = plane.get_native("face")
        if native_face is not None:
            # Create a plane from the face
            face_plane = bd.Plane(native_face)
            # Transform the wire to the face's plane before revolving
            native = face_plane * native

    # Create axis from the around edge
    v1 = around.v1.to_tuple()
    v2 = around.v2.to_tuple()
    direction = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    axis = (v1, direction)

    result = revolve_wire(native, axis, angle)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def loft(
    this: Edge,
    to: Edge,
    merge: bool = True,
    subtract: list[Edge] | None = None,
    plane: "Plane | Edge" = Plane.XY,
) -> Solid:
    """Create a 3D solid by lofting between 2D shapes.

    Args:
        this: The first 2D shape
        to: The second 2D shape
        merge: If True, the two solids are merged (if the edges were part of solids)
        subtract: Optional list of edges to subtract from the result
        plane: The plane to loft from (default: XY) or an Edge representing a Face

    Returns:
        A 3D solid
    """
    native1 = this.get_native()
    native2 = to.get_native()
    if native1 is None or native2 is None:
        raise ValueError("Edges have no native build123d objects")

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane
        native_face = plane.get_native("face")
        if native_face is not None:
            # Create a plane from the face
            face_plane = bd.Plane(native_face)
            # Transform both wires to the face's plane before lofting
            native1 = face_plane * native1
            native2 = face_plane * native2

    result = loft_wires([native1, native2], ruled=not merge)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def sweep(edge: Edge, path: Edge) -> Solid:
    """Sweep a 2D shape along a path to create a 3D solid."""
    profile_native = edge.get_native()
    path_native = path.get_native()
    if profile_native is None or path_native is None:
        raise ValueError("Edges have no native build123d objects")

    result = sweep_wire(profile_native, path_native)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def union(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
    """Combine this and that."""
    native1 = this.get_native()
    native2 = that.get_native()
    if native1 is None or native2 is None:
        raise ValueError("Solids have no native build123d objects")

    # Check if solids are touching before performing union
    if not _are_solids_touching(native1, native2):
        raise ValueError('"Wingardium levi-ohhh-sa; object cannot be floating"-KM')

    result = boolean_union(native1, native2)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def subtract(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
    """Subtract this solid from that."""
    native1 = this.get_native()
    native2 = that.get_native()
    if native1 is None or native2 is None:
        raise ValueError("Solids have no native build123d objects")

    # Check if solids are touching before performing subtraction
    if not _are_solids_touching(native1, native2):
        raise ValueError('"Wingardium levi-ohhh-sa; object cannot be floating"-KM')

    result = boolean_difference(native1, native2)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def intersection(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
    """Keep only the overlapping parts of this and that solids."""
    native1 = this.get_native()
    native2 = that.get_native()
    if native1 is None or native2 is None:
        raise ValueError("Solids have no native build123d objects")

    # Check if solids are touching before performing intersection
    if not _are_solids_touching(native1, native2):
        raise ValueError('"Wingardium levi-ohhh-sa; object cannot be floating"-KM')

    result = boolean_intersection(native1, native2)
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def concat(this: Solid, that: Solid) -> Solid:
    """Concatenate/combine two solids into a compound without performing a boolean union.

    This method preserves both geometries as separate entities within a compound object,
    unlike union() which merges them into a single solid.

    Args:
        this: First solid to combine
        that: Second solid to combine

    Returns:
        A compound solid containing both input solids
    """
    native1 = this.get_native()
    native2 = that.get_native()
    if native1 is None or native2 is None:
        raise ValueError("Solids have no native build123d objects")

    # Create a compound by adding the two solids together
    # In build123d, the + operator creates a Compound when used on solids
    result = bd.Compound([native1, native2])
    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def fillet(
    solid: Solid,
    radius: LengthType,
    edges: "list[Edge] | None" = None,
) -> Solid:
    """Apply fillet to edges on a solid.

    Args:
        solid: Solid to fillet
        radius: Fillet radius
        edges: List of edges to fillet, or None to fillet ALL edges

    Returns:
        Solid with filleted edges
    """

    native = solid.get_native()
    if native is None:
        raise ValueError("Solid has no native build123d object")

    r = float(LengthExp(radius))

    if edges is None:
        # Apply to all edges
        native_edges = native.edges()
    else:
        # Get native edges from the provided Edge objects
        native_edges = [e.get_native() for e in edges if e.get_native() is not None]

    result = bd.fillet(native_edges, radius=r)

    new_solid = Solid(is_hidden=False)
    new_solid.set_native(result)
    return new_solid


def chamfer(
    solid: Solid,
    length: LengthType,
    edges: "list[Edge] | None" = None,
) -> Solid:
    """Apply chamfer to edges on a solid.

    Args:
        solid: Solid to chamfer
        length: Chamfer length
        edges: List of edges to chamfer, or None to chamfer ALL edges

    Returns:
        Solid with chamfered edges
    """

    native = solid.get_native()
    if native is None:
        raise ValueError("Solid has no native build123d object")

    dist = float(LengthExp(length))

    if edges is None:
        # Apply to all edges
        native_edges = native.edges()
    else:
        # Get native edges from the provided Edge objects
        native_edges = [e.get_native() for e in edges if e.get_native() is not None]

    result = bd.chamfer(native_edges, length=dist)

    new_solid = Solid(is_hidden=False)
    new_solid.set_native(result)
    return new_solid


def _get_bd_axis(axis: Axis) -> bd.Axis:
    """Convert our Axis enum to build123d Axis."""
    if axis == Axis.X:
        return bd.Axis.X
    elif axis == Axis.Y:
        return bd.Axis.Y
    else:
        return bd.Axis.Z


def _are_solids_touching(native1: "bd.Shape", native2: "bd.Shape") -> bool:
    """Check if two build123d solids are touching or intersecting.

    Args:
        native1: First build123d solid
        native2: Second build123d solid

    Returns:
        True if the solids are touching (bounding boxes overlap), False otherwise
    """
    # Get bounding boxes
    bbox1 = native1.bounding_box()
    bbox2 = native2.bounding_box()

    # Check if bounding boxes overlap in all three dimensions
    # Two boxes overlap if they overlap in X AND Y AND Z
    x_overlap = not (bbox1.max.X < bbox2.min.X or bbox2.max.X < bbox1.min.X)
    y_overlap = not (bbox1.max.Y < bbox2.min.Y or bbox2.max.Y < bbox1.min.Y)
    z_overlap = not (bbox1.max.Z < bbox2.min.Z or bbox2.max.Z < bbox1.min.Z)

    return x_overlap and y_overlap and z_overlap


def mirror(solid: Solid, across: "Edge|Solid") -> Solid:
    """Mirror a solid across something."""
    native = solid.get_native()
    if native is None:
        raise ValueError("Solid has no native build123d object")

    # Determine the mirror plane from 'across'
    if isinstance(across, Edge):
        # Use the edge to define a plane
        v1 = across.v1.to_tuple()
        # Create plane with edge as normal direction (use XZ plane offset to edge position)
        plane = bd.Plane.XZ.offset(v1[0])
    else:
        # Use XY plane through solid center by default
        plane = bd.Plane.XY

    result = mirror_solid(native, plane)
    new_solid = Solid(is_hidden=False)
    new_solid.set_native(result)
    return new_solid


def pattern(
    solid: Solid,
    count: int,
    amount: LengthType,
    around: "Vertex|Edge|Solid|None" = None,
) -> Solid:
    """Create an array of solids."""
    native = solid.get_native()
    if native is None:
        raise ValueError("Solid has no native build123d object")

    if around is None:
        # Linear pattern along X axis
        results = pattern_linear(native, count, amount, bd.Axis.X)
    elif isinstance(around, (Vertex, Edge)):
        # Polar pattern around the axis
        if isinstance(around, Vertex):
            axis = bd.Axis(
                (around._x.value, around._y.value, around._z.value), (0, 0, 1)
            )
        else:
            v1 = around.v1.to_tuple()
            v2 = around.v2.to_tuple()
            direction = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
            axis = bd.Axis(v1, direction)
        results = pattern_polar(native, count, axis, amount)
    else:
        # Linear pattern
        results = pattern_linear(native, count, amount, bd.Axis.X)

    # Combine all pattern results into one compound
    if len(results) > 1:
        compound = results[0]
        for r in results[1:]:
            compound = compound + r
        new_solid = Solid(is_hidden=False)
        new_solid.set_native(compound)
        return new_solid
    elif results:
        new_solid = Solid(is_hidden=False)
        new_solid.set_native(results[0])
        return new_solid
    return solid


def import_file(file_path: str) -> Solid:
    """Import a solid from a file."""
    if file_path.lower().endswith(".step") or file_path.lower().endswith(".stp"):
        result = import_step(file_path)
    elif file_path.lower().endswith(".stl"):
        result = import_stl(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

    solid = Solid(is_hidden=False)
    solid.set_native(result[0] if isinstance(result, list) else result)
    return solid


def export_file(solid: Solid, file_path: str) -> None:
    """Export a solid to a file."""
    native = solid.get_native()
    if native is None:
        raise ValueError("Solid has no native build123d object")

    if file_path.lower().endswith(".step") or file_path.lower().endswith(".stp"):
        export_step(native, file_path)
    elif file_path.lower().endswith(".stl"):
        export_stl(native, file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def cuboid(
    center: Vertex, width: LengthType, height: LengthType, depth: LengthType
) -> Solid:
    """Create a cuboid."""

    edge = Draw.rectangle(center, width, height)
    return extrude(edge, depth)


def cylinder(
    center: Vertex,
    radius: LengthType,
    height: LengthType,
    plane: Plane = Plane.XY,
) -> Solid:
    """Create a cylinder.

    Args:
        center: Center vertex of the cylinder
        radius: Radius of the cylinder
        height: Height of the cylinder
        plane: The plane to create the cylinder on (default: XY)
              - XY: cylinder extends along Z axis
              - XZ: cylinder extends along Y axis
              - YZ: cylinder extends along X axis

    Returns:
        Solid representing the cylinder
    """

    edge = Draw.circle(center, radius, plane=plane)
    return extrude(edge, height)


def sphere(center: Vertex, radius: LengthType, angle: AngleType = "360deg") -> Solid:
    """Create a sphere."""

    edge = Draw.circle(center, radius)
    around = Draw.line(center, Vertex(x=center._x + radius, y=center._y, z=center._z))
    return revolve(edge, around, angle)


def torus(center: Vertex, major_radius: LengthType, minor_radius: LengthType) -> Solid:
    """Create a torus."""
    result = create_torus(major_radius, minor_radius)
    # Move to center
    cx, cy, cz = center._x.value, center._y.value, center._z.value
    result = result.moved(bd.Location((cx, cy, cz)))

    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def cone(center: Vertex, radius: LengthType, height: LengthType) -> Solid:
    """Create a cone."""
    result = create_cone(radius, height)
    # Move to center
    cx, cy, cz = center._x.value, center._y.value, center._z.value
    result = result.moved(bd.Location((cx, cy, cz)))

    solid = Solid(is_hidden=False)
    solid.set_native(result)
    return solid


def pyramid(
    center: Vertex, width: LengthType, height: LengthType, depth: LengthType
) -> Solid:
    """Create a pyramid."""

    w = float(LengthExp(width))
    d = float(LengthExp(depth))

    # Calculate draft angle for pyramid (taper to a point)
    # tan(angle) = (w/2) / d
    draft_angle = math.degrees(math.atan2(w / 2, d))

    edge = Draw.rectangle(center, width, height)
    return extrude(edge, depth, draft_angle=f"{draft_angle}deg")


def rotate(solid: Solid, x: AngleType = 0, y: AngleType = 0, z: AngleType = 0) -> Solid:
    """Rotate a solid around the X, Y, and Z axes.

    Args:
        solid: The solid to rotate
        x: Rotation angle around X axis (default 0)
        y: Rotation angle around Y axis (default 0)
        z: Rotation angle around Z axis (default 0)

    Returns:
        The rotated solid
    """
    return Transform.rotate(solid, x=x, y=y, z=z)
