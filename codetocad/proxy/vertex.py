# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.vertex_interface import VertexInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.entity import Entity


class Vertex(VertexInterface, Entity):
    """
    A single point in space, or a control point.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, "__proxied"), name)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "__proxied"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "__proxied"), name, value)

    def __nonzero__(self):
        return bool(object.__getattribute__(self, "__proxied"))

    def __str__(self):
        return str(object.__getattribute__(self, "__proxied"))

    def __repr__(self):
        return repr(object.__getattribute__(self, "__proxied"))

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
        object.__setattr__(
            self,
            "__proxied",
            get_provider(VertexInterface)(
                name, location, description, native_instance, parent_entity
            ),  # type: ignore
        )

    def get_control_points(
        self,
    ) -> "list[Point]":
        return object.__getattribute__(self, "__proxied").get_control_points()

    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:
        return object.__getattribute__(self, "__proxied").set_control_points(points)

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        return object.__getattribute__(self, "__proxied").project(project_from)
