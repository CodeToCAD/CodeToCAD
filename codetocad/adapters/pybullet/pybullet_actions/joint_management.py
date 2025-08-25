"""
PyBullet joint management functions.
"""

from typing import Tuple, Dict, Any
import pybullet as p
from codetocad.core.dimensions.point import Point


def create_joint(
    parent_body_id: int,
    child_body_id: int,
    joint_type: int,
    joint_axis: Point | tuple[float, float, float],
    parent_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    child_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    parent_frame_orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
    child_frame_orientation: tuple[float, float, float, float] = (0, 0, 0, 1),
    **kwargs,
) -> int:
    """Create a joint between two bodies."""
    if isinstance(joint_axis, Point):
        axis = (joint_axis.x, joint_axis.y, joint_axis.z)
    else:
        axis = joint_axis

    if isinstance(parent_frame_position, Point):
        parent_pos = (
            parent_frame_position.x,
            parent_frame_position.y,
            parent_frame_position.z,
        )
    else:
        parent_pos = parent_frame_position

    if isinstance(child_frame_position, Point):
        child_pos = (
            child_frame_position.x,
            child_frame_position.y,
            child_frame_position.z,
        )
    else:
        child_pos = child_frame_position

    joint_id = p.createConstraint(
        parentBodyUniqueId=parent_body_id,
        parentLinkIndex=-1,
        childBodyUniqueId=child_body_id,
        childLinkIndex=-1,
        jointType=joint_type,
        jointAxis=axis,
        parentFramePosition=parent_pos,
        childFramePosition=child_pos,
        parentFrameOrientation=parent_frame_orientation,
        childFrameOrientation=child_frame_orientation,
        **kwargs,
    )

    return joint_id


def create_fixed_joint(
    parent_body_id: int,
    child_body_id: int,
    parent_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    child_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    **kwargs,
) -> int:
    """Create a fixed joint."""
    return create_joint(
        parent_body_id,
        child_body_id,
        p.JOINT_FIXED,
        (0, 0, 0),  # Axis doesn't matter for fixed joint
        parent_frame_position,
        child_frame_position,
        **kwargs,
    )


def create_revolute_joint(
    parent_body_id: int,
    child_body_id: int,
    axis: Point | tuple[float, float, float],
    parent_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    child_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    **kwargs,
) -> int:
    """Create a revolute joint."""
    return create_joint(
        parent_body_id,
        child_body_id,
        p.JOINT_REVOLUTE,
        axis,
        parent_frame_position,
        child_frame_position,
        **kwargs,
    )


def create_prismatic_joint(
    parent_body_id: int,
    child_body_id: int,
    axis: Point | tuple[float, float, float],
    parent_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    child_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    **kwargs,
) -> int:
    """Create a prismatic joint."""
    return create_joint(
        parent_body_id,
        child_body_id,
        p.JOINT_PRISMATIC,
        axis,
        parent_frame_position,
        child_frame_position,
        **kwargs,
    )


def create_spherical_joint(
    parent_body_id: int,
    child_body_id: int,
    parent_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    child_frame_position: Point | tuple[float, float, float] = (0, 0, 0),
    **kwargs,
) -> int:
    """Create a spherical joint."""
    return create_joint(
        parent_body_id,
        child_body_id,
        p.JOINT_SPHERICAL,
        (0, 0, 0),  # Axis doesn't matter for spherical joint
        parent_frame_position,
        child_frame_position,
        **kwargs,
    )


def remove_joint(joint_id: int) -> None:
    """Remove a joint from the simulation."""
    p.removeConstraint(joint_id)


def set_joint_position(joint_id: int, position: float) -> None:
    """Set joint position (for position control)."""
    # This is typically done through joint control, not constraint modification
    # For actual joint control, we'd need the body and joint index
    pass


def get_joint_position(body_id: int, joint_index: int) -> float:
    """Get joint position."""
    joint_state = p.getJointState(body_id, joint_index)
    return joint_state[0]  # Joint position


def set_joint_velocity(body_id: int, joint_index: int, velocity: float) -> None:
    """Set joint velocity."""
    p.setJointMotorControl2(
        body_id, joint_index, p.VELOCITY_CONTROL, targetVelocity=velocity
    )


def get_joint_velocity(body_id: int, joint_index: int) -> float:
    """Get joint velocity."""
    joint_state = p.getJointState(body_id, joint_index)
    return joint_state[1]  # Joint velocity


def apply_joint_force(body_id: int, joint_index: int, force: float) -> None:
    """Apply force/torque to joint."""
    p.setJointMotorControl2(body_id, joint_index, p.TORQUE_CONTROL, force=force)


def set_joint_limits(
    body_id: int, joint_index: int, lower_limit: float, upper_limit: float
) -> None:
    """Set joint limits."""
    p.changeDynamics(
        body_id, joint_index, jointLowerLimit=lower_limit, jointUpperLimit=upper_limit
    )


def get_joint_limits(body_id: int, joint_index: int) -> tuple[float, float]:
    """Get joint limits."""
    joint_info = p.getJointInfo(body_id, joint_index)
    return joint_info[8], joint_info[9]  # Lower and upper limits


def get_joint_info(body_id: int, joint_index: int) -> dict[str, Any]:
    """Get comprehensive joint information."""
    joint_info = p.getJointInfo(body_id, joint_index)
    joint_state = p.getJointState(body_id, joint_index)

    return {
        "joint_index": joint_info[0],
        "joint_name": joint_info[1].decode("utf-8"),
        "joint_type": joint_info[2],
        "q_index": joint_info[3],
        "u_index": joint_info[4],
        "flags": joint_info[5],
        "joint_damping": joint_info[6],
        "joint_friction": joint_info[7],
        "joint_lower_limit": joint_info[8],
        "joint_upper_limit": joint_info[9],
        "joint_max_force": joint_info[10],
        "joint_max_velocity": joint_info[11],
        "link_name": joint_info[12].decode("utf-8"),
        "joint_axis": joint_info[13],
        "parent_frame_pos": joint_info[14],
        "parent_frame_orn": joint_info[15],
        "parent_index": joint_info[16],
        "position": joint_state[0],
        "velocity": joint_state[1],
        "reaction_forces": joint_state[2],
        "applied_torque": joint_state[3],
    }


def enable_joint_force_torque_sensor(
    body_id: int, joint_index: int, enable: bool = True
) -> None:
    """Enable or disable joint force/torque sensor."""
    p.enableJointForceTorqueSensor(body_id, joint_index, enable)


def get_joint_reaction_forces(body_id: int, joint_index: int) -> tuple[float, ...]:
    """Get joint reaction forces."""
    joint_state = p.getJointState(body_id, joint_index)
    return joint_state[2]  # Reaction forces


def set_joint_motor_control(
    body_id: int,
    joint_index: int,
    control_mode: int,
    target_position: float | None = None,
    target_velocity: float | None = None,
    force: float | None = None,
    position_gain: float = 0.1,
    velocity_gain: float = 1.0,
    max_velocity: float | None = None,
) -> None:
    """Set joint motor control."""
    p.setJointMotorControl2(
        bodyUniqueId=body_id,
        jointIndex=joint_index,
        controlMode=control_mode,
        targetPosition=target_position,
        targetVelocity=target_velocity,
        force=force,
        positionGain=position_gain,
        velocityGain=velocity_gain,
        maxVelocity=max_velocity,
    )
