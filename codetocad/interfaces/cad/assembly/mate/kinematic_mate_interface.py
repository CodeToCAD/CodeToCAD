"""
Interface for kinematic assembly mates.

Kinematic mates define motion relationships between parts, such as revolute joints,
linear slides, or ball joints. These mates allow controlled motion with specific
degrees of freedom.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

from codetocad.interfaces.cad.assembly.mate.mate_interface import (
    MateInterface,
    MateType,
)

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class KinematicMateInterface(MateInterface):
    """
    Base interface for kinematic assembly mates.

    Kinematic mates define motion relationships between parts,
    allowing specific degrees of freedom while constraining others.
    """

    def __init__(
        self,
        name: str,
        mate_type: MateType,
        part1: "PartInterface",
        part2: "PartInterface",
        **kwargs,
    ):
        """
        Initialize a kinematic mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of kinematic mate
            part1: First part in the mate relationship (typically fixed)
            part2: Second part in the mate relationship (typically moving)
            **kwargs: Additional mate-specific parameters
        """
        super().__init__(name, mate_type, part1, part2, **kwargs)

    @abstractmethod
    def get_degrees_of_freedom(self) -> int:
        """
        Get the number of degrees of freedom this mate allows.

        Returns:
            Number of degrees of freedom (0-6)
        """
        pass

    @abstractmethod
    def set_position(self, **kwargs) -> bool:
        """
        Set the position/orientation of the moving part.

        Args:
            **kwargs: Position parameters (specific to mate type)

        Returns:
            True if position was set successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_position(self) -> dict:
        """
        Get the current position/orientation of the moving part.

        Returns:
            Dictionary of current position parameters
        """
        pass


class RigidMateInterface(KinematicMateInterface):
    """
    Interface for rigid mates.

    Rigid mates fix two parts together with no degrees of freedom.
    This is equivalent to a fixed joint.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        location: Any = None,
        **kwargs,
    ):
        """
        Initialize a rigid mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (to be positioned)
            location: Location/orientation for the connection
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.RIGID, part1, part2, **kwargs)
        self.location = location

    def get_degrees_of_freedom(self) -> int:
        """Rigid mates have 0 degrees of freedom."""
        return 0


class RevoluteMateInterface(KinematicMateInterface):
    """
    Interface for revolute mates.

    Revolute mates allow rotation around a single axis, like a hinge.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        axis: Any,
        angle_range: Tuple[float, float] = (0, 360),
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
            angle_range: (min, max) angle limits in degrees
            current_angle: Current angle in degrees
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.REVOLUTE, part1, part2, **kwargs)
        self.axis = axis
        self.angle_range = angle_range
        self.current_angle = current_angle

    def get_degrees_of_freedom(self) -> int:
        """Revolute mates have 1 degree of freedom (rotation)."""
        return 1

    def set_angle(self, angle: float) -> bool:
        """
        Set the rotation angle.

        Args:
            angle: Angle in degrees

        Returns:
            True if angle was set successfully, False otherwise
        """
        return self.set_position(angle=angle)

    def get_angle(self) -> float:
        """
        Get the current rotation angle.

        Returns:
            Current angle in degrees
        """
        return self.current_angle


class LinearMateInterface(KinematicMateInterface):
    """
    Interface for linear mates.

    Linear mates allow translation along a single axis, like a slider.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        axis: Any,
        position_range: Tuple[float, float] = (0, float("inf")),
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
            position_range: (min, max) position limits
            current_position: Current position along axis
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.LINEAR, part1, part2, **kwargs)
        self.axis = axis
        self.position_range = position_range
        self.current_position = current_position

    def get_degrees_of_freedom(self) -> int:
        """Linear mates have 1 degree of freedom (translation)."""
        return 1

    def set_position_value(self, position: float) -> bool:
        """
        Set the linear position.

        Args:
            position: Position along the axis

        Returns:
            True if position was set successfully, False otherwise
        """
        return self.set_position(position=position)

    def get_position_value(self) -> float:
        """
        Get the current linear position.

        Returns:
            Current position along the axis
        """
        return self.current_position


class CylindricalMateInterface(KinematicMateInterface):
    """
    Interface for cylindrical mates.

    Cylindrical mates allow both rotation around and translation along a single axis,
    like a screw or bolt.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        axis: Any,
        position_range: Tuple[float, float] = (0, float("inf")),
        angle_range: Tuple[float, float] = (0, 360),
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
            position_range: (min, max) position limits
            angle_range: (min, max) angle limits in degrees
            current_position: Current position along axis
            current_angle: Current angle in degrees
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.CYLINDRICAL, part1, part2, **kwargs)
        self.axis = axis
        self.position_range = position_range
        self.angle_range = angle_range
        self.current_position = current_position
        self.current_angle = current_angle

    def get_degrees_of_freedom(self) -> int:
        """Cylindrical mates have 2 degrees of freedom (rotation + translation)."""
        return 2

    def set_position_and_angle(self, position: float, angle: float) -> bool:
        """
        Set both position and angle.

        Args:
            position: Position along the axis
            angle: Angle in degrees

        Returns:
            True if both were set successfully, False otherwise
        """
        return self.set_position(position=position, angle=angle)


class BallMateInterface(KinematicMateInterface):
    """
    Interface for ball mates.

    Ball mates allow rotation around all three axes, like a ball joint or gimbal.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        center_point: Any,
        angle_ranges: Tuple[
            Tuple[float, float], Tuple[float, float], Tuple[float, float]
        ] = ((0, 360), (0, 360), (0, 360)),
        current_angles: Tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ):
        """
        Initialize a ball mate.

        Args:
            name: Unique name for this mate
            part1: First part (fixed)
            part2: Second part (rotating)
            center_point: Center point of rotation
            angle_ranges: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) angle limits
            current_angles: (x, y, z) current angles in degrees
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.BALL, part1, part2, **kwargs)
        self.center_point = center_point
        self.angle_ranges = angle_ranges
        self.current_angles = current_angles

    def get_degrees_of_freedom(self) -> int:
        """Ball mates have 3 degrees of freedom (rotation around 3 axes)."""
        return 3

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
        return self.set_position(angles=(x_angle, y_angle, z_angle))
