"""
Transform operations interface for Assembly objects.
"""

from abc import ABC


class AssemblyTransformInterface(ABC):
    """Interface for assembly transformation operations."""

    def __init__(self, assembly: "AssemblyInterface"):
        self.assembly = assembly

    def translate_all(self, dx: float, dy: float, dz: float = 0):
        """Translate all parts in the assembly."""
        return self.assembly.translate_all(dx, dy, dz)

    def rotate_all(self, axis: tuple[float, float, float], angle: float):
        """Rotate all parts in the assembly."""
        return self.assembly.rotate_all(axis, angle)

    def scale_all(self, scale_x: float, scale_y: float, scale_z: float = 1.0):
        """Scale all parts in the assembly."""
        return self.assembly.scale_all(scale_x, scale_y, scale_z)

    def move(self, x: float, y: float, z: float):
        """Move all parts in the assembly."""
        return self.assembly.move(x, y, z)

    def rotate(self, x: float, y: float, z: float):
        """Rotate all parts in the assembly."""
        return self.assembly.rotate(x, y, z)

    def scale(self, x: float, y: float | None = None, z: float | None = None):
        """Scale all parts in the assembly."""
        return self.assembly.scale(x, y, z)
