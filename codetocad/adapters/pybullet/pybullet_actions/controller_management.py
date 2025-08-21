"""
PyBullet controller management functions.
"""

from typing import Dict, Any, List, Optional, Tuple
import pybullet as p


class PIDController:
    """Simple PID controller implementation."""

    def __init__(self, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, error: float, dt: float) -> float:
        """Update PID controller and return control output."""
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0

        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error

        return output

    def reset(self) -> None:
        """Reset PID controller state."""
        self.prev_error = 0.0
        self.integral = 0.0


def create_position_controller(
    body_id: int,
    joint_index: int,
    kp: float = 100.0,
    ki: float = 0.0,
    kd: float = 10.0,
    max_force: float = 1000.0,
) -> Dict[str, Any]:
    """Create a position controller for a joint."""
    controller = {
        "type": "position",
        "body_id": body_id,
        "joint_index": joint_index,
        "pid": PIDController(kp, ki, kd),
        "max_force": max_force,
        "target_position": 0.0,
        "enabled": True,
    }
    return controller


def create_velocity_controller(
    body_id: int,
    joint_index: int,
    kp: float = 10.0,
    ki: float = 0.0,
    kd: float = 1.0,
    max_force: float = 1000.0,
) -> Dict[str, Any]:
    """Create a velocity controller for a joint."""
    controller = {
        "type": "velocity",
        "body_id": body_id,
        "joint_index": joint_index,
        "pid": PIDController(kp, ki, kd),
        "max_force": max_force,
        "target_velocity": 0.0,
        "enabled": True,
    }
    return controller


def create_force_controller(body_id: int, joint_index: int) -> Dict[str, Any]:
    """Create a force controller for a joint."""
    controller = {
        "type": "force",
        "body_id": body_id,
        "joint_index": joint_index,
        "target_force": 0.0,
        "enabled": True,
    }
    return controller


def create_trajectory_controller(
    body_ids: List[int],
    joint_indices: List[int],
    kp: float = 100.0,
    ki: float = 0.0,
    kd: float = 10.0,
    max_forces: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """Create a trajectory controller for multiple joints."""
    if max_forces is None:
        max_forces = [1000.0] * len(joint_indices)

    controllers = []
    for i, (body_id, joint_idx) in enumerate(zip(body_ids, joint_indices)):
        controller = create_position_controller(
            body_id, joint_idx, kp, ki, kd, max_forces[i]
        )
        controllers.append(controller)

    trajectory_controller = {
        "type": "trajectory",
        "controllers": controllers,
        "trajectory": [],
        "current_waypoint": 0,
        "trajectory_time": 0.0,
        "enabled": True,
    }
    return trajectory_controller


def set_controller_target_position(controller: Dict[str, Any], position: float) -> None:
    """Set target position for a position controller."""
    if controller["type"] == "position":
        controller["target_position"] = position


def set_controller_target_velocity(controller: Dict[str, Any], velocity: float) -> None:
    """Set target velocity for a velocity controller."""
    if controller["type"] == "velocity":
        controller["target_velocity"] = velocity


def set_controller_target_force(controller: Dict[str, Any], force: float) -> None:
    """Set target force for a force controller."""
    if controller["type"] == "force":
        controller["target_force"] = force


def set_trajectory(
    controller: Dict[str, Any],
    positions: List[List[float]],
    velocities: Optional[List[List[float]]] = None,
    times: Optional[List[float]] = None,
) -> None:
    """Set trajectory for a trajectory controller."""
    if controller["type"] == "trajectory":
        trajectory = []
        for i, pos in enumerate(positions):
            waypoint = {
                "positions": pos,
                "velocities": velocities[i] if velocities else [0.0] * len(pos),
                "time": times[i] if times else i * 1.0,  # Default 1 second per waypoint
            }
            trajectory.append(waypoint)

        controller["trajectory"] = trajectory
        controller["current_waypoint"] = 0
        controller["trajectory_time"] = 0.0


def update_controller(controller: Dict[str, Any], dt: float) -> None:
    """Update a controller."""
    if not controller["enabled"]:
        return

    controller_type = controller["type"]

    if controller_type == "position":
        _update_position_controller(controller, dt)
    elif controller_type == "velocity":
        _update_velocity_controller(controller, dt)
    elif controller_type == "force":
        _update_force_controller(controller, dt)
    elif controller_type == "trajectory":
        _update_trajectory_controller(controller, dt)


def _update_position_controller(controller: Dict[str, Any], dt: float) -> None:
    """Update position controller."""
    body_id = controller["body_id"]
    joint_index = controller["joint_index"]
    target_pos = controller["target_position"]
    max_force = controller["max_force"]
    pid = controller["pid"]

    # Get current position
    joint_state = p.getJointState(body_id, joint_index)
    current_pos = joint_state[0]

    # Calculate error and PID output
    error = target_pos - current_pos
    control_output = pid.update(error, dt)

    # Clamp to max force
    force = max(-max_force, min(max_force, control_output))

    # Apply control
    p.setJointMotorControl2(
        body_id, joint_index, p.POSITION_CONTROL, targetPosition=target_pos, force=force
    )


def _update_velocity_controller(controller: Dict[str, Any], dt: float) -> None:
    """Update velocity controller."""
    body_id = controller["body_id"]
    joint_index = controller["joint_index"]
    target_vel = controller["target_velocity"]
    max_force = controller["max_force"]
    pid = controller["pid"]

    # Get current velocity
    joint_state = p.getJointState(body_id, joint_index)
    current_vel = joint_state[1]

    # Calculate error and PID output
    error = target_vel - current_vel
    control_output = pid.update(error, dt)

    # Clamp to max force
    force = max(-max_force, min(max_force, control_output))

    # Apply control
    p.setJointMotorControl2(
        body_id, joint_index, p.VELOCITY_CONTROL, targetVelocity=target_vel, force=force
    )


def _update_force_controller(controller: Dict[str, Any], dt: float) -> None:
    """Update force controller."""
    body_id = controller["body_id"]
    joint_index = controller["joint_index"]
    target_force = controller["target_force"]

    # Apply force directly
    p.setJointMotorControl2(body_id, joint_index, p.TORQUE_CONTROL, force=target_force)


def _update_trajectory_controller(controller: Dict[str, Any], dt: float) -> None:
    """Update trajectory controller."""
    trajectory = controller["trajectory"]
    if not trajectory:
        return

    controller["trajectory_time"] += dt
    current_waypoint = controller["current_waypoint"]

    if current_waypoint >= len(trajectory):
        return  # Trajectory complete

    waypoint = trajectory[current_waypoint]
    target_positions = waypoint["positions"]

    # Update each joint controller
    for i, joint_controller in enumerate(controller["controllers"]):
        if i < len(target_positions):
            set_controller_target_position(joint_controller, target_positions[i])
            _update_position_controller(joint_controller, dt)

    # Check if we should move to next waypoint
    if controller["trajectory_time"] >= waypoint["time"]:
        controller["current_waypoint"] += 1


def enable_controller(controller: Dict[str, Any]) -> None:
    """Enable a controller."""
    controller["enabled"] = True


def disable_controller(controller: Dict[str, Any]) -> None:
    """Disable a controller."""
    controller["enabled"] = False


def reset_controller(controller: Dict[str, Any]) -> None:
    """Reset controller state."""
    if "pid" in controller:
        controller["pid"].reset()

    if controller["type"] == "trajectory":
        controller["current_waypoint"] = 0
        controller["trajectory_time"] = 0.0
        for joint_controller in controller["controllers"]:
            reset_controller(joint_controller)
