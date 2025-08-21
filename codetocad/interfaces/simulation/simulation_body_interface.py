"""
Interface for rigid bodies in physics simulation.

This interface defines the functionality for rigid bodies that can be
simulated in physics engines, including properties like mass, inertia,
position, velocity, and forces.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.simulation.simulation_joint_interface import (
        SimulationJointInterface,
    )
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class SimulationBodyInterface(ABC):
    """
    Base interface for rigid bodies in physics simulation.

    This interface provides methods for managing rigid body properties,
    applying forces and torques, and querying body state.
    """

    def __init__(self):
        """Initialize the simulation body interface."""
        self.name: str | None = None
        self.mass: float = 1.0
        self.is_static: bool = False
        self.is_kinematic: bool = False
        self.joints: list["SimulationJointInterface"] = []
        self.original_part: "PartInterface | None" = None

    def set_name(self, name: str):
        """Set the body name."""
        self.name = name

    @abstractmethod
    def get_position(self) -> Point:
        """
        Get the current position of the body.

        Returns:
            Current position as Point
        """
        ...

    @abstractmethod
    def set_position(self, position: Point | tuple[float, float, float]) -> None:
        """
        Set the position of the body.

        Args:
            position: New position as Point or (x, y, z) tuple
        """
        ...

    @abstractmethod
    def get_orientation(self) -> tuple[float, float, float, float]:
        """
        Get the current orientation of the body.

        Returns:
            Orientation as quaternion (x, y, z, w)
        """
        ...

    @abstractmethod
    def set_orientation(self, orientation: tuple[float, float, float, float]) -> None:
        """
        Set the orientation of the body.

        Args:
            orientation: New orientation as quaternion (x, y, z, w)
        """
        ...

    @abstractmethod
    def get_linear_velocity(self) -> Point:
        """
        Get the current linear velocity of the body.

        Returns:
            Linear velocity as Point
        """
        ...

    @abstractmethod
    def set_linear_velocity(self, velocity: Point | tuple[float, float, float]) -> None:
        """
        Set the linear velocity of the body.

        Args:
            velocity: New linear velocity as Point or (x, y, z) tuple
        """
        ...

    @abstractmethod
    def get_angular_velocity(self) -> Point:
        """
        Get the current angular velocity of the body.

        Returns:
            Angular velocity as Point
        """
        ...

    @abstractmethod
    def set_angular_velocity(
        self, velocity: Point | tuple[float, float, float]
    ) -> None:
        """
        Set the angular velocity of the body.

        Args:
            velocity: New angular velocity as Point or (x, y, z) tuple
        """
        ...

    @abstractmethod
    def apply_force(
        self,
        force: Point | tuple[float, float, float],
        position: Point | tuple[float, float, float] | None = None,
    ) -> None:
        """
        Apply a force to the body.

        Args:
            force: Force vector as Point or (x, y, z) tuple
            position: Position to apply force (None for center of mass)
        """
        ...

    @abstractmethod
    def apply_torque(self, torque: Point | tuple[float, float, float]) -> None:
        """
        Apply a torque to the body.

        Args:
            torque: Torque vector as Point or (x, y, z) tuple
        """
        ...

    @abstractmethod
    def apply_impulse(
        self,
        impulse: Point | tuple[float, float, float],
        position: Point | tuple[float, float, float] | None = None,
    ) -> None:
        """
        Apply an impulse to the body.

        Args:
            impulse: Impulse vector as Point or (x, y, z) tuple
            position: Position to apply impulse (None for center of mass)
        """
        ...

    @abstractmethod
    def get_mass(self) -> float:
        """
        Get the mass of the body.

        Returns:
            Mass in kg
        """
        ...

    @abstractmethod
    def set_mass(self, mass: float) -> None:
        """
        Set the mass of the body.

        Args:
            mass: New mass in kg
        """
        ...

    @abstractmethod
    def get_inertia(self) -> tuple[float, float, float]:
        """
        Get the inertia tensor diagonal of the body.

        Returns:
            Inertia tensor diagonal (Ixx, Iyy, Izz)
        """
        ...

    @abstractmethod
    def set_inertia(self, inertia: tuple[float, float, float]) -> None:
        """
        Set the inertia tensor diagonal of the body.

        Args:
            inertia: Inertia tensor diagonal (Ixx, Iyy, Izz)
        """
        ...

    @abstractmethod
    def set_friction(self, friction: float) -> None:
        """
        Set the friction coefficient of the body.

        Args:
            friction: Friction coefficient
        """
        ...

    @abstractmethod
    def set_restitution(self, restitution: float) -> None:
        """
        Set the restitution (bounciness) of the body.

        Args:
            restitution: Restitution coefficient (0.0 to 1.0)
        """
        ...

    @abstractmethod
    def set_static(self, is_static: bool) -> None:
        """
        Set whether the body is static (immovable).

        Args:
            is_static: True if body should be static
        """
        ...

    @abstractmethod
    def set_kinematic(self, is_kinematic: bool) -> None:
        """
        Set whether the body is kinematic (position controlled).

        Args:
            is_kinematic: True if body should be kinematic
        """
        ...

    @abstractmethod
    def get_contact_points(self) -> list[dict[str, Any]]:
        """
        Get contact points for this body.

        Returns:
            List of contact point information dictionaries
        """
        ...

    @abstractmethod
    def enable_collision(self, enable: bool = True) -> None:
        """
        Enable or disable collision detection for this body.

        Args:
            enable: True to enable collision detection
        """
        ...

    @abstractmethod
    def remove(self) -> None:
        """Remove this body from the simulation."""
        ...

    def get_joints(self) -> list["SimulationJointInterface"]:
        """Get all joints connected to this body."""
        return self.joints.copy()

    def add_joint(self, joint: "SimulationJointInterface") -> None:
        """Add a joint to this body's joint list."""
        if joint not in self.joints:
            self.joints.append(joint)

    def remove_joint(self, joint: "SimulationJointInterface") -> None:
        """Remove a joint from this body's joint list."""
        if joint in self.joints:
            self.joints.remove(joint)

    def __repr__(self) -> str:
        return f"<SimulationBody: {self.name or 'Unnamed'}, Mass: {self.mass}kg>"
