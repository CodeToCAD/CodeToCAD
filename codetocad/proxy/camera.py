# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.camera_interface import CameraInterface


from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Camera(CameraInterface, Entity):
    """
    Manipulate a camera object.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    __slots__ = [
        "__proxied",
    ]

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.__proxied = get_provider(CameraInterface)(
            name, description, native_instance
        )  # type: ignore

    def create_perspective(
        self,
    ):
        return self.__proxied.create_perspective()

    def create_orthogonal(
        self,
    ):
        return self.__proxied.create_orthogonal()

    def create_panoramic(
        self,
    ):
        return self.__proxied.create_panoramic()

    def set_focal_length(self, length: "float"):
        return self.__proxied.set_focal_length(length)
