from codetocad.core.cad.sketch import Draw
from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType


class Shape:
    """Common solid generation methods."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Do not instantiate a {cls.__name__} class, use its methods instead.")
    
    @staticmethod
    def extrude(edge: Edge, height: LengthType, draft_angle: AngleType = 0, ) -> Solid:
        """Extrude a 2D shape into a 3D solid."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def revolve(edge: Edge, around: Edge, angle: AngleType) -> Solid:
        """Revolve a 2D shape around an axis to create a 3D solid."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def loft(this: Edge, to: Edge, merge: bool = True) -> Solid:
        """Create a 3D solid by lofting between 2D shapes. If merge is True, the two solids are merged, if the edges were part of solids."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def sweep(edge: Edge, path: Edge) -> Solid:
        """Sweep a 2D shape along a path to create a 3D solid."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def union(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
        """Combine this and that."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def subtract(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
        """Subtract this solid from that."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def intersection(this: Solid, that: Solid, delete_this: bool = True) -> Solid:
        """Keep only the overlapping parts of this and that solids."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def fillet(edge: Edge, radius: LengthType) -> Solid:
        """Round the corners of an edge."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def chamfer(edge: Edge, distance: LengthType) -> Solid:
        """Bevel the corners of an edge."""
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def mirror(solid: Solid, across: "Edge|Solid") -> Solid:
        """Mirror a solid across a something."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def pattern(solid: Solid, count: int, amount: LengthType, around:"Vertex|Edge|Solid|None" = None) -> Solid:
        """Create an array of solids."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def import_file(file_path: str) -> Solid:
        """Import a solid from a file."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def export_file(solid: Solid, file_path: str) -> None:
        """Export a solid to a file."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def cuboid(center: Vertex, width: LengthType, height: LengthType, depth: LengthType) -> Solid:
        """Create a cuboid."""
        edge = Draw.rectangle(center, width, height)
        return Shape.extrude(edge, depth)
    
    @staticmethod
    def cylinder(center: Vertex, radius: LengthType, height: LengthType) -> Solid:
        """Create a cylinder."""
        edge = Draw.circle(center, radius)
        return Shape.extrude(edge, height)
    
    @staticmethod
    def sphere(center: Vertex, radius: LengthType, angle: AngleType = "360deg") -> Solid:
        """Create a sphere."""
        edge = Draw.circle(center, radius)
        around = Draw.line(center, Vertex(x=center._x + radius, y=center._y, z=center._z))
        return Shape.revolve(edge, around, angle)
    
    @staticmethod
    def torus(center: Vertex, major_radius: LengthType, minor_radius: LengthType) -> Solid:
        """Create a torus."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def cone(center: Vertex, radius: LengthType, height: LengthType) -> Solid:
        """Create a cone."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def pyramid(center: Vertex, width: LengthType, height: LengthType, depth: LengthType) -> Solid:
        """Create a pyramid."""
        raise NotImplementedError("Method not implemented.")
    

