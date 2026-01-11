from dataclasses import dataclass

from codetocad.core.cad.vertex_edge_solid import Edge, Vertex
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.enums.axis import AxisType


@dataclass
class Assembly:
    """An assembly is a collection of parts and other assemblies."""
    pass


class Constraint:
    """Common joint or mate constraint methods."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Do not instantiate a {cls.__name__} class, use its methods instead.")
    
    @staticmethod
    def fix(this: "Vertex|Edge", at: "Vertex|Edge", offset: "LengthType"=0) -> None:
        """Fix this to at. Same as, coincide."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def tangent(this: "Edge", at: "Edge") -> None:
        """Make this edge tangent to at."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def parallel(this: "Edge", at: "Edge") -> None:
        """Make this edge parallel to at."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def perpendicular(this: "Edge", at: "Edge") -> None:
        """Make this edge perpendicular to at."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def revolute(this: "Edge", at: "Edge", axis: "AxisType" = "z", limit_min: "AngleType|None" = None, limit_max: "AngleType|None" = None) -> None:
        """Create a revolute joint between this and at."""
        raise NotImplementedError("Method not implemented.")
    
    @staticmethod
    def prismatic(this: "Edge", at: "Edge", axis: "AxisType" = "z",limit_min: "LengthType|None" = None, limit_max: "LengthType|None" = None) -> None:
        """Create a prismatic joint between this and at."""
        raise NotImplementedError("Method not implemented.")

