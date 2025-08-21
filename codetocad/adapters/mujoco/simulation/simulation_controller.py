"""
MuJoCo implementation of SimulationControllerInterface.
"""

from typing import TYPE_CHECKING, Tuple
from codetocad.interfaces.simulation.simulation_controller_interface import (
    SimulationControllerInterface,
    ControllerType,
)

if TYPE_CHECKING:
    from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody
    from codetocad.adapters.mujoco.simulation.simulation_joint import SimulationJoint
    from codetocad.adapters.mujoco.simulation.simulation_sensor import SimulationSensor


class SimulationController(SimulationControllerInterface):
    """MuJoCo implementation of SimulationControllerInterface."""

    def __init__(self):
        super().__init__()

    def create_pid_controller(self, joint, kp=1.0, ki=0.0, kd=0.0, **kwargs):
        """Create a PID controller for a joint."""
        self.controller_type = ControllerType.PID
        self.controlled_joints = [joint]

    def create_position_controller(self, joint, max_force=1000.0, **kwargs):
        """Create a position controller for a joint."""
        self.controller_type = ControllerType.POSITION
        self.controlled_joints = [joint]

    def create_velocity_controller(self, joint, max_force=1000.0, **kwargs):
        """Create a velocity controller for a joint."""
        self.controller_type = ControllerType.VELOCITY
        self.controlled_joints = [joint]

    def create_force_controller(self, joint, **kwargs):
        """Create a force controller for a joint."""
        self.controller_type = ControllerType.FORCE
        self.controlled_joints = [joint]

    def create_trajectory_controller(self, joints, **kwargs):
        """Create a trajectory controller for multiple joints."""
        self.controller_type = ControllerType.TRAJECTORY
        self.controlled_joints = joints

    def set_target_position(self, position):
        """Set the target position for the controller."""
        pass

    def set_target_velocity(self, velocity):
        """Set the target velocity for the controller."""
        pass

    def set_target_force(self, force):
        """Set the target force for the controller."""
        pass

    def set_trajectory(self, positions, velocities=None, times=None):
        """Set a trajectory for the controller to follow."""
        pass

    def get_current_position(self):
        """Get the current position of controlled joints."""
        if len(self.controlled_joints) == 1:
            return self.controlled_joints[0].get_position()
        return [joint.get_position() for joint in self.controlled_joints]

    def get_current_velocity(self):
        """Get the current velocity of controlled joints."""
        if len(self.controlled_joints) == 1:
            return self.controlled_joints[0].get_velocity()
        return [joint.get_velocity() for joint in self.controlled_joints]

    def get_current_force(self):
        """Get the current force of controlled joints."""
        if len(self.controlled_joints) == 1:
            return 0.0
        return [0.0] * len(self.controlled_joints)

    def set_pid_gains(self, kp: float, ki: float, kd: float) -> None:
        """Set PID gains for the controller."""
        pass

    def get_pid_gains(self) -> Tuple[float, float, float]:
        """Get PID gains for the controller."""
        return (0.0, 0.0, 0.0)

    def set_limits(self, position_limits=None, velocity_limits=None, force_limits=None):
        """Set controller limits."""
        pass

    def add_sensor(self, sensor):
        """Add a sensor for feedback control."""
        if sensor not in self.sensors:
            self.sensors.append(sensor)

    def remove_sensor(self, sensor):
        """Remove a sensor from the controller."""
        if sensor in self.sensors:
            self.sensors.remove(sensor)

    def update(self, dt: float) -> None:
        """Update the controller."""
        pass

    def reset(self) -> None:
        """Reset the controller state."""
        pass

    def enable(self) -> None:
        """Enable the controller."""
        self.is_enabled = True

    def disable(self) -> None:
        """Disable the controller."""
        self.is_enabled = False

    def remove(self) -> None:
        """Remove the controller from the simulation."""
        pass
