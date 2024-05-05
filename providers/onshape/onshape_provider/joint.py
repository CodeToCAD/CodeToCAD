from codetocad.interfaces.joint_interface import JointInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.proxy.entity import Entity
from providers.onshape.onshape_provider.entity import Entity
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Joint(JointInterface):
    entity1: str | Entity
    entity2: str | Entity

    def __init__(self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"):
        self.entity1 = entity1
        self.entity2 = entity2

    def translate_landmark_onto_another(self):
        return self

    def pivot(self):
        return self

    def gear_ratio(self, ratio: "float"):
        return self

    def limit_location_xyz(
        self,
        x: "str|float|Dimension| None" = None,
        y: "str|float|Dimension| None" = None,
        z: "str|float|Dimension| None" = None,
    ):
        return self

    def limit_location_x(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        return self

    def limit_location_y(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        return self

    def limit_location_z(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        return self

    def limit_rotation_xyz(
        self,
        x: "str|float|Angle| None" = None,
        y: "str|float|Angle| None" = None,
        z: "str|float|Angle| None" = None,
    ):
        return self

    def limit_rotation_x(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        return self

    def limit_rotation_y(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        return self

    def limit_rotation_z(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        return self
