from abc import ABC, abstractmethod
from codetocad.interfaces.cad.edge.edge_transform import EdgeTransformInterface
from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class EdgeInterface(ABC):
    def __init__(self, v1: "VertexInterface", v2: "VertexInterface"):
        self.v1: VertexInterface = v1
        self.v2: VertexInterface = v2
        self.transform = EdgeTransformInterface(self)
        self.name: str | None = None

    def direction(self):
        return self.v2.position - self.v1.position

    def length(self) -> float:
        """Get the length of the edge."""
        import numpy as np

        return float(np.linalg.norm(self.direction()))

    def midpoint(self) -> "VertexInterface":
        """Get the midpoint of the edge."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific vertex type
        raise NotImplementedError("midpoint must be implemented by concrete classes")

    def direction_vector(self) -> tuple[float, float, float]:
        """Get the direction vector of the edge."""
        direction = self.direction()
        return tuple(direction)

    def is_parallel_to(self, other: "EdgeInterface", tolerance: float = 1e-6) -> bool:
        """Check if this edge is parallel to another edge."""
        import numpy as np

        dir1 = self.direction()
        dir2 = other.direction()

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if cross product is near zero (parallel) or near 1 (anti-parallel)
        cross_product = np.cross(dir1_norm, dir2_norm)
        cross_magnitude = np.linalg.norm(cross_product)

        return cross_magnitude < tolerance

    def is_perpendicular_to(
        self, other: "EdgeInterface", tolerance: float = 1e-6
    ) -> bool:
        """Check if this edge is perpendicular to another edge."""
        import numpy as np

        dir1 = self.direction()
        dir2 = other.direction()

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if dot product is near zero
        dot_product = np.dot(dir1_norm, dir2_norm)

        return abs(dot_product) < tolerance

    def split_at_parameter(
        self, parameter: float
    ) -> tuple["EdgeInterface", "EdgeInterface"]:
        """Split the edge at a given parameter (0.0 to 1.0)."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific edge type
        raise NotImplementedError(
            "split_at_parameter must be implemented by concrete classes"
        )

    def __repr__(self):
        return f"Edge({self.v1.position}, {self.v2.position})"
