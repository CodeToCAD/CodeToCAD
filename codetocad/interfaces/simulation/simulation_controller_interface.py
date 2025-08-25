"""
Interface for controllers in physics simulation.

This interface defines the functionality for controllers that can be used
to control robots, mechanisms, and other actuated systems in the simulation,
including PID controllers, trajectory controllers, and force controllers.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.simulation.simulation_body_interface import (
        SimulationBodyInterface,
    )
    from codetocad.interfaces.simulation.simulation_joint_interface import (
        SimulationJointInterface,
    )
    from codetocad.interfaces.simulation.simulation_sensor_interface import (
        SimulationSensorInterface,
    )


class ControllerType(Enum):
    """Enumeration of controller types."""

    PID = "pid"
    POSITION = "position"
    VELOCITY = "velocity"
    FORCE = "force"
    TORQUE = "torque"
    TRAJECTORY = "trajectory"
    IMPEDANCE = "impedance"
    ADMITTANCE = "admittance"


class SimulationControllerInterface(ABC):
    """
    Base interface for controllers in physics simulation.

    This interface provides methods for creating and managing controllers
    that can control the motion and forces of bodies and joints in the simulation.
    """

    def __init__(self):
        """Initialize the simulation controller interface."""
        self.name: str | None = None
        self.controller_type: ControllerType = ControllerType.POSITION
        self.controlled_joints: list["SimulationJointInterface"] = []
        self.controlled_bodies: list["SimulationBodyInterface"] = []
        self.sensors: list["SimulationSensorInterface"] = []
        self.is_enabled: bool = True
        self.update_rate: float = 240.0  # Hz

    def set_name(self, name: str):
        """Set the controller name."""
        self.name = name

    @abstractmethod
    def create_pid_controller(
        self,
        joint: "SimulationJointInterface",
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        **kwargs,
    ) -> None:
        """
        Create a PID controller for a joint.

        Args:
            joint: The joint to control
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            **kwargs: Additional controller parameters
        """
        ...

    @abstractmethod
    def create_position_controller(
        self, joint: "SimulationJointInterface", max_force: float = 1000.0, **kwargs
    ) -> None:
        """
        Create a position controller for a joint.

        Args:
            joint: The joint to control
            max_force: Maximum force/torque to apply
            **kwargs: Additional controller parameters
        """
        ...

    @abstractmethod
    def create_velocity_controller(
        self, joint: "SimulationJointInterface", max_force: float = 1000.0, **kwargs
    ) -> None:
        """
        Create a velocity controller for a joint.

        Args:
            joint: The joint to control
            max_force: Maximum force/torque to apply
            **kwargs: Additional controller parameters
        """
        ...

    @abstractmethod
    def create_force_controller(
        self, joint: "SimulationJointInterface", **kwargs
    ) -> None:
        """
        Create a force controller for a joint.

        Args:
            joint: The joint to control
            **kwargs: Additional controller parameters
        """
        ...

    @abstractmethod
    def create_trajectory_controller(
        self, joints: list["SimulationJointInterface"], **kwargs
    ) -> None:
        """
        Create a trajectory controller for multiple joints.

        Args:
            joints: The joints to control
            **kwargs: Additional controller parameters
        """
        ...

    @abstractmethod
    def set_target_position(self, position: float | list[float]) -> None:
        """
        Set the target position for the controller.

        Args:
            position: Target position (single value or list for multiple joints)
        """
        ...

    @abstractmethod
    def set_target_velocity(self, velocity: float | list[float]) -> None:
        """
        Set the target velocity for the controller.

        Args:
            velocity: Target velocity (single value or list for multiple joints)
        """
        ...

    @abstractmethod
    def set_target_force(self, force: float | list[float]) -> None:
        """
        Set the target force for the controller.

        Args:
            force: Target force (single value or list for multiple joints)
        """
        ...

    @abstractmethod
    def set_trajectory(
        self,
        positions: list[list[float]],
        velocities: list[list[float]] | None = None,
        times: list[float] | None = None,
    ) -> None:
        """
        Set a trajectory for the controller to follow.

        Args:
            positions: List of position waypoints
            velocities: List of velocity waypoints (optional)
            times: List of time points for waypoints (optional)
        """
        ...

    @abstractmethod
    def get_current_position(self) -> float | list[float]:
        """
        Get the current position of controlled joints.

        Returns:
            Current position (single value or list for multiple joints)
        """
        ...

    @abstractmethod
    def get_current_velocity(self) -> float | list[float]:
        """
        Get the current velocity of controlled joints.

        Returns:
            Current velocity (single value or list for multiple joints)
        """
        ...

    @abstractmethod
    def get_current_force(self) -> float | list[float]:
        """
        Get the current force of controlled joints.

        Returns:
            Current force (single value or list for multiple joints)
        """
        ...

    @abstractmethod
    def set_pid_gains(self, kp: float, ki: float, kd: float) -> None:
        """
        Set PID gains for the controller.

        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
        """
        ...

    @abstractmethod
    def get_pid_gains(self) -> tuple[float, float, float]:
        """
        Get PID gains for the controller.

        Returns:
            Tuple of (kp, ki, kd)
        """
        ...

    @abstractmethod
    def set_limits(
        self,
        position_limits: tuple[float, float] | None = None,
        velocity_limits: tuple[float, float] | None = None,
        force_limits: tuple[float, float] | None = None,
    ) -> None:
        """
        Set controller limits.

        Args:
            position_limits: (min, max) position limits
            velocity_limits: (min, max) velocity limits
            force_limits: (min, max) force limits
        """
        ...

    @abstractmethod
    def add_sensor(self, sensor: "SimulationSensorInterface") -> None:
        """
        Add a sensor for feedback control.

        Args:
            sensor: The sensor to add
        """
        ...

    @abstractmethod
    def remove_sensor(self, sensor: "SimulationSensorInterface") -> None:
        """
        Remove a sensor from the controller.

        Args:
            sensor: The sensor to remove
        """
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update the controller (called each simulation step).

        Args:
            dt: Time step in seconds
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the controller state."""
        ...

    @abstractmethod
    def enable(self) -> None:
        """Enable the controller."""
        ...

    @abstractmethod
    def disable(self) -> None:
        """Disable the controller."""
        ...

    @abstractmethod
    def remove(self) -> None:
        """Remove the controller from the simulation."""
        ...

    def get_controller_type(self) -> ControllerType:
        """Get the controller type."""
        return self.controller_type

    def get_controlled_joints(self) -> list["SimulationJointInterface"]:
        """Get the controlled joints."""
        return self.controlled_joints.copy()

    def get_controlled_bodies(self) -> list["SimulationBodyInterface"]:
        """Get the controlled bodies."""
        return self.controlled_bodies.copy()

    def get_sensors(self) -> list["SimulationSensorInterface"]:
        """Get the sensors used by this controller."""
        return self.sensors.copy()

    def is_controller_enabled(self) -> bool:
        """Check if the controller is enabled."""
        return self.is_enabled

    def set_update_rate(self, rate: float) -> None:
        """Set the controller update rate."""
        self.update_rate = rate

    def get_update_rate(self) -> float:
        """Get the controller update rate."""
        return self.update_rate

    def __repr__(self) -> str:
        return f"<SimulationController: {self.name or 'Unnamed'}, Type: {self.controller_type.value}>"
