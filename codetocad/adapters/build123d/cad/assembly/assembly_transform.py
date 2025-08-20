"""
build123d implementation of AssemblyTransformInterface.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_transform_interface import (
        AssemblyTransformInterface,
    )


class AssemblyTransform(AssemblyTransformInterface):
    """build123d implementation of assembly transformation operations."""

    def translate_all(self, dx: float, dy: float, dz: float = 0):
        """Translate all parts in the assembly."""
        for part in self.assembly.parts:
            part.transform.translate(dx, dy, dz)

    def rotate_all(self, axis: tuple[float, float, float], angle: float):
        """Rotate all parts in the assembly."""
        for part in self.assembly.parts:
            part.transform.rotate(axis, angle)

    def scale_all(self, scale_x: float, scale_y: float, scale_z: float = 1.0):
        """Scale all parts in the assembly."""
        for part in self.assembly.parts:
            part.transform.scale(scale_x, scale_y, scale_z)

    def move(self, x: float, y: float, z: float):
        """Move all parts in the assembly."""
        for part in self.assembly.parts:
            part.transform.move(x, y, z)

    def rotate(self, x: float, y: float, z: float):
        """Rotate all parts in the assembly."""
        for part in self.assembly.parts:
            # Convert to axis-angle representation for consistency
            import math

            # This is a simplified rotation - adapters should implement proper rotation
            magnitude = math.sqrt(x * x + y * y + z * z)
            if magnitude > 0:
                axis = (x / magnitude, y / magnitude, z / magnitude)
                part.transform.rotate(axis, magnitude)

    def scale(self, x: float, y: float | None = None, z: float | None = None):
        """Scale all parts in the assembly."""
        y_val = y if y is not None else x
        z_val = z if z is not None else x
        for part in self.assembly.parts:
            part.transform.scale(x, y_val, z_val)
