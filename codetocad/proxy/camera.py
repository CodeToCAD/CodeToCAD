# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.camera_interface import CameraInterface


from codetocad.proxy.entity import Entity


class Camera(CameraInterface, Entity):
    """
    Manipulate a camera object.

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
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        object.__setattr__(
            self,
            "__proxied",
            get_provider(CameraInterface)(
                name, description, native_instance
            ),  # type: ignore
        )

    def create_perspective(
        self,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_perspective()

    def create_orthogonal(
        self,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_orthogonal()

    def create_panoramic(
        self,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").create_panoramic()

    def set_focal_length(self, length: "float") -> Self:
        return object.__getattribute__(self, "__proxied").set_focal_length(length)
