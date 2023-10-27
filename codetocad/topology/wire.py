from dataclasses import dataclass
from typing import List

from codetocad.topology.edge import Edge


@dataclass
class Wire:
    '''
    A collection of edges.
    '''
    edges: List[Edge]
