from dataclasses import dataclass

from codetocad.core.point import Point


@dataclass
class Vertex(Point):
    '''
    A single point in space.
    '''
    ...
