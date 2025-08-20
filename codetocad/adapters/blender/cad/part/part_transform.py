"""
Blender implementation of PartTransformInterface.
"""

from codetocad.interfaces.cad.part.part_interface import PartInterface
from codetocad.interfaces.cad.part.part_transform_interface import (
    PartTransformInterface,
)
from codetocad.core.dimensions.length_expression import LengthType, LengthExpression


class PartTransform(PartTransformInterface):
    """Blender implementation of part transformation operations."""

    def translate(
        self, dx: LengthType, dy: LengthType, dz: LengthType = 0
    ) -> "PartInterface":
        """Translate the part."""
        if self.part._blender_object:
            current_loc = self.part._blender_object.location
            self.part._blender_object.location = (
                current_loc[0] + float(LengthExpression(dx)),
                current_loc[1] + float(LengthExpression(dy)),
                current_loc[2] + float(LengthExpression(dz)),
            )
        return self.part

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "PartInterface":
        """Rotate the part around an axis."""
        if self.part._blender_object:
            # Convert axis-angle to Euler angles (simplified)
            # This is a basic implementation - more complex rotation would require matrix math
            import math

            magnitude = math.sqrt(sum(a * a for a in axis))
            if magnitude > 0:
                # Normalize axis and apply rotation
                normalized_axis = tuple(a / magnitude for a in axis)
                # For simplicity, apply rotation as Euler angles
                # In a full implementation, this would use proper axis-angle to Euler conversion
                self.part._blender_object.rotation_euler = (
                    normalized_axis[0] * angle,
                    normalized_axis[1] * angle,
                    normalized_axis[2] * angle,
                )
        return self.part

    def scale(
        self, scale_x: float, scale_y: float, scale_z: float = 1.0
    ) -> "PartInterface":
        """Scale the part."""
        if self.part._blender_object:
            current_scale = self.part._blender_object.scale
            self.part._blender_object.scale = (
                current_scale[0] * scale_x,
                current_scale[1] * scale_y,
                current_scale[2] * scale_z,
            )
        return self.part

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        if self.part._blender_object:
            self.part._blender_object.location = (x, y, z)
