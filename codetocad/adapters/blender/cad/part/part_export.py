"""
Blender implementation of PartExportInterface.
"""

from codetocad.interfaces.cad.part.part_export_interface import PartExportInterface


class PartExport(PartExportInterface):
    """Blender implementation of part export operations."""

    def step(self, file_path: str):
        """Export the part to STEP format."""
        # Blender doesn't have native STEP export, would need addon
        raise NotImplementedError("STEP export requires additional Blender addon")

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the part to STL format."""
        if self.part._blender_object:
            # This would require using Blender's export operators
            # For now, raise NotImplementedError as it requires bpy.ops context
            raise NotImplementedError(
                "STL export requires Blender context and operators"
            )

    def brep(self, file_path: str):
        """Export the part to BREP format."""
        # Blender doesn't have native BREP export
        raise NotImplementedError("BREP export not supported in Blender")
