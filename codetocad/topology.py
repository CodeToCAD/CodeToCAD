"""Geometric topography classes: vertex, edge, face, solid.

These are used to interact with native topology in the federated application.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .location import Location
from .units import LengthMeters


@dataclass
class Vertex:
    location: Location


@dataclass
class Edge:
    start: Vertex
    end: Vertex

    @property
    def midpoint(self) -> Location:
        return Location(
            (self.start.location.x.value + self.end.location.x.value) / 2,
            (self.start.location.y.value + self.end.location.y.value) / 2,
            (self.start.location.z.value + self.end.location.z.value) / 2,
        )

    @property
    def length(self) -> LengthMeters:
        return self.start.location.distance_to(self.end.location)


@dataclass
class Face:
    vertices: list[Vertex] = field(default_factory=list)

    @property
    def center(self) -> Location:
        count = len(self.vertices)
        return Location(
            sum(v.location.x.value for v in self.vertices) / count,
            sum(v.location.y.value for v in self.vertices) / count,
            sum(v.location.z.value for v in self.vertices) / count,
        )


@dataclass
class Solid:
    faces: list[Face] = field(default_factory=list)
