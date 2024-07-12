# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.joint_interface import JointInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Joint(
    JointInterface,
):
    """
    Joints define the relationships and constraints between entities.

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

    def __init__(self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"):
        object.__setattr__(
            self,
            "__proxied",
            get_provider(JointInterface)(entity1, entity2),  # type: ignore
        )

    def translate_landmark_onto_another(
        self,
    ) -> Self:
        return object.__getattribute__(
            self, "__proxied"
        ).translate_landmark_onto_another()

    def pivot(
        self,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").pivot()

    def gear_ratio(self, ratio: "float") -> Self:
        return object.__getattribute__(self, "__proxied").gear_ratio(ratio)

    def limit_location_xyz(
        self,
        x: "str|float|Dimension| None" = None,
        y: "str|float|Dimension| None" = None,
        z: "str|float|Dimension| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_location_xyz(x, y, z)

    def limit_location_x(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_location_x(min, max)

    def limit_location_y(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_location_y(min, max)

    def limit_location_z(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_location_z(min, max)

    def limit_rotation_xyz(
        self,
        x: "str|float|Angle| None" = None,
        y: "str|float|Angle| None" = None,
        z: "str|float|Angle| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_rotation_xyz(x, y, z)

    def limit_rotation_x(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_rotation_x(min, max)

    def limit_rotation_y(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_rotation_y(min, max)

    def limit_rotation_z(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:
        return object.__getattribute__(self, "__proxied").limit_rotation_z(min, max)
