"""
Operations interface for Edge objects.
"""

from abc import ABC


class EdgeOperationsInterface(ABC):
    """Interface for edge operations."""

    def __init__(self, edge: "EdgeInterface"):
        self.edge = edge

    def split_at_parameter(
        self, parameter: float
    ) -> tuple["EdgeInterface", "EdgeInterface"]:
        """Split the edge at a given parameter (0.0 to 1.0)."""
        return self.edge.split_at_parameter(parameter)
