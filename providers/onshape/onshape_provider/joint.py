from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.interfaces import JointInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Joint(JointInterface):
    entity1: EntityOrItsName
    entity2: EntityOrItsName

    def __init__(self, entity1: "EntityOrItsName", entity2: "EntityOrItsName"):
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
        x: "DimensionOrItsFloatOrStringValue| None" = None,
        y: "DimensionOrItsFloatOrStringValue| None" = None,
        z: "DimensionOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_location_x(
        self,
        min: "DimensionOrItsFloatOrStringValue| None" = None,
        max: "DimensionOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_location_y(
        self,
        min: "DimensionOrItsFloatOrStringValue| None" = None,
        max: "DimensionOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_location_z(
        self,
        min: "DimensionOrItsFloatOrStringValue| None" = None,
        max: "DimensionOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_rotation_xyz(
        self,
        x: "AngleOrItsFloatOrStringValue| None" = None,
        y: "AngleOrItsFloatOrStringValue| None" = None,
        z: "AngleOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_rotation_x(
        self,
        min: "AngleOrItsFloatOrStringValue| None" = None,
        max: "AngleOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_rotation_y(
        self,
        min: "AngleOrItsFloatOrStringValue| None" = None,
        max: "AngleOrItsFloatOrStringValue| None" = None,
    ):
        return self

    def limit_rotation_z(
        self,
        min: "AngleOrItsFloatOrStringValue| None" = None,
        max: "AngleOrItsFloatOrStringValue| None" = None,
    ):
        return self
