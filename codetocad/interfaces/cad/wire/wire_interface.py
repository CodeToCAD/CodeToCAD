from typing import TYPE_CHECKING, List
from abc import ABC
from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraintInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
    from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


from abc import ABCMeta


class _WirePresetClassPropertyInterface(ABCMeta):
    """Metaclass to provide a preset property for the WireInterface class."""

    @property
    def preset(self):
        return WirePresetsInterface(WireInterface, None)


class WireInterface(ABC, metaclass=_WirePresetClassPropertyInterface):
    """Wire class representing a collection of edges and operations."""

    def __init__(self, sketch: "SketchInterface|None"):
        if sketch is not None:
            self.member_sketches: list[SketchInterface] = [sketch]
        else:
            self.member_sketches: list[SketchInterface] = []

        self.edges: list[EdgeInterface] = []
        self.add = WireAddInterface(self)
        self.get = WireGetInterface(self)
        self.constraint = WireConstraintInterface(self)
        self.name: str | None = None

    def is_closed(self) -> bool:
        """Check if the wire is closed."""
        if len(self.edges) < 3:
            return False

        # Check if the last vertex connects to the first vertex
        first_vertex = self.edges[0].v1
        last_vertex = self.edges[-1].v2

        # Use a small tolerance for comparison
        tolerance = 1e-6
        distance = first_vertex.distance_to(last_vertex)
        return distance < tolerance

    def length(self) -> float:
        """Get the total length of the wire."""
        return sum(edge.length() for edge in self.edges)

    def get_vertices(self) -> List["VertexInterface"]:
        """Get all unique vertices in the wire."""
        vertices = []
        for edge in self.edges:
            if edge.v1 not in vertices:
                vertices.append(edge.v1)
            if edge.v2 not in vertices:
                vertices.append(edge.v2)
        return vertices

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the wire as (min_point, max_point)."""
        if not self.edges:
            return ((0, 0, 0), (0, 0, 0))

        vertices = self.get_vertices()
        positions = [v.position for v in vertices]

        min_x = min(pos[0] for pos in positions)
        min_y = min(pos[1] for pos in positions)
        min_z = min(pos[2] for pos in positions)

        max_x = max(pos[0] for pos in positions)
        max_y = max(pos[1] for pos in positions)
        max_z = max(pos[2] for pos in positions)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def reverse(self) -> "WireInterface":
        """Create a new wire with reversed direction."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific wire type
        raise NotImplementedError("reverse must be implemented by concrete classes")

    def close(self):
        """Close the wire by connecting the last vertex to the first."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific edge type
        raise NotImplementedError("close must be implemented by concrete classes")

    def extrude(self, _length: LengthType) -> "PartInterface":
        """Extrude the wire to create a part."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific part type
        raise NotImplementedError("extrude must be implemented by concrete classes")

    def __repr__(self):
        return f"Wire({len(self.edges)} edges, closed={self.is_closed()})"
