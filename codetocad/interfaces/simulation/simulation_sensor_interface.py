"""
Interface for sensors in physics simulation.

This interface defines the functionality for various types of sensors
that can be used to gather information from the simulation environment,
such as force sensors, position sensors, and contact sensors.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.simulation.simulation_body_interface import (
        SimulationBodyInterface,
    )
    from codetocad.interfaces.simulation.simulation_joint_interface import (
        SimulationJointInterface,
    )


class SensorType(Enum):
    """Enumeration of sensor types."""

    FORCE = "force"
    TORQUE = "torque"
    POSITION = "position"
    VELOCITY = "velocity"
    ACCELERATION = "acceleration"
    CONTACT = "contact"
    JOINT_POSITION = "joint_position"
    JOINT_VELOCITY = "joint_velocity"
    JOINT_FORCE = "joint_force"
    IMU = "imu"
    CAMERA = "camera"
    LIDAR = "lidar"


class SimulationSensorInterface(ABC):
    """
    Base interface for sensors in physics simulation.

    This interface provides methods for creating and managing sensors
    that can measure various properties of bodies and joints in the simulation.
    """

    def __init__(self):
        """Initialize the simulation sensor interface."""
        self.name: str | None = None
        self.sensor_type: SensorType = SensorType.POSITION
        self.attached_body: "SimulationBodyInterface | None" = None
        self.attached_joint: "SimulationJointInterface | None" = None
        self.is_enabled: bool = True
        self.update_rate: float = 240.0  # Hz

    def set_name(self, name: str):
        """Set the sensor name."""
        self.name = name

    @abstractmethod
    def create_force_sensor(
        self,
        body: "SimulationBodyInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """
        Create a force sensor attached to a body.

        Args:
            body: The body to attach the sensor to
            position: Position on the body to measure force
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def create_torque_sensor(self, body: "SimulationBodyInterface", **kwargs) -> None:
        """
        Create a torque sensor attached to a body.

        Args:
            body: The body to attach the sensor to
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def create_position_sensor(self, body: "SimulationBodyInterface", **kwargs) -> None:
        """
        Create a position sensor attached to a body.

        Args:
            body: The body to attach the sensor to
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def create_velocity_sensor(self, body: "SimulationBodyInterface", **kwargs) -> None:
        """
        Create a velocity sensor attached to a body.

        Args:
            body: The body to attach the sensor to
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def create_contact_sensor(self, body: "SimulationBodyInterface", **kwargs) -> None:
        """
        Create a contact sensor attached to a body.

        Args:
            body: The body to attach the sensor to
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def create_joint_sensor(
        self,
        joint: "SimulationJointInterface",
        sensor_type: SensorType = SensorType.JOINT_POSITION,
        **kwargs,
    ) -> None:
        """
        Create a sensor attached to a joint.

        Args:
            joint: The joint to attach the sensor to
            sensor_type: Type of joint sensor to create
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def create_imu_sensor(
        self,
        body: "SimulationBodyInterface",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """
        Create an IMU (Inertial Measurement Unit) sensor.

        Args:
            body: The body to attach the sensor to
            position: Position on the body for the IMU
            **kwargs: Additional sensor parameters
        """
        ...

    @abstractmethod
    def read_data(self) -> Any:
        """
        Read the current sensor data.

        Returns:
            Sensor data (type depends on sensor type)
        """
        ...

    @abstractmethod
    def read_force(self) -> Point:
        """
        Read force data (for force sensors).

        Returns:
            Force vector as Point
        """
        ...

    @abstractmethod
    def read_torque(self) -> Point:
        """
        Read torque data (for torque sensors).

        Returns:
            Torque vector as Point
        """
        ...

    @abstractmethod
    def read_position(self) -> Point:
        """
        Read position data (for position sensors).

        Returns:
            Position as Point
        """
        ...

    @abstractmethod
    def read_velocity(self) -> Point:
        """
        Read velocity data (for velocity sensors).

        Returns:
            Velocity vector as Point
        """
        ...

    @abstractmethod
    def read_acceleration(self) -> Point:
        """
        Read acceleration data (for acceleration/IMU sensors).

        Returns:
            Acceleration vector as Point
        """
        ...

    @abstractmethod
    def read_angular_velocity(self) -> Point:
        """
        Read angular velocity data (for IMU sensors).

        Returns:
            Angular velocity vector as Point
        """
        ...

    @abstractmethod
    def read_contact_points(self) -> list[dict[str, Any]]:
        """
        Read contact point data (for contact sensors).

        Returns:
            List of contact point information dictionaries
        """
        ...

    @abstractmethod
    def read_joint_position(self) -> float:
        """
        Read joint position data (for joint sensors).

        Returns:
            Joint position value
        """
        ...

    @abstractmethod
    def read_joint_velocity(self) -> float:
        """
        Read joint velocity data (for joint sensors).

        Returns:
            Joint velocity value
        """
        ...

    @abstractmethod
    def read_joint_force(self) -> float:
        """
        Read joint force data (for joint sensors).

        Returns:
            Joint force value
        """
        ...

    @abstractmethod
    def set_update_rate(self, rate: float) -> None:
        """
        Set the sensor update rate.

        Args:
            rate: Update rate in Hz
        """
        ...

    @abstractmethod
    def enable(self) -> None:
        """Enable the sensor."""
        ...

    @abstractmethod
    def disable(self) -> None:
        """Disable the sensor."""
        ...

    @abstractmethod
    def remove(self) -> None:
        """Remove the sensor from the simulation."""
        ...

    def get_sensor_type(self) -> SensorType:
        """Get the sensor type."""
        return self.sensor_type

    def get_attached_body(self) -> "SimulationBodyInterface | None":
        """Get the attached body."""
        return self.attached_body

    def get_attached_joint(self) -> "SimulationJointInterface | None":
        """Get the attached joint."""
        return self.attached_joint

    def is_sensor_enabled(self) -> bool:
        """Check if the sensor is enabled."""
        return self.is_enabled

    def get_update_rate(self) -> float:
        """Get the sensor update rate."""
        return self.update_rate

    def __repr__(self) -> str:
        return f"<SimulationSensor: {self.name or 'Unnamed'}, Type: {self.sensor_type.value}>"
