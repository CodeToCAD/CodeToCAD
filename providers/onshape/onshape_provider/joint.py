from codetocad.interfaces.joint_interface import JointInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *


class Joint(JointInterface):
    entity_1: str | EntityInterface
    entity_2: str | EntityInterface

    def __init__(self, entity_1: "EntityInterface", entity_2: "EntityInterface"):
        self.entity_1 = entity_1
        self.entity_2 = entity_2

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_landmark_onto_another(self):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def pivot(self):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def gear_ratio(self, ratio: "float"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_xyz(
        self,
        x: "str|float|Dimension| None" = None,
        y: "str|float|Dimension| None" = None,
        z: "str|float|Dimension| None" = None,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_x(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_y(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_location_z(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_xyz(
        self,
        x: "str|float|Angle| None" = None,
        y: "str|float|Angle| None" = None,
        z: "str|float|Angle| None" = None,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_x(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_y(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def limit_rotation_z(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        return self
