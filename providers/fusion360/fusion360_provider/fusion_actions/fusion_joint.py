from codetocad import *
from .base import get_root_component

import adsk.fusion


class FusionJoint:
    def __init__(self, entity_1: str | Entity, entity_2: str | Entity):
        self.entity_1 = entity_1
        self.entity_2 = entity_2
        self.joint_slider = None
        self.joint_ball_motion = None

    def limit_rotation_motion(self, axis: str, min: float, max: float):
        if self.joint_ball_motion is None:
            self.joint_ball_motion = self._make_ball_joint_motion()
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
        if self.joint_slider:
            return

        geoEntity1 = adsk.fusion.JointGeometry.createByPoint(
            self.entity_1.fusion_landmark.point
        )
        geoEntity2 = adsk.fusion.JointGeometry.createByPoint(
            self.entity_2.fusion_landmark.point
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
            adsk.fusion.JointDirections.XAxisJointDirection,
        )
        joint = joints.add(jointInput)

        return joint

    def limit_location(self, axis: str, min: float, max: float):
        if self.joint_ball_motion:
            return

        match axis:
            case "x":
                direction = adsk.fusion.JointDirections.XAxisJointDirection
            case "y":
                direction = adsk.fusion.JointDirections.YAxisJointDirection
            case "z":
                direction = adsk.fusion.JointDirections.ZAxisJointDirection

        if self.joint_slider is None:
            geoEntity1 = adsk.fusion.JointGeometry.createByPoint(
                self.entity_1.fusion_landmark.point
            )
            geoEntity2 = adsk.fusion.JointGeometry.createByPoint(
                self.entity_2.fusion_landmark.point
            )

            angle = adsk.core.ValueInput.createByReal(0)
            offset = adsk.core.ValueInput.createByReal(0)

            rootComp = get_root_component()
            joints = rootComp.joints
            jointInput = joints.createInput(geoEntity2, geoEntity1)
            jointInput.angle = angle
            jointInput.offset = offset
            jointInput.setAsSliderJointMotion(direction)
            joint = joints.add(jointInput)

            self.joint_slider = joint

        sliderMotion = self.joint_slider.jointMotion
        limits = sliderMotion.slideLimits
        limits.isMinimumValueEnabled = True
        limits.minimumValue = min
        limits.isMaximumValueEnabled = True
        limits.maximumValue = max
