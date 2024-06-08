# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.joint_interface import JointInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Joint(
    JointInterface,
):

    def __init__(self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"):

        self.entity1 = entity1
        self.entity2 = entity2

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_landmark_onto_another(
        self,
    ) -> Self:

        print(
            "translate_landmark_onto_another called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def pivot(
        self,
    ) -> Self:

        print(
            "pivot called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def gear_ratio(self, ratio: "float") -> Self:

        print("gear_ratio called", f": {ratio}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_xyz(
        self,
        x: "str|float|Dimension| None" = None,
        y: "str|float|Dimension| None" = None,
        z: "str|float|Dimension| None" = None,
    ) -> Self:

        print("limit_location_xyz called", f": {x}, {y}, {z}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_x(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:

        print("limit_location_x called", f": {min}, {max}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_y(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:

        print("limit_location_y called", f": {min}, {max}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_z(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:

        print("limit_location_z called", f": {min}, {max}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_xyz(
        self,
        x: "str|float|Angle| None" = None,
        y: "str|float|Angle| None" = None,
        z: "str|float|Angle| None" = None,
    ) -> Self:

        print("limit_rotation_xyz called", f": {x}, {y}, {z}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_x(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:

        print("limit_rotation_x called", f": {min}, {max}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_y(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:

        print("limit_rotation_y called", f": {min}, {max}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_z(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:

        print("limit_rotation_z called", f": {min}, {max}")

        return self
