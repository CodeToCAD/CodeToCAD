"""
PyBullet implementation of SimulationControllerInterface.
"""

from typing import TYPE_CHECKING, Dict, Any, Tuple
from codetocad.interfaces.simulation.simulation_controller_interface import (
    SimulationControllerInterface,
    ControllerType,
)
from codetocad.adapters.pybullet.pybullet_actions import controller_management

if TYPE_CHECKING:
    from codetocad.adapters.pybullet.simulation.simulation_body import SimulationBody
    from codetocad.adapters.pybullet.simulation.simulation_joint import SimulationJoint
    from codetocad.adapters.pybullet.simulation.simulation_sensor import (
        SimulationSensor,
    )


class SimulationController(SimulationControllerInterface):
    """PyBullet implementation of SimulationControllerInterface."""

    def __init__(self):
        super().__init__()
        self.controller_data: dict[str, Any] = {}

    def create_pid_controller(
        self,
        joint: "SimulationJoint",
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        **kwargs,
    ) -> None:
        """Create a PID controller for a joint."""
        self.controller_type = ControllerType.PID
        self.controlled_joints = [joint]

        if joint.body_id is not None and joint.joint_index is not None:
            self.controller_data = controller_management.create_position_controller(
                joint.body_id, joint.joint_index, kp, ki, kd, **kwargs
            )

    def create_position_controller(
        self, joint: "SimulationJoint", max_force: float = 1000.0, **kwargs
    ) -> None:
        """Create a position controller for a joint."""
        self.controller_type = ControllerType.POSITION
        self.controlled_joints = [joint]

        if joint.body_id is not None and joint.joint_index is not None:
            self.controller_data = controller_management.create_position_controller(
                joint.body_id, joint.joint_index, max_force=max_force, **kwargs
            )

    def create_velocity_controller(
        self, joint: "SimulationJoint", max_force: float = 1000.0, **kwargs
    ) -> None:
        """Create a velocity controller for a joint."""
        self.controller_type = ControllerType.VELOCITY
        self.controlled_joints = [joint]

        if joint.body_id is not None and joint.joint_index is not None:
            self.controller_data = controller_management.create_velocity_controller(
                joint.body_id, joint.joint_index, max_force=max_force, **kwargs
            )

    def create_force_controller(self, joint: "SimulationJoint", **kwargs) -> None:
        """Create a force controller for a joint."""
        self.controller_type = ControllerType.FORCE
        self.controlled_joints = [joint]

        if joint.body_id is not None and joint.joint_index is not None:
            self.controller_data = controller_management.create_force_controller(
                joint.body_id, joint.joint_index, **kwargs
            )

    def create_trajectory_controller(
        self, joints: list["SimulationJoint"], **kwargs
    ) -> None:
        """Create a trajectory controller for multiple joints."""
        self.controller_type = ControllerType.TRAJECTORY
        self.controlled_joints = joints

        body_ids = []
        joint_indices = []

        for joint in joints:
            if joint.body_id is not None and joint.joint_index is not None:
                body_ids.append(joint.body_id)
                joint_indices.append(joint.joint_index)

        if body_ids and joint_indices:
            self.controller_data = controller_management.create_trajectory_controller(
                body_ids, joint_indices, **kwargs
            )

    def set_target_position(self, position: float | list[float]) -> None:
        """Set the target position for the controller."""
        if isinstance(position, (int, float)):
            controller_management.set_controller_target_position(
                self.controller_data, position
            )
        elif (
            isinstance(position, list)
            and self.controller_type == ControllerType.TRAJECTORY
        ):
            # For trajectory controller, set positions for all joints
            if "controllers" in self.controller_data:
                for i, controller in enumerate(self.controller_data["controllers"]):
                    if i < len(position):
                        controller_management.set_controller_target_position(
                            controller, position[i]
                        )

    def set_target_velocity(self, velocity: float | list[float]) -> None:
        """Set the target velocity for the controller."""
        if isinstance(velocity, (int, float)):
            controller_management.set_controller_target_velocity(
                self.controller_data, velocity
            )
        elif (
            isinstance(velocity, list)
            and self.controller_type == ControllerType.TRAJECTORY
        ):
            # For trajectory controller, set velocities for all joints
            if "controllers" in self.controller_data:
                for i, controller in enumerate(self.controller_data["controllers"]):
                    if i < len(velocity):
                        controller_management.set_controller_target_velocity(
                            controller, velocity[i]
                        )

    def set_target_force(self, force: float | list[float]) -> None:
        """Set the target force for the controller."""
        if isinstance(force, (int, float)):
            controller_management.set_controller_target_force(
                self.controller_data, force
            )

    def set_trajectory(
        self,
        positions: list[list[float]],
        velocities: list[list[float]] | None = None,
        times: list[float] | None = None,
    ) -> None:
        """Set a trajectory for the controller to follow."""
        if self.controller_type == ControllerType.TRAJECTORY:
            controller_management.set_trajectory(
                self.controller_data, positions, velocities, times
            )

    def get_current_position(self) -> float | list[float]:
        """Get the current position of controlled joints."""
        if len(self.controlled_joints) == 1:
            joint = self.controlled_joints[0]
            return joint.get_position()
        else:
            return [joint.get_position() for joint in self.controlled_joints]

    def get_current_velocity(self) -> float | list[float]:
        """Get the current velocity of controlled joints."""
        if len(self.controlled_joints) == 1:
            joint = self.controlled_joints[0]
            return joint.get_velocity()
        else:
            return [joint.get_velocity() for joint in self.controlled_joints]

    def get_current_force(self) -> float | list[float]:
        """Get the current force of controlled joints."""
        # This would require force sensors on the joints
        if len(self.controlled_joints) == 1:
            return 0.0  # Placeholder
        else:
            return [0.0] * len(self.controlled_joints)  # Placeholder

    def set_pid_gains(self, kp: float, ki: float, kd: float) -> None:
        """Set PID gains for the controller."""
        if "pid" in self.controller_data:
            pid = self.controller_data["pid"]
            pid.kp = kp
            pid.ki = ki
            pid.kd = kd

    def get_pid_gains(self) -> tuple[float, float, float]:
        """Get PID gains for the controller."""
        if "pid" in self.controller_data:
            pid = self.controller_data["pid"]
            return (pid.kp, pid.ki, pid.kd)
        return (0.0, 0.0, 0.0)

    def set_limits(
        self,
        position_limits: tuple[float, float] | None = None,
        velocity_limits: tuple[float, float] | None = None,
        force_limits: tuple[float, float] | None = None,
    ) -> None:
        """Set controller limits."""
        # Store limits in controller data
        if position_limits:
            self.controller_data["position_limits"] = position_limits
        if velocity_limits:
            self.controller_data["velocity_limits"] = velocity_limits
        if force_limits:
            self.controller_data["force_limits"] = force_limits

    def add_sensor(self, sensor: "SimulationSensor") -> None:
        """Add a sensor for feedback control."""
        if sensor not in self.sensors:
            self.sensors.append(sensor)

    def remove_sensor(self, sensor: "SimulationSensor") -> None:
        """Remove a sensor from the controller."""
        if sensor in self.sensors:
            self.sensors.remove(sensor)

    def update(self, dt: float) -> None:
        """Update the controller."""
        if self.is_enabled and self.controller_data:
            controller_management.update_controller(self.controller_data, dt)

    def reset(self) -> None:
        """Reset the controller state."""
        if self.controller_data:
            controller_management.reset_controller(self.controller_data)

    def enable(self) -> None:
        """Enable the controller."""
        self.is_enabled = True
        if self.controller_data:
            controller_management.enable_controller(self.controller_data)

    def disable(self) -> None:
        """Disable the controller."""
        self.is_enabled = False
        if self.controller_data:
            controller_management.disable_controller(self.controller_data)

    def remove(self) -> None:
        """Remove the controller from the simulation."""
        self.disable()
        self.controller_data.clear()
