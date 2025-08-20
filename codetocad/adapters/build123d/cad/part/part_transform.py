"""
build123d implementation of PartTransformInterface.
"""

from codetocad.interfaces.cad.part.part_transform_interface import (
    PartTransformInterface,
)
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.build123d_actions.transformations import (
    translate_object,
    rotate_object,
    scale_object,
)


class PartTransform(PartTransformInterface):
    """build123d implementation of part transformation operations."""

    def translate(
        self, dx: LengthType, dy: LengthType, dz: LengthType = 0
    ) -> "PartInterface":
        """Translate the part."""
        if self.part.native_instance:
            self.part.native_instance = translate_object(
                self.part.native_instance, float(dx), float(dy), float(dz)
            )
        return self.part

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "PartInterface":
        """Rotate the part around an axis."""
        if self.part.native_instance:
            import build123d as bd

            axis_vector = bd.Vector(*axis)
            self.part.native_instance = rotate_object(
                self.part.native_instance, axis_vector, angle
            )
        return self.part

    def scale(
        self, scale_x: float, scale_y: float, scale_z: float = 1.0
    ) -> "PartInterface":
        """Scale the part."""
        if self.part.native_instance:
            self.part.native_instance = scale_object(
                self.part.native_instance, scale_x, scale_y, scale_z
            )
        return self.part

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        # For build123d, move is implemented as translate from origin
        if self.part.native_instance:
            # Get current center and translate to new position
            bbox = self.part.native_instance.bounding_box()
            current_center = bbox.center()
            dx = x - current_center.X
            dy = y - current_center.Y
            dz = z - current_center.Z
            self.part.native_instance = translate_object(
                self.part.native_instance, dx, dy, dz
            )
