"""
build123d implementation of AssemblyExportInterface.
"""

from codetocad.interfaces.cad.assembly.assembly_export_interface import (
    AssemblyExportInterface,
)
from codetocad.adapters.build123d.build123d_actions.export import (
    export_step,
    export_stl,
    export_brep,
)


class AssemblyExport(AssemblyExportInterface):
    """build123d implementation of assembly export operations."""

    def step(self, file_path: str):
        """Export the assembly to STEP format."""
        # Get all native instances and export as compound
        native_instances = self.assembly.get_all_native_instances()
        if native_instances:
            # For now, export the first part - full assembly export would need compound creation
            export_step(native_instances[0], file_path)

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the assembly to STL format."""
        # Get all native instances and export as compound
        native_instances = self.assembly.get_all_native_instances()
        if native_instances:
            # For now, export the first part - full assembly export would need compound creation
            export_stl(native_instances[0], file_path, tolerance)

    def brep(self, file_path: str):
        """Export the assembly to BREP format."""
        # Get all native instances and export as compound
        native_instances = self.assembly.get_all_native_instances()
        if native_instances:
            # For now, export the first part - full assembly export would need compound creation
            export_brep(native_instances[0], file_path)
