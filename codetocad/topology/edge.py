from dataclasses import dataclass
from codetocad.topology.vertex import Vertex


@dataclass
class Edge:
    '''
    Curve bounded by two vertices
    '''
    v1: Vertex
    v2: Vertex
