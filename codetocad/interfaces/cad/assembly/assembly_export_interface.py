"""
Export operations interface for Assembly objects.
"""

from abc import ABC

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class AssemblyExportInterface(ABC):
    """Interface for assembly export operations."""

    def __init__(self, assembly: "AssemblyInterface"):
        self.assembly = assembly

    def step(self, file_path: str):
        """Export the assembly to STEP format."""
        # Default implementation - adapters should override this
        pass

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the assembly to STL format."""
        # Default implementation - adapters should override this
        pass

    def brep(self, file_path: str):
        """Export the assembly to BREP format."""
        # Default implementation - adapters should override this
        pass
