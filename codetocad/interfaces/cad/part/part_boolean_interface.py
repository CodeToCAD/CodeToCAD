"""
Boolean operations interface for Part objects.
"""

from abc import ABC


class PartBooleanInterface(ABC):
    """Interface for part boolean operations."""

    def __init__(self, part: "PartInterface"):
        self.part = part

    def union(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean union with another part."""
        # Default implementation - adapters should override this
        return self.part

    def difference(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean difference with another part."""
        # Default implementation - adapters should override this
        return self.part

    def intersection(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean intersection with another part."""
        # Default implementation - adapters should override this
        return self.part
