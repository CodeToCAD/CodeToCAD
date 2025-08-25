"""
MuJoCo implementation of SimulationSensorInterface.
"""

from typing import TYPE_CHECKING, Any, Dict
from codetocad.interfaces.simulation.simulation_sensor_interface import (
    SimulationSensorInterface,
    SensorType,
)
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody
    from codetocad.adapters.mujoco.simulation.simulation_joint import SimulationJoint


class SimulationSensor(SimulationSensorInterface):
    """MuJoCo implementation of SimulationSensorInterface."""

    def __init__(self):
        super().__init__()

    def create_force_sensor(self, body, position=(0, 0, 0), **kwargs):
        """Create a force sensor attached to a body."""
        self.sensor_type = SensorType.FORCE
        self.attached_body = body

    def create_torque_sensor(self, body, **kwargs):
        """Create a torque sensor attached to a body."""
        self.sensor_type = SensorType.TORQUE
        self.attached_body = body

    def create_position_sensor(self, body, **kwargs):
        """Create a position sensor attached to a body."""
        self.sensor_type = SensorType.POSITION
        self.attached_body = body

    def create_velocity_sensor(self, body, **kwargs):
        """Create a velocity sensor attached to a body."""
        self.sensor_type = SensorType.VELOCITY
        self.attached_body = body

    def create_contact_sensor(self, body, **kwargs):
        """Create a contact sensor attached to a body."""
        self.sensor_type = SensorType.CONTACT
        self.attached_body = body

    def create_joint_sensor(
        self, joint, sensor_type=SensorType.JOINT_POSITION, **kwargs
    ):
        """Create a sensor attached to a joint."""
        self.sensor_type = sensor_type
        self.attached_joint = joint

    def create_imu_sensor(self, body, position=(0, 0, 0), **kwargs):
        """Create an IMU sensor."""
        self.sensor_type = SensorType.IMU
        self.attached_body = body

    def read_data(self) -> Any:
        """Read the current sensor data."""
        return None

    def read_force(self) -> Point:
        """Read force data."""
        return Point(0, 0, 0)

    def read_torque(self) -> Point:
        """Read torque data."""
        return Point(0, 0, 0)

    def read_position(self) -> Point:
        """Read position data."""
        if self.attached_body:
            return self.attached_body.get_position()
        return Point(0, 0, 0)

    def read_velocity(self) -> Point:
        """Read velocity data."""
        if self.attached_body:
            return self.attached_body.get_linear_velocity()
        return Point(0, 0, 0)

    def read_acceleration(self) -> Point:
        """Read acceleration data."""
        return Point(0, 0, 0)

    def read_angular_velocity(self) -> Point:
        """Read angular velocity data."""
        if self.attached_body:
            return self.attached_body.get_angular_velocity()
        return Point(0, 0, 0)

    def read_contact_points(self) -> list[dict[str, Any]]:
        """Read contact point data."""
        if self.attached_body:
            return self.attached_body.get_contact_points()
        return []

    def read_joint_position(self) -> float:
        """Read joint position data."""
        if self.attached_joint:
            return self.attached_joint.get_position()
        return 0.0

    def read_joint_velocity(self) -> float:
        """Read joint velocity data."""
        if self.attached_joint:
            return self.attached_joint.get_velocity()
        return 0.0

    def read_joint_force(self) -> float:
        """Read joint force data."""
        return 0.0

    def set_update_rate(self, rate: float) -> None:
        """Set the sensor update rate."""
        self.update_rate = rate

    def enable(self) -> None:
        """Enable the sensor."""
        self.is_enabled = True

    def disable(self) -> None:
        """Disable the sensor."""
        self.is_enabled = False

    def remove(self) -> None:
        """Remove the sensor from the simulation."""
        pass
