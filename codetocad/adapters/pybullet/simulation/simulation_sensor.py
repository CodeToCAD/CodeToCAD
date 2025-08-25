"""
PyBullet implementation of SimulationSensorInterface.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional
from codetocad.interfaces.simulation.simulation_sensor_interface import (
    SimulationSensorInterface,
    SensorType,
)
from codetocad.core.dimensions.point import Point
from codetocad.adapters.pybullet.pybullet_actions import sensor_management

if TYPE_CHECKING:
    from codetocad.adapters.pybullet.simulation.simulation_body import SimulationBody
    from codetocad.adapters.pybullet.simulation.simulation_joint import SimulationJoint


class SimulationSensor(SimulationSensorInterface):
    """PyBullet implementation of SimulationSensorInterface."""

    def __init__(self):
        super().__init__()
        self.sensor_data: dict[str, Any] = {}

    def create_force_sensor(
        self,
        body: "SimulationBody",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """Create a force sensor attached to a body."""
        self.sensor_type = SensorType.FORCE
        self.attached_body = body

        if body.body_id is not None:
            sensor_management.create_force_sensor(body.body_id)
            self.sensor_data = {
                "body_id": body.body_id,
                "sensor_type": "force",
                "position": position,
            }

    def create_torque_sensor(self, body: "SimulationBody", **kwargs) -> None:
        """Create a torque sensor attached to a body."""
        self.sensor_type = SensorType.TORQUE
        self.attached_body = body

        if body.body_id is not None:
            self.sensor_data = {"body_id": body.body_id, "sensor_type": "torque"}

    def create_position_sensor(self, body: "SimulationBody", **kwargs) -> None:
        """Create a position sensor attached to a body."""
        self.sensor_type = SensorType.POSITION
        self.attached_body = body

        if body.body_id is not None:
            self.sensor_data = {"body_id": body.body_id, "sensor_type": "position"}

    def create_velocity_sensor(self, body: "SimulationBody", **kwargs) -> None:
        """Create a velocity sensor attached to a body."""
        self.sensor_type = SensorType.VELOCITY
        self.attached_body = body

        if body.body_id is not None:
            self.sensor_data = {"body_id": body.body_id, "sensor_type": "velocity"}

    def create_contact_sensor(self, body: "SimulationBody", **kwargs) -> None:
        """Create a contact sensor attached to a body."""
        self.sensor_type = SensorType.CONTACT
        self.attached_body = body

        if body.body_id is not None:
            self.sensor_data = sensor_management.create_contact_sensor(body.body_id)

    def create_joint_sensor(
        self,
        joint: "SimulationJoint",
        sensor_type: SensorType = SensorType.JOINT_POSITION,
        **kwargs,
    ) -> None:
        """Create a sensor attached to a joint."""
        self.sensor_type = sensor_type
        self.attached_joint = joint

        if joint.body_id is not None and joint.joint_index is not None:
            self.sensor_data = {
                "body_id": joint.body_id,
                "joint_index": joint.joint_index,
                "sensor_type": sensor_type.value,
            }

    def create_imu_sensor(
        self,
        body: "SimulationBody",
        position: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """Create an IMU sensor."""
        self.sensor_type = SensorType.IMU
        self.attached_body = body

        if body.body_id is not None:
            self.sensor_data = sensor_management.create_imu_sensor(body.body_id)

    def read_data(self) -> Any:
        """Read the current sensor data."""
        return sensor_management.read_sensor_data(self.sensor_data)

    def read_force(self) -> Point:
        """Read force data."""
        if self.attached_body and self.attached_body.body_id is not None:
            return sensor_management.read_force_data(self.attached_body.body_id)
        return Point(0, 0, 0)

    def read_torque(self) -> Point:
        """Read torque data."""
        if self.attached_body and self.attached_body.body_id is not None:
            return sensor_management.read_torque_data(self.attached_body.body_id)
        return Point(0, 0, 0)

    def read_position(self) -> Point:
        """Read position data."""
        if self.attached_body and self.attached_body.body_id is not None:
            return sensor_management.read_position_data(self.attached_body.body_id)
        return Point(0, 0, 0)

    def read_velocity(self) -> Point:
        """Read velocity data."""
        if self.attached_body and self.attached_body.body_id is not None:
            return sensor_management.read_velocity_data(self.attached_body.body_id)
        return Point(0, 0, 0)

    def read_acceleration(self) -> Point:
        """Read acceleration data."""
        # For IMU sensors
        if self.sensor_type == SensorType.IMU and self.sensor_data:
            imu_data = sensor_management.read_imu_data(self.sensor_data)
            return imu_data.get("linear_acceleration", Point(0, 0, 0))
        return Point(0, 0, 0)

    def read_angular_velocity(self) -> Point:
        """Read angular velocity data."""
        if self.attached_body and self.attached_body.body_id is not None:
            return sensor_management.read_angular_velocity_data(
                self.attached_body.body_id
            )
        return Point(0, 0, 0)

    def read_contact_points(self) -> list[dict[str, Any]]:
        """Read contact point data."""
        if self.attached_body and self.attached_body.body_id is not None:
            return sensor_management.read_contact_data(self.attached_body.body_id)
        return []

    def read_joint_position(self) -> float:
        """Read joint position data."""
        if (
            self.attached_joint
            and self.attached_joint.body_id is not None
            and self.attached_joint.joint_index is not None
        ):
            return sensor_management.read_joint_position_data(
                self.attached_joint.body_id, self.attached_joint.joint_index
            )
        return 0.0

    def read_joint_velocity(self) -> float:
        """Read joint velocity data."""
        if (
            self.attached_joint
            and self.attached_joint.body_id is not None
            and self.attached_joint.joint_index is not None
        ):
            return sensor_management.read_joint_velocity_data(
                self.attached_joint.body_id, self.attached_joint.joint_index
            )
        return 0.0

    def read_joint_force(self) -> float:
        """Read joint force data."""
        if (
            self.attached_joint
            and self.attached_joint.body_id is not None
            and self.attached_joint.joint_index is not None
        ):
            return sensor_management.read_joint_force_data(
                self.attached_joint.body_id, self.attached_joint.joint_index
            )
        return 0.0

    def set_update_rate(self, rate: float) -> None:
        """Set the sensor update rate."""
        self.update_rate = rate

    def enable(self) -> None:
        """Enable the sensor."""
        self.is_enabled = True
        if self.sensor_data:
            sensor_management.enable_sensor(self.sensor_data)

    def disable(self) -> None:
        """Disable the sensor."""
        self.is_enabled = False
        if self.sensor_data:
            sensor_management.disable_sensor(self.sensor_data)

    def remove(self) -> None:
        """Remove the sensor from the simulation."""
        self.disable()
        self.sensor_data.clear()
