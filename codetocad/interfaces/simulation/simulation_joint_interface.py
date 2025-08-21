"""
Interface for joints and constraints in physics simulation.

This interface defines the functionality for joints that connect rigid bodies
in physics simulations, including different joint types like revolute,
prismatic, fixed, and spherical joints.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.simulation.simulation_body_interface import (
        SimulationBodyInterface,
    )


class JointType(Enum):
    """Enumeration of joint types."""

    FIXED = "fixed"
    REVOLUTE = "revolute"
    PRISMATIC = "prismatic"
    SPHERICAL = "spherical"
    CYLINDRICAL = "cylindrical"
    PLANAR = "planar"
    UNIVERSAL = "universal"
    POINT_TO_POINT = "point_to_point"


class SimulationJointInterface(ABC):
    """
    Base interface for joints in physics simulation.

    This interface provides methods for creating and managing joints
    that constrain the motion between rigid bodies.
    """

    def __init__(self):
        """Initialize the simulation joint interface."""
        self.name: str | None = None
        self.joint_type: JointType = JointType.FIXED
        self.parent_body: "SimulationBodyInterface | None" = None
        self.child_body: "SimulationBodyInterface | None" = None
        self.is_enabled: bool = True

    def set_name(self, name: str):
        """Set the joint name."""
        self.name = name

    @abstractmethod
    def create_fixed_joint(
        self,
        parent_body: "SimulationBodyInterface",
        child_body: "SimulationBodyInterface",
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """
        Create a fixed joint between two bodies.

        Args:
            parent_body: The parent body
            child_body: The child body
            parent_frame: Connection point on parent body
            child_frame: Connection point on child body
            **kwargs: Additional joint parameters
        """
        ...

    @abstractmethod
    def create_revolute_joint(
        self,
        parent_body: "SimulationBodyInterface",
        child_body: "SimulationBodyInterface",
        axis: Point | tuple[float, float, float],
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        lower_limit: float | None = None,
        upper_limit: float | None = None,
        **kwargs,
    ) -> None:
        """
        Create a revolute (hinge) joint between two bodies.

        Args:
            parent_body: The parent body
            child_body: The child body
            axis: Rotation axis as Point or (x, y, z) tuple
            parent_frame: Connection point on parent body
            child_frame: Connection point on child body
            lower_limit: Lower rotation limit in radians
            upper_limit: Upper rotation limit in radians
            **kwargs: Additional joint parameters
        """
        ...

    @abstractmethod
    def create_prismatic_joint(
        self,
        parent_body: "SimulationBodyInterface",
        child_body: "SimulationBodyInterface",
        axis: Point | tuple[float, float, float],
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        lower_limit: float | None = None,
        upper_limit: float | None = None,
        **kwargs,
    ) -> None:
        """
        Create a prismatic (sliding) joint between two bodies.

        Args:
            parent_body: The parent body
            child_body: The child body
            axis: Translation axis as Point or (x, y, z) tuple
            parent_frame: Connection point on parent body
            child_frame: Connection point on child body
            lower_limit: Lower translation limit in meters
            upper_limit: Upper translation limit in meters
            **kwargs: Additional joint parameters
        """
        ...

    @abstractmethod
    def create_spherical_joint(
        self,
        parent_body: "SimulationBodyInterface",
        child_body: "SimulationBodyInterface",
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """
        Create a spherical (ball) joint between two bodies.

        Args:
            parent_body: The parent body
            child_body: The child body
            parent_frame: Connection point on parent body
            child_frame: Connection point on child body
            **kwargs: Additional joint parameters
        """
        ...

    @abstractmethod
    def get_position(self) -> float:
        """
        Get the current joint position.

        Returns:
            Joint position (angle for revolute, distance for prismatic)
        """
        ...

    @abstractmethod
    def set_position(self, position: float) -> None:
        """
        Set the joint position.

        Args:
            position: Target position (angle for revolute, distance for prismatic)
        """
        ...

    @abstractmethod
    def get_velocity(self) -> float:
        """
        Get the current joint velocity.

        Returns:
            Joint velocity (angular for revolute, linear for prismatic)
        """
        ...

    @abstractmethod
    def set_velocity(self, velocity: float) -> None:
        """
        Set the joint velocity.

        Args:
            velocity: Target velocity (angular for revolute, linear for prismatic)
        """
        ...

    @abstractmethod
    def apply_force(self, force: float) -> None:
        """
        Apply a force/torque to the joint.

        Args:
            force: Force (torque for revolute, force for prismatic)
        """
        ...

    @abstractmethod
    def set_limits(self, lower: float | None, upper: float | None) -> None:
        """
        Set joint limits.

        Args:
            lower: Lower limit (None for no limit)
            upper: Upper limit (None for no limit)
        """
        ...

    @abstractmethod
    def get_limits(self) -> tuple[float | None, float | None]:
        """
        Get joint limits.

        Returns:
            Tuple of (lower_limit, upper_limit)
        """
        ...

    @abstractmethod
    def set_stiffness(self, stiffness: float) -> None:
        """
        Set joint stiffness.

        Args:
            stiffness: Joint stiffness value
        """
        ...

    @abstractmethod
    def set_damping(self, damping: float) -> None:
        """
        Set joint damping.

        Args:
            damping: Joint damping value
        """
        ...

    @abstractmethod
    def enable(self) -> None:
        """Enable the joint."""
        ...

    @abstractmethod
    def disable(self) -> None:
        """Disable the joint."""
        ...

    @abstractmethod
    def remove(self) -> None:
        """Remove the joint from the simulation."""
        ...

    def get_parent_body(self) -> "SimulationBodyInterface | None":
        """Get the parent body."""
        return self.parent_body

    def get_child_body(self) -> "SimulationBodyInterface | None":
        """Get the child body."""
        return self.child_body

    def get_joint_type(self) -> JointType:
        """Get the joint type."""
        return self.joint_type

    def is_joint_enabled(self) -> bool:
        """Check if the joint is enabled."""
        return self.is_enabled

    def __repr__(self) -> str:
        return f"<SimulationJoint: {self.name or 'Unnamed'}, Type: {self.joint_type.value}>"
