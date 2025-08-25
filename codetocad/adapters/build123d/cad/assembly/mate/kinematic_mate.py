"""
build123d implementation of kinematic assembly mates.

This module provides implementations for kinematic mates that wrap
build123d's joint system for motion-based constraints.
"""

from typing import TYPE_CHECKING, Any, Tuple

from codetocad.interfaces.cad.assembly.mate.kinematic_mate_interface import (
    KinematicMateInterface,
    RigidMateInterface,
    RevoluteMateInterface,
    LinearMateInterface,
    CylindricalMateInterface,
    BallMateInterface,
)
from codetocad.interfaces.cad.assembly.mate.mate_interface import MateType, MateStatus

from codetocad.adapters.build123d.cad.assembly.mate.mate import Mate

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.part.part import Part
    import build123d as bd


class KinematicMate(Mate, KinematicMateInterface):
    """
    build123d implementation of KinematicMateInterface.

    Base class for all kinematic mates that use build123d's joint system.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """
        Initialize a kinematic mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of kinematic mate
            part1: First part (typically fixed)
            part2: Second part (typically moving)
            **kwargs: Additional mate-specific parameters
        """
        super().__init__(name, mate_type, part1, part2, **kwargs)

    def _apply_constraint(self) -> bool:
        """
        Apply the kinematic constraint using build123d joints.

        Returns:
            True if constraint was applied successfully, False otherwise
        """
        try:
            # Create the appropriate build123d joint
            joint = self._create_build123d_joint()
            if joint:
                self.set_native_joint(joint)
                return True
            return False
        except Exception as e:
            print(f"Error creating build123d joint for mate {self.name}: {e}")
            return False

    def _remove_constraint(self) -> bool:
        """
        Remove the kinematic constraint.

        Returns:
            True if constraint was removed successfully, False otherwise
        """
        try:
            # Remove the joint connection
            if self._native_joint:
                # In build123d, joints are typically managed by the parts themselves
                # So we don't need to explicitly remove them, just clear our reference
                self._native_joint = None
            return True
        except Exception as e:
            print(f"Error removing build123d joint for mate {self.name}: {e}")
            return False

    def _create_build123d_joint(self) -> Any | None:
        """
        Create the appropriate build123d joint for this mate type.

        This method should be overridden by subclasses.

        Returns:
            build123d joint instance or None if creation failed
        """
        return None


class RigidMate(KinematicMate, RigidMateInterface):
    """
    build123d implementation of RigidMateInterface.

    Uses build123d's RigidJoint to fix two parts together.
    """

    def __init__(
        self,
        name: str,
        part1: "Part",
        part2: "Part",
        location1: Any = None,
        location2: Any = None,
        location: Any = None,  # Backward compatibility
        **kwargs,
    ):
        """
        Initialize a rigid mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (to be positioned)
            location1: Location/orientation on part1
            location2: Location/orientation on part2
            location: Legacy parameter for backward compatibility
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.RIGID, part1, part2, **kwargs)
        self.location1 = location1
        self.location2 = location2
        self.location = location or location1  # Backward compatibility

    def _create_build123d_joint(self) -> Any | None:
        """
        Create a build123d RigidJoint.

        Returns:
            RigidJoint instance or None if creation failed
        """
        try:
            # For now, we'll create a placeholder joint without requiring build123d native instances
            # In a full implementation, this would create actual build123d joints

            # Create a simple joint representation
            joint_info = {
                "type": "rigid",
                "part1": self.part1.name,
                "part2": self.part2.name,
                "location1": self.location1,
                "location2": self.location2,
                "location": self.location,  # Backward compatibility
            }

            # Store joint info on parts
            if not hasattr(self.part1, "joints"):
                self.part1.joints = {}
            if not hasattr(self.part2, "joints"):
                self.part2.joints = {}

            self.part1.joints[f"{self.name}_part1"] = joint_info
            self.part2.joints[f"{self.name}_part2"] = joint_info

            return joint_info

        except Exception as e:
            print(f"Error creating RigidJoint: {e}")
            return None

    def set_position(self, **kwargs) -> bool:
        """
        Set the position (rigid mates have no degrees of freedom).

        Returns:
            False (rigid mates cannot be repositioned)
        """
        return False

    def get_position(self) -> dict:
        """
        Get the current position (always empty for rigid mates).

        Returns:
            Empty dictionary
        """
        return {}


