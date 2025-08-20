"""
Export operations interface for Part objects.
"""

from abc import ABC


class PartExportInterface(ABC):
    """Interface for part export operations."""

    def __init__(self, part: "PartInterface"):
        self.part = part

    def step(self, file_path: str):
        """Export the part to STEP format."""
        return self.part.export_step(file_path)

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the part to STL format."""
        return self.part.export_stl(file_path, tolerance)

    def brep(self, file_path: str):
        """Export the part to BREP format."""
        return self.part.export_brep(file_path)
