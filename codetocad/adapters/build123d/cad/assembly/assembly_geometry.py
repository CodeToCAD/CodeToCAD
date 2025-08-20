"""
build123d implementation of AssemblyGeometryInterface.
"""

from codetocad.interfaces.cad.assembly.assembly_geometry_interface import (
    AssemblyGeometryInterface,
)


class AssemblyGeometry(AssemblyGeometryInterface):
    """build123d implementation of assembly geometry operations."""

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the entire assembly."""
        if not self.assembly.parts:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes from all parts
        bboxes = [part.geometry.bounding_box() for part in self.assembly.parts]

        # Find overall min and max coordinates
        min_x = min(bbox[0][0] for bbox in bboxes)
        min_y = min(bbox[0][1] for bbox in bboxes)
        min_z = min(bbox[0][2] for bbox in bboxes)
        max_x = max(bbox[1][0] for bbox in bboxes)
        max_y = max(bbox[1][1] for bbox in bboxes)
        max_z = max(bbox[1][2] for bbox in bboxes)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def total_volume(self) -> float:
        """Get the total volume of all parts in the assembly."""
        return sum(part.geometry.volume() for part in self.assembly.parts)
