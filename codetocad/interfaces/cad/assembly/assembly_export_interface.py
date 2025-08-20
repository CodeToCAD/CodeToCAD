"""
Export operations interface for Assembly objects.
"""

from abc import ABC


class AssemblyExportInterface(ABC):
    """Interface for assembly export operations."""

    def __init__(self, assembly: "AssemblyInterface"):
        self.assembly = assembly

    def step(self, file_path: str):
        """Export the assembly to STEP format."""
        return self.assembly.export_step(file_path)

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the assembly to STL format."""
        return self.assembly.export_stl(file_path, tolerance)

    def brep(self, file_path: str):
        """Export the assembly to BREP format."""
        return self.assembly.export_brep(file_path)
