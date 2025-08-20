"""
build123d implementation of PartGeometryInterface.
"""

from codetocad.interfaces.cad.part.part_geometry_interface import PartGeometryInterface


class PartGeometry(PartGeometryInterface):
    """build123d implementation of part geometry operations."""

    def volume(self) -> float:
        """Get the volume of the part."""
        if self.part.native_instance:
            return float(self.part.native_instance.volume)
        return 0.0

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        if self.part.native_instance:
            bbox = self.part.native_instance.bounding_box()
            return (
                (bbox.min.X, bbox.min.Y, bbox.min.Z),
                (bbox.max.X, bbox.max.Y, bbox.max.Z),
            )
        return ((0, 0, 0), (0, 0, 0))
