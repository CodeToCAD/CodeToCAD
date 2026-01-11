"""
Shapes make up the building blocks of 3D models.

To simplify the code-CAD experience, we will combine edges, wires and faces into Edges. Faces are implicitly closed wires. Wires contain many edges.

CodeToCAD uses these building blocks:
* Vertex
* Edge
* Solid
"""
from dataclasses import dataclass
from enum import Enum, auto

from codetocad.core.cad.native import NativeObject
from codetocad.core.dimensions.point import Point


class CurveType(Enum):
    """Curve representation type for arcs, circles, and splines."""
    BEZIER = auto()
    NURBS = auto()


@dataclass(kw_only=True)
class Vertex(NativeObject, Point):
    """A vertex is a point in 3D space."""
    # Constraints
    coincide: "Vertex|Edge|None" = None
    midpoint: "Edge|None" = None

    # Bezier handles for curve control
    handle_in: "Vertex|None" = None    # Control point for incoming curve
    handle_out: "Vertex|None" = None   # Control point for outgoing curve
    weight: "float|None" = None       # Weight for rational curves (circles/arcs)

    is_hidden: bool = False


@dataclass(kw_only=True)
class Edge(NativeObject):
    """An edge in CodeToCAD is a continuous line between two vertices."""
    v1: Vertex
    v2: Vertex

    sub_edges: "list[Edge]|None" = None

    # NURBS knot vector (only needed for NURBS curves)
    knots: "list[float]|None" = None

    # Constraints
    coincide: "Vertex|Edge|None" = None
    parallel: "Edge|None" = None
    perpendicular: "Edge|None" = None
    tangent: "Edge|None" = None

    is_construction: bool = False

    is_hidden: bool = False


@dataclass(kw_only=True)
class Solid(NativeObject):
    """A solid is a 3D object defined by a set of closed Edges."""

    is_hidden: bool = False

