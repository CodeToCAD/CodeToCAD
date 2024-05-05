# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.vertex_interface import VertexInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Vertex(VertexInterface, Entity):
    """
    A single point in space, or a control point.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    __slots__ = [
        "__proxied",
    ]

    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.__proxied = get_provider(VertexInterface)(
            name, location, description, native_instance, parent_entity
        )  # type: ignore

    def get_control_points(
        self,
    ) -> "list[VertexInterface]":
        return self.__proxied.get_control_points()

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        return self.__proxied.project(project_from)
