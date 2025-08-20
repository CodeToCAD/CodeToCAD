"""
build123d implementation of EdgeInterface.
"""

from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.adapters.build123d.cad.vertex.vertex import Vertex
from codetocad.adapters.build123d.build123d_actions.geometry import (
    create_edge_from_vertices,
)
from codetocad.adapters.build123d.build123d_actions.transformations import (
    translate_object,
    get_length,
)

if TYPE_CHECKING:
    import build123d as bd


class Edge(EdgeInterface):
    """build123d implementation of EdgeInterface."""

    def __init__(
        self,
        v1: "Vertex",
        v2: "Vertex",
        name: str | None = None,
        native_instance: "bd.Edge | None" = None,
    ):
        # Initialize the parent interface
        super().__init__(v1, v2)

        # build123d-specific properties
        self.name = name or f"edge_{str(uuid4())[:8]}"

        # Create or use provided build123d edge
        if native_instance is not None:
            self.native_instance = native_instance
        else:
            self.native_instance = create_edge_from_vertices(
                v1.native_instance, v2.native_instance
            )

    def __repr__(self):
        return f"Edge({self.v1.position}, {self.v2.position})"
