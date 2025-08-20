"""
Blender implementation of WireOperationsInterface.
"""

from codetocad.interfaces.cad.wire.wire_operations_interface import (
    WireOperationsInterface,
)
from codetocad.core.dimensions.length_expression import LengthType


class WireOperations(WireOperationsInterface):
    """Blender implementation of wire operations."""

    def reverse(self) -> "WireInterface":
        """Create a new wire with reversed direction."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.wire.wire import Wire
        from codetocad.adapters.blender.cad.edge.edge import Edge

        reversed_wire = Wire(name=f"{self.wire.name}_reversed")

        # Reverse the order of edges and flip each edge
        for edge in reversed(self.wire.edges):
            reversed_edge = Edge(edge.v2, edge.v1)
            reversed_wire.edges.append(reversed_edge)

        reversed_wire._update_blender_curve()
        return reversed_wire

    def close(self):
        """Close the wire by connecting the last vertex to the first."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.edge.edge import Edge

        if len(self.wire.edges) >= 2:
            first_vertex = self.wire.edges[0].v1
            last_vertex = self.wire.edges[-1].v2

            if first_vertex != last_vertex:
                closing_edge = Edge(last_vertex, first_vertex)
                self.wire.edges.append(closing_edge)
                self.wire._update_blender_curve()

    def extrude(self, length: LengthType) -> "PartInterface":
        """Extrude the wire to create a part."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.part.part import Part
        from codetocad.adapters.blender.cad.sketch.sketch import Sketch

        part = Part()
        sketch = Sketch()
        part.sketch = sketch
        sketch.wires.append(self.wire)
        self.wire.member_sketches.append(sketch)

        # Apply extrusion using Blender's solidify modifier
        part.extrude_sketch(length)

        return part
