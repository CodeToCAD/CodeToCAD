from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.codetocad_types import *


class Vertex(VertexInterface, Entity):

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()

    location: str | list[str] | list[float] | list[Dimension] | Point
    parent: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(self, native_instance: "Any"):
        self.location = location
        self.parent = parent
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_control_points(self) -> "list[Point]":
        raise NotImplementedError()

    @property
    def _center(self):
        return self.location

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> "Self":
        print("set_control_points called", f": {points}")
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location(self) -> "Point":
        print("get_location called")
        return Point.from_list_of_float_or_string([0, 0, 0])