class RevoluteMate(KinematicMate, RevoluteMateInterface):
    """
    build123d implementation of RevoluteMateInterface.

    Uses build123d's RevoluteJoint for hinge-like motion.
    """

    def __init__(
        self,
        name: str,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any = None,
        location2: Any = None,
        angle_range: tuple[float, float] = (0, 360),
        current_angle: float = 0,
        **kwargs,
    ):
        """
        Initialize a revolute mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (rotating)
            axis: Axis of rotation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            angle_range: (min, max) angle limits in degrees
            current_angle: Current angle in degrees
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.REVOLUTE, part1, part2, **kwargs)
        self.axis = axis
        self.location1 = location1
        self.location2 = location2
        self.angle_range = angle_range
        self.current_angle = current_angle

    def _create_build123d_joint(self) -> Any | None:
        """
        Create a build123d RevoluteJoint.

        Returns:
            RevoluteJoint instance or None if creation failed
        """
        try:
            import build123d as bd

            # Create a revolute joint on part2 (the moving part)
            joint = bd.RevoluteJoint(
                label=f"{self.name}_revolute",
                to_part=self.part2.native_instance,
                axis=self.axis,
                angular_range=self.angle_range,
            )

            if not hasattr(self.part2, "joints"):
                self.part2.joints = {}
            self.part2.joints[f"{self.name}_revolute"] = joint

            # Create a rigid joint on part1 to connect to
            rigid_joint = bd.RigidJoint(
                label=f"{self.name}_fixed",
                to_part=self.part1.native_instance,
                joint_location=bd.Location(),
            )

            if not hasattr(self.part1, "joints"):
                self.part1.joints = {}
            self.part1.joints[f"{self.name}_fixed"] = rigid_joint

            # Connect the joints
            rigid_joint.connect_to(joint, angle=self.current_angle)

            return joint
        except Exception as e:
            print(f"Error creating RevoluteJoint: {e}")
            return None

    def set_position(self, **kwargs) -> bool:
        """
        Set the rotation angle.

        Args:
            **kwargs: Should contain 'angle' parameter

        Returns:
            True if angle was set successfully, False otherwise
        """
        angle = kwargs.get("angle")
        if angle is not None:
            return self.set_angle(angle)
        return False

    def get_position(self) -> dict:
        """
        Get the current rotation angle.

        Returns:
            Dictionary with current angle
        """
        return {"angle": self.current_angle}

    def set_angle(self, angle: float) -> bool:
        """
        Set the rotation angle.

        Args:
            angle: Angle in degrees

        Returns:
            True if angle was set successfully, False otherwise
        """
        try:
            if self.angle_range[0] <= angle <= self.angle_range[1]:
                self.current_angle = angle

                # Update the joint if it exists
                if self._native_joint and hasattr(self.part1, "joints"):
                    joint1_key = f"{self.name}_fixed"
                    if joint1_key in self.part1.joints:
                        self.part1.joints[joint1_key].connect_to(
                            self._native_joint, angle=angle
                        )

                return True
            else:
                print(f"Angle {angle} is outside range {self.angle_range}")
                return False
        except Exception as e:
            print(f"Error setting angle: {e}")
            return False


class LinearMate(KinematicMate, LinearMateInterface):
    """
    build123d implementation of LinearMateInterface.

    Uses build123d's LinearJoint for sliding motion.
    """

    def __init__(
        self,
        name: str,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any = None,
        location2: Any = None,
        position_range: tuple[float, float] = (0, float("inf")),
        current_position: float = 0,
        **kwargs,
    ):
        """
        Initialize a linear mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (sliding)
            axis: Axis of translation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            position_range: (min, max) position limits
            current_position: Current position along axis
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.LINEAR, part1, part2, **kwargs)
        self.axis = axis
        self.location1 = location1
        self.location2 = location2
        self.position_range = position_range
        self.current_position = current_position

    def _create_build123d_joint(self) -> Any | None:
        """
        Create a build123d LinearJoint.

        Returns:
            LinearJoint instance or None if creation failed
        """
        try:
            import build123d as bd

            # Create a linear joint on part2 (the moving part)
            joint = bd.LinearJoint(
                label=f"{self.name}_linear",
                to_part=self.part2.native_instance,
                axis=self.axis,
                linear_range=self.position_range,
            )

            if not hasattr(self.part2, "joints"):
                self.part2.joints = {}
            self.part2.joints[f"{self.name}_linear"] = joint

            # Create a rigid joint on part1 to connect to
            rigid_joint = bd.RigidJoint(
                label=f"{self.name}_fixed",
                to_part=self.part1.native_instance,
                joint_location=bd.Location(),
            )

            if not hasattr(self.part1, "joints"):
                self.part1.joints = {}
            self.part1.joints[f"{self.name}_fixed"] = rigid_joint

            # Connect the joints
            rigid_joint.connect_to(joint, position=self.current_position)

            return joint
        except Exception as e:
            print(f"Error creating LinearJoint: {e}")
            return None

    def set_position(self, **kwargs) -> bool:
        """
        Set the linear position.

        Args:
            **kwargs: Should contain 'position' parameter

        Returns:
            True if position was set successfully, False otherwise
        """
        position = kwargs.get("position")
        if position is not None:
            return self.set_position_value(position)
        return False

    def get_position(self) -> dict:
        """
        Get the current linear position.

        Returns:
            Dictionary with current position
        """
        return {"position": self.current_position}

    def set_position_value(self, position: float) -> bool:
        """
        Set the linear position.

        Args:
            position: Position along the axis

        Returns:
            True if position was set successfully, False otherwise
        """
        try:
            if self.position_range[0] <= position <= self.position_range[1]:
                self.current_position = position

                # Update the joint if it exists
                if self._native_joint and hasattr(self.part1, "joints"):
                    joint1_key = f"{self.name}_fixed"
                    if joint1_key in self.part1.joints:
                        self.part1.joints[joint1_key].connect_to(
                            self._native_joint, position=position
                        )

                return True
            else:
                print(f"Position {position} is outside range {self.position_range}")
                return False
        except Exception as e:
            print(f"Error setting position: {e}")
            return False


