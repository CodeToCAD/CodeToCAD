"""
build123d implementation of PartExportInterface.
"""

from codetocad.interfaces.cad.part.part_export_interface import PartExportInterface
from codetocad.adapters.build123d.build123d_actions.export import (
    export_step,
    export_stl,
    export_brep,
)


class PartExport(PartExportInterface):
    """build123d implementation of part export operations."""

    def step(self, file_path: str):
        """Export the part to STEP format."""
        if self.part.native_instance:
            export_step(self.part.native_instance, file_path)

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the part to STL format."""
        if self.part.native_instance:
            export_stl(self.part.native_instance, file_path, tolerance)

    def brep(self, file_path: str):
        """Export the part to BREP format."""
        if self.part.native_instance:
            export_brep(self.part.native_instance, file_path)
