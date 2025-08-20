"""
Blender implementation of AssemblyTransformInterface.
"""

from codetocad.interfaces.cad.assembly.assembly_transform_interface import (
    AssemblyTransformInterface,
)


class AssemblyTransform(AssemblyTransformInterface):
    """Blender implementation of assembly transformation operations."""

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
            blender_object = part._blender_object
            if blender_object:
                current_loc = blender_object.location
                blender_object.location = (
                    current_loc[0] + x,
                    current_loc[1] + y,
                    current_loc[2] + z,
                )

    def rotate(self, x: float, y: float, z: float):
        """Rotate all parts in the assembly."""
        for part in self.assembly.parts:
            blender_object = part._blender_object
            if blender_object:
                current_rot = blender_object.rotation_euler
                blender_object.rotation_euler = (
                    current_rot[0] + x,
                    current_rot[1] + y,
                    current_rot[2] + z,
                )

    def scale(self, x: float, y: float | None = None, z: float | None = None):
        """Scale all parts in the assembly."""
        y_val = y if y is not None else x
        z_val = z if z is not None else x

        for part in self.assembly.parts:
            blender_object = part._blender_object
            if blender_object:
                current_scale = blender_object.scale
                blender_object.scale = (
                    current_scale[0] * x,
                    current_scale[1] * y_val,
                    current_scale[2] * z_val,
                )
