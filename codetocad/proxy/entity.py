# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.entity_interface import EntityInterface


class Entity(
    EntityInterface,
):
    """
    Capabilities shared between scene objects.

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

        self.__proxied = get_provider(EntityInterface)(
            name, description, native_instance
        )  # type: ignore

    def is_exists(
        self,
    ) -> "bool":
        return self.__proxied.is_exists()

    def rename(
        self, new_name: "str", renamelinked_entities_and_landmarks: "bool" = True
    ):
        return self.__proxied.rename(new_name, renamelinked_entities_and_landmarks)

    def delete(self, remove_children: "bool" = True):
        return self.__proxied.delete(remove_children)

    def is_visible(
        self,
    ) -> "bool":
        return self.__proxied.is_visible()

    def set_visible(self, is_visible: "bool"):
        return self.__proxied.set_visible(is_visible)

    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ):
        return self.__proxied.apply(rotation, scale, location, modifiers)

    def get_native_instance(
        self,
    ) -> "object":
        return self.__proxied.get_native_instance()

    def get_location_world(
        self,
    ) -> "Point":
        return self.__proxied.get_location_world()

    def get_location_local(
        self,
    ) -> "Point":
        return self.__proxied.get_location_local()

    def select(
        self,
    ):
        return self.__proxied.select()

    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        return self.__proxied.translate_xyz(x, y, z)

    def translate_x(self, amount: "str|float|Dimension"):
        return self.__proxied.translate_x(amount)

    def translate_y(self, amount: "str|float|Dimension"):
        return self.__proxied.translate_y(amount)

    def translate_z(self, amount: "str|float|Dimension"):
        return self.__proxied.translate_z(amount)

    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        return self.__proxied.rotate_xyz(x, y, z)

    def rotate_x(self, rotation: "str|float|Angle"):
        return self.__proxied.rotate_x(rotation)

    def rotate_y(self, rotation: "str|float|Angle"):
        return self.__proxied.rotate_y(rotation)

    def rotate_z(self, rotation: "str|float|Angle"):
        return self.__proxied.rotate_z(rotation)

    def get_bounding_box(
        self,
    ) -> "BoundaryBox":
        return self.__proxied.get_bounding_box()

    def get_dimensions(
        self,
    ) -> "Dimensions":
        return self.__proxied.get_dimensions()
