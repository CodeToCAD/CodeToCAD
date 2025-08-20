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
        # Default implementation - adapters should override this
        pass

    def stl(self, file_path: str, tolerance: float = 0.1):
        """Export the part to STL format."""
        # Default implementation - adapters should override this
        pass

    def brep(self, file_path: str):
        """Export the part to BREP format."""
        # Default implementation - adapters should override this
        pass
