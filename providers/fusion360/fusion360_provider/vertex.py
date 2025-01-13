from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *


class Vertex(VertexInterface, Entity):

    def __init__(self, native_instance: "Any"):
        self.location = location
        self.parent = parent
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_control_points(self) -> "list[Vertex]":
        raise NotImplementedError()
        return [Vertex(location=(0, 0), name="myVertex")]

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return Sketch("a projected sketch")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location(self) -> "Point":
        print("get_location called")
        return Point.from_list_of_float_or_string([0, 0, 0])
