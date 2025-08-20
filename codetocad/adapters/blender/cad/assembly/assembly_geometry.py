"""
Blender implementation of AssemblyGeometryInterface.
"""

from codetocad.interfaces.cad.assembly.assembly_geometry_interface import (
    AssemblyGeometryInterface,
)


class AssemblyGeometry(AssemblyGeometryInterface):
    """Blender implementation of assembly geometry operations."""

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of all parts in the assembly."""
        if not self.assembly.parts:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes of all parts
        part_boxes = [part.geometry.bounding_box() for part in self.assembly.parts]

        if not part_boxes:
            return ((0, 0, 0), (0, 0, 0))

        # Find overall min and max
        min_x = min(box[0][0] for box in part_boxes)
        min_y = min(box[0][1] for box in part_boxes)
        min_z = min(box[0][2] for box in part_boxes)

        max_x = max(box[1][0] for box in part_boxes)
        max_y = max(box[1][1] for box in part_boxes)
        max_z = max(box[1][2] for box in part_boxes)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def total_volume(self) -> float:
        """Get the total volume of all parts in the assembly."""
        return sum(part.geometry.volume() for part in self.assembly.parts)
