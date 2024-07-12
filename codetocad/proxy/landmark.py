# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.entity import Entity


class Landmark(LandmarkInterface, Entity):
    """
    Landmarks are named positions on an entity.

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
        parent_entity: "str|EntityInterface",
        description: "str| None" = None,
        native_instance=None,
    ):
        object.__setattr__(
            self,
            "__proxied",
            get_provider(LandmarkInterface)(
                name, parent_entity, description, native_instance
            ),  # type: ignore
        )

    def clone(
        self,
        new_name: "str",
        offset: "str|list[str]|list[float]|list[Dimension]|Dimensions| None" = None,
        new_parent: "str|EntityInterface| None" = None,
    ) -> "LandmarkInterface":
        return object.__getattribute__(self, "__proxied").clone(
            new_name, offset, new_parent
        )

    def get_landmark_entity_name(
        self,
    ) -> "str":
        return object.__getattribute__(self, "__proxied").get_landmark_entity_name()

    def get_parent_entity(
        self,
    ) -> "EntityInterface":
        return object.__getattribute__(self, "__proxied").get_parent_entity()
