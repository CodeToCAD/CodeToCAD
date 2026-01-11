"""
Build123d implementation of Shape class.
"""

import build123d as bd

from codetocad.core.cad.shape import Shape as BaseShape
from codetocad.core.cad.sketch import Draw as BaseDraw
from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType

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
    boolean_union,
    boolean_difference,
    boolean_intersection,
)
from codetocad.integrations.build123d.adapter.export import (
    export_step,
    export_stl,
    import_step,
    import_stl,
)


class Shape(BaseShape):
    """Build123d implementation of Shape operations."""

    def __new__(cls, *args, **kwargs):
        raise TypeError("Do not instantiate a Shape class, use its methods instead.")

    @staticmethod
    def extrude(edge: Edge, height: LengthType, draft_angle: AngleType = 0) -> Solid:
        """Extrude a 2D shape into a 3D solid."""
        native = edge.native

        # If edge has no native but has sub_edges, combine sub_edge natives into a Wire
        if native is None and edge.sub_edges:
            native_edges = []
            for sub in edge.sub_edges:
                if sub.native is not None:
                    native_edges.append(sub.native)
            if native_edges:
                # Combine edges into a Curve (Wire)
                native = bd.Curve() + native_edges

        if native is None:
            raise ValueError("Edge has no native build123d object")

        result = extrude_wire(native, height, draft_angle)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def revolve(edge: Edge, around: Edge, angle: AngleType) -> Solid:
        """Revolve a 2D shape around an axis to create a 3D solid."""
        native = edge.native
        if native is None:
            raise ValueError("Edge has no native build123d object")

        # Create axis from the around edge
        v1 = around.v1.to_tuple()
        v2 = around.v2.to_tuple()
        direction = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
        axis = (v1, direction)

        result = revolve_wire(native, axis, angle)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def loft(this: Edge, to: Edge, merge: bool = True) -> Solid:
        """Create a 3D solid by lofting between 2D shapes."""
        native1 = this.native
        native2 = to.native
        if native1 is None or native2 is None:
            raise ValueError("Edges have no native build123d objects")

        result = loft_wires([native1, native2], ruled=not merge)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def sweep(edge: Edge, path: Edge) -> Solid:
        """Sweep a 2D shape along a path to create a 3D solid."""
        profile_native = edge.native
        path_native = path.native
        if profile_native is None or path_native is None:
            raise ValueError("Edges have no native build123d objects")

        result = sweep_wire(profile_native, path_native)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def union(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
        """Combine this and that."""
        native1 = this.native
        native2 = that.native
        if native1 is None or native2 is None:
            raise ValueError("Solids have no native build123d objects")

        result = boolean_union(native1, native2)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def subtract(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
        """Subtract this solid from that."""
        native1 = this.native
        native2 = that.native
        if native1 is None or native2 is None:
            raise ValueError("Solids have no native build123d objects")

        result = boolean_difference(native1, native2)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def intersection(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
        """Keep only the overlapping parts of this and that solids."""
        native1 = this.native
        native2 = that.native
        if native1 is None or native2 is None:
            raise ValueError("Solids have no native build123d objects")

        result = boolean_intersection(native1, native2)
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def fillet(edge: Edge, radius: LengthType) -> Solid:
        """Round the corners of an edge."""
        native = edge.native
        if native is None:
            raise ValueError("Edge has no native build123d object")

        result = fillet_edges(
            native, [native] if isinstance(native, bd.Edge) else None, radius
        )
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def chamfer(edge: Edge, distance: LengthType) -> Solid:
        """Bevel the corners of an edge."""
        native = edge.native
        if native is None:
            raise ValueError("Edge has no native build123d object")

        result = chamfer_edges(
            native, [native] if isinstance(native, bd.Edge) else None, distance
        )
        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def mirror(solid: Solid, across: "Edge|Solid") -> Solid:
        """Mirror a solid across something."""
        native = solid.native
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
        new_solid.native = result
        return new_solid

    @staticmethod
    def pattern(
        solid: Solid,
        count: int,
        amount: LengthType,
        around: "Vertex|Edge|Solid|None" = None,
    ) -> Solid:
        """Create an array of solids."""
        native = solid.native
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
            new_solid.native = compound
            return new_solid
        elif results:
            new_solid = Solid(is_hidden=False)
            new_solid.native = results[0]
            return new_solid
        return solid

    @staticmethod
    def import_file(file_path: str) -> Solid:
        """Import a solid from a file."""
        if file_path.lower().endswith(".step") or file_path.lower().endswith(".stp"):
            result = import_step(file_path)
        elif file_path.lower().endswith(".stl"):
            result = import_stl(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

        solid = Solid(is_hidden=False)
        solid.native = result[0] if isinstance(result, list) else result
        return solid

    @staticmethod
    def export_file(solid: Solid, file_path: str) -> None:
        """Export a solid to a file."""
        native = solid.native
        if native is None:
            raise ValueError("Solid has no native build123d object")

        if file_path.lower().endswith(".step") or file_path.lower().endswith(".stp"):
            export_step(native, file_path)
        elif file_path.lower().endswith(".stl"):
            export_stl(native, file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    @staticmethod
    def cuboid(
        center: Vertex, width: LengthType, height: LengthType, depth: LengthType
    ) -> Solid:
        """Create a cuboid."""
        # Import here to avoid circular import
        from codetocad.integrations.build123d.cad.draw import Draw

        edge = Draw.rectangle(center, width, height)
        return Shape.extrude(edge, depth)

    @staticmethod
    def cylinder(center: Vertex, radius: LengthType, height: LengthType) -> Solid:
        """Create a cylinder."""
        from codetocad.integrations.build123d.cad.draw import Draw

        edge = Draw.circle(center, radius)
        return Shape.extrude(edge, height)

    @staticmethod
    def sphere(
        center: Vertex, radius: LengthType, angle: AngleType = "360deg"
    ) -> Solid:
        """Create a sphere."""
        from codetocad.integrations.build123d.cad.draw import Draw

        edge = Draw.circle(center, radius)
        around = BaseDraw.line(
            center, Vertex(x=center._x + radius, y=center._y, z=center._z)
        )
        return Shape.revolve(edge, around, angle)

    @staticmethod
    def torus(
        center: Vertex, major_radius: LengthType, minor_radius: LengthType
    ) -> Solid:
        """Create a torus."""
        result = create_torus(major_radius, minor_radius)
        # Move to center
        cx, cy, cz = center._x.value, center._y.value, center._z.value
        result = result.moved(bd.Location((cx, cy, cz)))

        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def cone(center: Vertex, radius: LengthType, height: LengthType) -> Solid:
        """Create a cone."""
        result = create_cone(radius, height)
        # Move to center
        cx, cy, cz = center._x.value, center._y.value, center._z.value
        result = result.moved(bd.Location((cx, cy, cz)))

        solid = Solid(is_hidden=False)
        solid.native = result
        return solid

    @staticmethod
    def pyramid(
        center: Vertex, width: LengthType, height: LengthType, depth: LengthType
    ) -> Solid:
        """Create a pyramid."""
        # Use extrude with draft angle to create a pyramid
        from codetocad.core.dimensions.length_expression import LengthExp
        from codetocad.integrations.build123d.cad.draw import Draw
        import math

        w = float(LengthExp(width))
        d = float(LengthExp(depth))

        # Calculate draft angle for pyramid (taper to a point)
        # tan(angle) = (w/2) / d
        draft_angle = math.degrees(math.atan2(w / 2, d))

        edge = Draw.rectangle(center, width, height)
        return Shape.extrude(edge, depth, draft_angle=f"{draft_angle}deg")
