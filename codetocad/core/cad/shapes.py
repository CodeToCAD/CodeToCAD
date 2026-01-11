"""
Shapes make up the building blocks of 3D models. 

CodeToCAD uses these building blocks:
* Vertex
* Edge
* Solid
"""
from dataclasses import dataclass
from codetocad.core.cad.native import NativeObject
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.dimensions.point import Point

    
@dataclass(kw_only=True)
class Vertex(NativeObject, Point):
    """A vertex is a point in 3D space."""
    coincide: "Vertex|Edge|None" = None
    midpoint: "Edge|None" = None

    is_hidden: bool = False


@dataclass(kw_only=True)
class Edge(NativeObject):
    """An edge in CodeToCAD is a continous line between two vertices, there may be other vertices between the two vertices."""
    v1: Vertex
    v2: Vertex

    sub_edges: "list[Edge]|None" = None

    coincide: "Vertex|Edge|None"  = None
    parallel: "Edge|None"  = None
    perpendicular: "Edge|None"  = None
    tangent: "Edge|None"  = None


    is_construction: bool = False

    is_hidden: bool = False


@dataclass(kw_only=True)
class Solid(NativeObject):
    """A solid is a 3D object defined by a set of closed Edges."""

    is_hidden: bool = False

