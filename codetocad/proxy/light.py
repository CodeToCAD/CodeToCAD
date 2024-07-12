# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.light_interface import LightInterface


from codetocad.proxy.entity import Entity


class Light(LightInterface, Entity):
    """
    Manipulate a light object.

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
            get_provider(LightInterface)(
                name, description, native_instance
            ),  # type: ignore
        )

    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ) -> Self:
        return object.__getattribute__(self, "__proxied").set_color(
            r_value, g_value, b_value
        )

    def create_sun(self, energy_level: "float") -> Self:
        return object.__getattribute__(self, "__proxied").create_sun(energy_level)

    def create_spot(self, energy_level: "float") -> Self:
        return object.__getattribute__(self, "__proxied").create_spot(energy_level)

    def create_point(self, energy_level: "float") -> Self:
        return object.__getattribute__(self, "__proxied").create_point(energy_level)

    def create_area(self, energy_level: "float") -> Self:
        return object.__getattribute__(self, "__proxied").create_area(energy_level)
