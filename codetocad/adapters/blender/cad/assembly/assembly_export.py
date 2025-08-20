"""
Blender implementation of AssemblyExportInterface.
"""

from codetocad.interfaces.cad.assembly.assembly_export_interface import (
    AssemblyExportInterface,
)
from codetocad.adapters.blender.blender_actions.import_export import export_objects


class AssemblyExport(AssemblyExportInterface):
    """Blender implementation of assembly export operations."""

    def step(self, file_path: str):
        """Export the assembly to STEP format."""
        # Blender doesn't have native STEP export, would need addon
        raise NotImplementedError("STEP export requires additional Blender addon")

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the assembly to STL format."""
        blender_objects = self._get_all_blender_objects()
        export_objects(blender_objects, file_path)

    def brep(self, file_path: str):
        """Export the assembly to BREP format."""
        # Blender doesn't have native BREP export
        raise NotImplementedError("BREP export not supported in Blender")

    def obj(self, file_path: str):
        """Export the assembly to OBJ format."""
        blender_objects = self._get_all_blender_objects()
        export_objects(blender_objects, file_path)

    def _get_all_blender_objects(self) -> "list[bpy.types.Object]":
        """Get all Blender objects in the assembly."""
        return [
            obj
            for obj in [part._blender_object for part in self.assembly.parts]
            if obj is not None
        ]
