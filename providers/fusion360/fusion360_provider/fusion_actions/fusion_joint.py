from codetocad import *
from .base import get_root_component

import adsk.fusion


class FusionJoint:
    def __init__(self, entity1: EntityOrItsName, entity2: EntityOrItsName):
        self.entity1 = entity1
        self.entity2 = entity2
        self.joint_slider = None
        self.joint_ball_motion = self._make_ball_joint_motion()

    def limit_rotation_motion(self, axis: str, min: float, max: float):
        ballMotion = self.joint_ball_motion.jointMotion

        # @check if the orientations are correct
        match axis:
            case "x":
                limits = ballMotion.pitchLimits
            case "y":
                limits = ballMotion.yawLimits
            case "z":
                limits = ballMotion.rollLimits

        limits.isMinimumValueEnabled = True
        limits.minimumValue = min
        limits.isMaximumValueEnabled = True
        limits.maximumValue = max

    def _make_ball_joint_motion(self):
        geoEntity1 = adsk.fusion.JointGeometry.createByPoint(
            self.entity1.fusion_landmark.point
        )
        geoEntity2 = adsk.fusion.JointGeometry.createByPoint(
            self.entity2.fusion_landmark.point
        )

        angle = adsk.core.ValueInput.createByReal(0)
        offset = adsk.core.ValueInput.createByReal(0)

        rootComp = get_root_component()
        joints = rootComp.joints
        # First input is who moves and the second is the "origin" point from the move
        jointInput = joints.createInput(geoEntity2, geoEntity1)
        jointInput.angle = angle
        jointInput.offset = offset
        jointInput.setAsBallJointMotion(
            adsk.fusion.JointDirections.ZAxisJointDirection,
            adsk.fusion.JointDirections.XAxisJointDirection
        )
        joint = joints.add(jointInput)

        return joint


    def limit_location(self, axis: str, min: float, max: float):
        # skip if already exists a limit in one axis
        if self.joint_slider is not None:
            return

        match axis:
            case "x":
                direction = adsk.fusion.JointDirections.XAxisJointDirection
            case "y":
                direction = adsk.fusion.JointDirections.YAxisJointDirection
            case "z":
                direction = adsk.fusion.JointDirections.ZAxisJointDirection

        geoEntity1 = adsk.fusion.JointGeometry.createByPoint(
            self.entity1.fusion_landmark.point
        )
        geoEntity2 = adsk.fusion.JointGeometry.createByPoint(
            self.entity2.fusion_landmark.point
        )

        angle = adsk.core.ValueInput.createByReal(0)
        offset = adsk.core.ValueInput.createByReal(0)

        rootComp = get_root_component()
        joints = rootComp.joints
        jointInput = joints.createInput(geoEntity1, geoEntity2)
        jointInput.angle = angle
        jointInput.offset = offset
        jointInput.setAsSliderJointMotion(direction)
        joint = joints.add(jointInput)

        sliderMotion = joint.jointMotion
        limits = sliderMotion.slideLimits
        limits.isMinimumValueEnabled = True
        limits.minimumValue = min
        limits.isMaximumValueEnabled = True
        limits.maximumValue = max

        self.joint_slider = joint

