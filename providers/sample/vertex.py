# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.vertex_interface import VertexInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Vertex(VertexInterface, Entity):

    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.name = name
        self.location = location
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_control_points(
        self,
    ) -> "list[Point]":

        print(
            "get_control_points called",
        )

        return ["Point.from_list_of_float_or_string([0,0,0])"]

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:

        print("set_control_points called", f": {points}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":

        print("project called", f": {project_from}")

        return __import__("codetocad").Sketch("a projected sketch")
