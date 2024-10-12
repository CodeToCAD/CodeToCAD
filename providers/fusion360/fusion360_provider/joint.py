from typing import Optional
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.joint_interface import JointInterface
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.fusion_body import FusionBody
from providers.fusion360.fusion360_provider.fusion_actions.fusion_joint import (
    FusionJoint,
)


class Joint(JointInterface):

    def __init__(self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"):
        self.entity1 = entity1
        self.entity2 = entity2

    @property
    def _fusion_joint(self):
        return FusionJoint(FusionBody(entity1), FusionBody(entity2))

    @supported(SupportLevel.PLANNED)
    def translate_landmark_onto_another(self):
        if not isinstance(self.entity1, LandmarkInterface) or not isinstance(
            self.entity2, LandmarkInterface
        ):
            raise TypeError("Entities 1 and 2 should be landmarks.")
        landmark1: LandmarkInterface = self.entity1
        landmark2: LandmarkInterface = self.entity2
        entityForLandmark2 = self.entity2.get_parent_entity()
        translation = landmark1.get_location_world() - landmark2.get_location_world()
        entityForLandmark2.translate_xyz(translation.x, translation.y, translation.z)
        return self

    @supported(SupportLevel.PLANNED)
    def pivot(self):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def gear_ratio(self, ratio: "float"):
        raise NotImplementedError()
        return self

    @staticmethod
    def _get_limit_location_pair(min, max) -> list[Optional[Dimension]]:
        locationPair: list[Optional[Dimension]] = [None, None]
        if min is not None:
            locationPair[0] = Dimension.from_string(min)
        if max is not None:
            locationPair[1] = Dimension.from_string(max)
        return locationPair

    def _limit_location_xyz(
        self,
        x: Optional[str | float | Dimension] = None,
        y: Optional[str | float | Dimension] = None,
        z: Optional[str | float | Dimension] = None,
    ):
        if self.fusion_joint.joint_ball_motion:
            return self
        # offset = self.entity2.get_location_local() * -1
        offset = self.entity2.get_location_local()
        offset.x = offset.x * -1
        offset.y = offset.y * -1
        offset.z = offset.z * -1
        if x and x[0]:
            x[0] += offset.x
        if x and x[1]:
            x[1] += offset.x
        if y and y[0]:
            y[0] += offset.y
        if y and y[1]:
            y[1] += offset.y
        if z and z[0]:
            z[0] += offset.z
        if z and z[1]:
            z[1] += offset.z
        if x:
            self.fusion_joint.limit_location("x", x[0].value, x[1].value)
        elif y:
            self.fusion_joint.limit_location("y", y[0].value, y[1].value)
        elif z:
            self.fusion_joint.limit_location("z", z[0].value, z[1].value)
        return self

    @supported(SupportLevel.PLANNED)
    def limit_location_x(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)
        self._limit_location_xyz(dimensions, None, None)
        return self

    @supported(SupportLevel.PLANNED)
    def limit_location_y(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)
        self._limit_location_xyz(None, dimensions, None)
        return self

    @supported(SupportLevel.PLANNED)
    def limit_location_z(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)
        self._limit_location_xyz(None, None, dimensions)
        return self

    @supported(SupportLevel.PLANNED)
    def limit_location_xyz(
        self,
        x: "str|float|Dimension| None" = None,
        y: "str|float|Dimension| None" = None,
        z: "str|float|Dimension| None" = None,
    ):
        dimensionsX = Joint._get_limit_location_pair(x, x) if x is not None else None
        dimensionsY = Joint._get_limit_location_pair(y, y) if y is not None else None
        dimensionsZ = Joint._get_limit_location_pair(z, z) if y is not None else None
        self._limit_location_xyz(dimensionsX, dimensionsY, dimensionsZ)
        return self

    @staticmethod
    def _get_limit_rotation_pair(min, max) -> list[Optional[Angle]]:
        rotationPair: list[Optional[Angle]] = [None, None]
        if min is not None:
            rotationPair[0] = Angle.from_angle_or_its_float_or_string_value(
                min
            ).to_radians()
        if max is not None:
            rotationPair[1] = Angle.from_angle_or_its_float_or_string_value(
                max
            ).to_radians()
        return rotationPair

    def _limit_rotation_xyz(self, rotation_pair_x, rotation_pair_y, rotation_pair_z):
        if self.fusion_joint.joint_slider:
            return self
        if rotation_pair_x:
            self.fusion_joint.limit_rotation_motion(
                "x", rotation_pair_x[0].value, rotation_pair_x[1].value
            )
        if rotation_pair_y:
            self.fusion_joint.limit_rotation_motion(
                "y", rotation_pair_y[0].value, rotation_pair_y[1].value
            )
        if rotation_pair_z:
            self.fusion_joint.limit_rotation_motion(
                "z", rotation_pair_z[0].value, rotation_pair_z[1].value
            )
        return self

    @supported(SupportLevel.PLANNED)
    def limit_rotation_xyz(
        self,
        x: "str|float|Angle| None" = None,
        y: "str|float|Angle| None" = None,
        z: "str|float|Angle| None" = None,
    ):
        rotation_pair_x = Joint._get_limit_rotation_pair(x, x)
        rotation_pair_y = Joint._get_limit_rotation_pair(y, y)
        rotation_pair_z = Joint._get_limit_rotation_pair(z, z)
        self._limit_rotation_xyz(rotation_pair_x, rotation_pair_y, rotation_pair_z)
        return self

    @supported(SupportLevel.PLANNED)
    def limit_rotation_x(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(rotationPair, None, None)

    @supported(SupportLevel.PLANNED)
    def limit_rotation_y(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(None, rotationPair, None)

    @supported(SupportLevel.PLANNED)
    def limit_rotation_z(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(None, None, rotationPair)
