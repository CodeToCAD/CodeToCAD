from dataclasses import dataclass
import math

from codetocad.core.cad.native import NativeObject
from codetocad.core.dimensions.angle import Angle, AngleType
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.cad.vertex_edge_solid import CurveType, Edge, Vertex
from codetocad.core.enums.plane import Plane


@dataclass
class Sketch(NativeObject):
    """A sketch is a 2D drawing in a plane."""
