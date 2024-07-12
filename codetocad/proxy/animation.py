# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.animation_interface import AnimationInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Animation(
    AnimationInterface,
):
    """
    Animation related functionality.

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
    ):
        object.__setattr__(
            self, "__proxied", get_provider(AnimationInterface)()  # type: ignore
        )

    @staticmethod
    def default() -> "AnimationInterface":
        return get_provider(AnimationInterface).default()

    def set_frame_start(self, frame_number: "int") -> Self:
        return object.__getattribute__(self, "__proxied").set_frame_start(frame_number)

    def set_frame_end(self, frame_number: "int") -> Self:
        return object.__getattribute__(self, "__proxied").set_frame_end(frame_number)

    def set_frame_current(self, frame_number: "int") -> Self:
        return object.__getattribute__(self, "__proxied").set_frame_current(
            frame_number
        )

    def create_key_frame_location(
        self, entity: "str|EntityInterface", frame_number: "int"
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_key_frame_location(
            entity, frame_number
        )

    def create_key_frame_rotation(
        self, entity: "str|EntityInterface", frame_number: "int"
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_key_frame_rotation(
            entity, frame_number
        )