class CylindricalMate(KinematicMate, CylindricalMateInterface):
    """
    build123d implementation of CylindricalMateInterface.

    Uses build123d's CylindricalJoint for screw-like motion.
    """

    def __init__(
        self,
        name: str,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any = None,
        location2: Any = None,
        position_range: tuple[float, float] = (0, float("inf")),
        angle_range: tuple[float, float] = (0, 360),
        current_position: float = 0,
        current_angle: float = 0,
        **kwargs,
    ):
        """
        Initialize a cylindrical mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (moving)
            axis: Axis of rotation and translation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            position_range: (min, max) position limits
            angle_range: (min, max) angle limits in degrees
            current_position: Current position along axis
            current_angle: Current angle in degrees
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.CYLINDRICAL, part1, part2, **kwargs)
        self.axis = axis
        self.location1 = location1
        self.location2 = location2
        self.position_range = position_range
        self.angle_range = angle_range
        self.current_position = current_position
        self.current_angle = current_angle

    def _create_build123d_joint(self) -> Any | None:
        """
        Create a build123d CylindricalJoint.

        Returns:
            CylindricalJoint instance or None if creation failed
        """
        try:
            import build123d as bd

            # Create a cylindrical joint on part2 (the moving part)
            joint = bd.CylindricalJoint(
                label=f"{self.name}_cylindrical",
                to_part=self.part2.native_instance,
                axis=self.axis,
                linear_range=self.position_range,
                angular_range=self.angle_range,
            )

            if not hasattr(self.part2, "joints"):
                self.part2.joints = {}
            self.part2.joints[f"{self.name}_cylindrical"] = joint

            # Create a rigid joint on part1 to connect to
            rigid_joint = bd.RigidJoint(
                label=f"{self.name}_fixed",
                to_part=self.part1.native_instance,
                joint_location=bd.Location(),
            )

            if not hasattr(self.part1, "joints"):
                self.part1.joints = {}
            self.part1.joints[f"{self.name}_fixed"] = rigid_joint

            # Connect the joints
            rigid_joint.connect_to(
                joint, position=self.current_position, angle=self.current_angle
            )

            return joint
        except Exception as e:
            print(f"Error creating CylindricalJoint: {e}")
            return None

    def set_position(self, **kwargs) -> bool:
        """
        Set the position and/or angle.

        Args:
            **kwargs: Should contain 'position' and/or 'angle' parameters

        Returns:
            True if parameters were set successfully, False otherwise
        """
        position = kwargs.get("position")
        angle = kwargs.get("angle")

        if position is not None and angle is not None:
            return self.set_position_and_angle(position, angle)
        elif position is not None:
            return self.set_position_and_angle(position, self.current_angle)
        elif angle is not None:
            return self.set_position_and_angle(self.current_position, angle)

        return False

    def get_position(self) -> dict:
        """
        Get the current position and angle.

        Returns:
            Dictionary with current position and angle
        """
        return {"position": self.current_position, "angle": self.current_angle}

    def set_position_and_angle(self, position: float, angle: float) -> bool:
        """
        Set both position and angle.

        Args:
            position: Position along the axis
            angle: Angle in degrees

        Returns:
            True if both were set successfully, False otherwise
        """
        try:
            if (
                self.position_range[0] <= position <= self.position_range[1]
                and self.angle_range[0] <= angle <= self.angle_range[1]
            ):

                self.current_position = position
                self.current_angle = angle

                # Update the joint if it exists
                if self._native_joint and hasattr(self.part1, "joints"):
                    joint1_key = f"{self.name}_fixed"
                    if joint1_key in self.part1.joints:
                        self.part1.joints[joint1_key].connect_to(
                            self._native_joint, position=position, angle=angle
                        )

                return True
            else:
                print(f"Position {position} or angle {angle} is outside allowed ranges")
                return False
        except Exception as e:
            print(f"Error setting position and angle: {e}")
            return False


class BallMate(KinematicMate, BallMateInterface):
    """
    build123d implementation of BallMateInterface.

    Uses build123d's BallJoint for gimbal-like motion.
    """

    def __init__(
        self,
        name: str,
        part1: "Part",
        part2: "Part",
        center_point: Any,
        location1: Any = None,
        location2: Any = None,
        angle_ranges: tuple[
            tuple[float, float], tuple[float, float], tuple[float, float]
        ] = ((0, 360), (0, 360), (0, 360)),
        current_angles: tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ):
        """
        Initialize a ball mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (rotating)
            center_point: Center point of rotation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            angle_ranges: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) angle limits
            current_angles: (x, y, z) current angles in degrees
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.BALL, part1, part2, **kwargs)
        self.center_point = center_point
        self.location1 = location1
        self.location2 = location2
        self.angle_ranges = angle_ranges
        self.current_angles = current_angles

    def _create_build123d_joint(self) -> Any | None:
        """
        Create a build123d BallJoint.

        Returns:
            BallJoint instance or None if creation failed
        """
        try:
            import build123d as bd

            # Create a ball joint on part2 (the moving part)
            joint = bd.BallJoint(
                label=f"{self.name}_ball",
                to_part=self.part2.native_instance,
                joint_location=self.center_point,
                angular_range=self.angle_ranges,
            )

            if not hasattr(self.part2, "joints"):
                self.part2.joints = {}
            self.part2.joints[f"{self.name}_ball"] = joint

            # Create a rigid joint on part1 to connect to
            rigid_joint = bd.RigidJoint(
                label=f"{self.name}_fixed",
                to_part=self.part1.native_instance,
                joint_location=self.center_point,
            )

            if not hasattr(self.part1, "joints"):
                self.part1.joints = {}
            self.part1.joints[f"{self.name}_fixed"] = rigid_joint

            # Connect the joints
            rigid_joint.connect_to(joint, angles=self.current_angles)

            return joint
        except Exception as e:
            print(f"Error creating BallJoint: {e}")
            return None

    def set_position(self, **kwargs) -> bool:
        """
        Set the rotation angles.

        Args:
            **kwargs: Should contain 'angles' parameter as tuple of (x, y, z) angles

        Returns:
            True if angles were set successfully, False otherwise
        """
        angles = kwargs.get("angles")
        if angles is not None and len(angles) == 3:
            return self.set_angles(angles[0], angles[1], angles[2])
        return False

    def get_position(self) -> dict:
        """
        Get the current rotation angles.

        Returns:
            Dictionary with current angles
        """
        return {"angles": self.current_angles}

    def set_angles(self, x_angle: float, y_angle: float, z_angle: float) -> bool:
        """
        Set the rotation angles around all three axes.

        Args:
            x_angle: Rotation around X axis in degrees
            y_angle: Rotation around Y axis in degrees
            z_angle: Rotation around Z axis in degrees

        Returns:
            True if angles were set successfully, False otherwise
        """
        try:
            # Check if angles are within allowed ranges
            if (
                self.angle_ranges[0][0] <= x_angle <= self.angle_ranges[0][1]
                and self.angle_ranges[1][0] <= y_angle <= self.angle_ranges[1][1]
                and self.angle_ranges[2][0] <= z_angle <= self.angle_ranges[2][1]
            ):

                self.current_angles = (x_angle, y_angle, z_angle)

                # Update the joint if it exists
                if self._native_joint and hasattr(self.part1, "joints"):
                    joint1_key = f"{self.name}_fixed"
                    if joint1_key in self.part1.joints:
                        self.part1.joints[joint1_key].connect_to(
                            self._native_joint, angles=self.current_angles
                        )

                return True
            else:
                print(
                    f"Angles {(x_angle, y_angle, z_angle)} are outside allowed ranges"
                )
                return False
        except Exception as e:
            print(f"Error setting angles: {e}")
            return False
