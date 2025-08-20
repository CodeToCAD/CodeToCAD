"""
Blender implementation of PartGeometryInterface.
"""

from codetocad.interfaces.cad.part.part_geometry_interface import PartGeometryInterface
import bmesh


class PartGeometry(PartGeometryInterface):
    """Blender implementation of part geometry operations."""

    def volume(self) -> float:
        """Get the volume of the part."""
        if self.part._blender_object and hasattr(self.part._blender_object, "data"):
            try:
                import bpy

                if isinstance(self.part._blender_object.data, bpy.types.Mesh):
                    # Create bmesh instance
                    bm = bmesh.new()
                    bm.from_mesh(self.part._blender_object.data)
                    bm.transform(self.part._blender_object.matrix_world)

                    # Calculate volume
                    volume = bm.calc_volume()
                    bm.free()
                    return volume
            except ImportError:
                pass
        return 0.0

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        if self.part._blender_object:
            try:
                import mathutils

                # Get bounding box in world coordinates
                bbox = [
                    self.part._blender_object.matrix_world @ mathutils.Vector(corner)
                    for corner in self.part._blender_object.bound_box
                ]

                # Find min and max coordinates
                min_coords = [min(corner[i] for corner in bbox) for i in range(3)]
                max_coords = [max(corner[i] for corner in bbox) for i in range(3)]

                return (
                    (min_coords[0], min_coords[1], min_coords[2]),
                    (max_coords[0], max_coords[1], max_coords[2]),
                )
            except ImportError:
                pass

        return ((0, 0, 0), (0, 0, 0))
