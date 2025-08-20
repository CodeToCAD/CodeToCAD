import numpy as np
from abc import ABC, abstractmethod
from codetocad.core.dimensions.length_expression import LengthExpression, LengthType
from codetocad.core.dimensions.point import Point


class VertexInterface(ABC):
    def __init__(self, x: LengthType, y: LengthType, z: LengthType = 0):
        self.position = np.array(
            [
                float(LengthExpression(x)),
                float(LengthExpression(y)),
                float(LengthExpression(z)),
            ]
        )
        self.name: str | None = None

    def transform(self, matrix):
        pos = np.append(self.position, 1)
        self.position = (matrix @ pos)[:3]

    def get_position(self) -> tuple[float, float, float]:
        """Get the current position of the vertex."""
        return tuple(self.position)

    def set_position(self, x: LengthType, y: LengthType, z: LengthType = 0):
        """Set the position of the vertex."""
        self.position = np.array(
            [
                float(LengthExpression(x)),
                float(LengthExpression(y)),
                float(LengthExpression(z)),
            ]
        )

    def distance_to(self, other: "VertexInterface") -> float:
        """Calculate distance to another vertex."""
        return float(np.linalg.norm(self.position - other.position))

    def get_point(self) -> Point:
        """Get the vertex position as a Point object."""
        return Point.from_list(self.position.tolist())

    def __repr__(self):
        return f"Vertex({self.position})"
