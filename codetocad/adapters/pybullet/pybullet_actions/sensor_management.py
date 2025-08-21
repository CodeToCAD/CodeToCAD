"""
PyBullet sensor management functions.
"""

from typing import Dict, Any, List, Tuple, Optional
import pybullet as p
from codetocad.core.dimensions.point import Point


def create_force_sensor(body_id: int, link_index: int = -1) -> None:
    """Enable force sensor on a body/link."""
    p.enableJointForceTorqueSensor(body_id, link_index, True)


def create_contact_sensor(body_id: int) -> Dict[str, Any]:
    """Create a contact sensor for a body."""
    return {"body_id": body_id, "sensor_type": "contact", "enabled": True}


def read_sensor_data(sensor_info: Dict[str, Any]) -> Any:
    """Read data from a sensor."""
    sensor_type = sensor_info.get("sensor_type")
    body_id = sensor_info.get("body_id")

    if sensor_type == "contact":
        return read_contact_data(body_id)
    elif sensor_type == "force":
        link_index = sensor_info.get("link_index", -1)
        return read_force_data(body_id, link_index)
    elif sensor_type == "position":
        return read_position_data(body_id)
    elif sensor_type == "velocity":
        return read_velocity_data(body_id)
    else:
        return None


def read_contact_data(body_id: int) -> List[Dict[str, Any]]:
    """Read contact data for a body."""
    contacts = p.getContactPoints(bodyA=body_id)
    contact_list = []

    for contact in contacts:
        contact_info = {
            "body_a": contact[1],
            "body_b": contact[2],
            "link_a": contact[3],
            "link_b": contact[4],
            "position_on_a": Point(contact[5][0], contact[5][1], contact[5][2]),
            "position_on_b": Point(contact[6][0], contact[6][1], contact[6][2]),
            "normal": Point(contact[7][0], contact[7][1], contact[7][2]),
            "distance": contact[8],
            "normal_force": contact[9],
        }
        contact_list.append(contact_info)

    return contact_list


def read_force_data(body_id: int, link_index: int = -1) -> Point:
    """Read force data from a force sensor."""
    if link_index == -1:
        # For base link, we need to calculate forces differently
        # This is a simplified implementation
        return Point(0, 0, 0)
    else:
        joint_state = p.getJointState(body_id, link_index)
        reaction_forces = joint_state[2]
        if len(reaction_forces) >= 3:
            return Point(reaction_forces[0], reaction_forces[1], reaction_forces[2])
        else:
            return Point(0, 0, 0)


def read_torque_data(body_id: int, link_index: int = -1) -> Point:
    """Read torque data from a torque sensor."""
    if link_index == -1:
        return Point(0, 0, 0)
    else:
        joint_state = p.getJointState(body_id, link_index)
        reaction_forces = joint_state[2]
        if len(reaction_forces) >= 6:
            return Point(reaction_forces[3], reaction_forces[4], reaction_forces[5])
        else:
            return Point(0, 0, 0)


def read_position_data(body_id: int) -> Point:
    """Read position data from a position sensor."""
    pos, _ = p.getBasePositionAndOrientation(body_id)
    return Point(pos[0], pos[1], pos[2])


def read_orientation_data(body_id: int) -> Tuple[float, float, float, float]:
    """Read orientation data from an orientation sensor."""
    _, orn = p.getBasePositionAndOrientation(body_id)
    return orn


def read_velocity_data(body_id: int) -> Point:
    """Read velocity data from a velocity sensor."""
    lin_vel, _ = p.getBaseVelocity(body_id)
    return Point(lin_vel[0], lin_vel[1], lin_vel[2])


def read_angular_velocity_data(body_id: int) -> Point:
    """Read angular velocity data from an angular velocity sensor."""
    _, ang_vel = p.getBaseVelocity(body_id)
    return Point(ang_vel[0], ang_vel[1], ang_vel[2])


def read_joint_position_data(body_id: int, joint_index: int) -> float:
    """Read joint position data."""
    joint_state = p.getJointState(body_id, joint_index)
    return joint_state[0]


def read_joint_velocity_data(body_id: int, joint_index: int) -> float:
    """Read joint velocity data."""
    joint_state = p.getJointState(body_id, joint_index)
    return joint_state[1]


def read_joint_force_data(body_id: int, joint_index: int) -> float:
    """Read joint force data."""
    joint_state = p.getJointState(body_id, joint_index)
    return joint_state[3]  # Applied torque


def create_imu_sensor(body_id: int, link_index: int = -1) -> Dict[str, Any]:
    """Create an IMU sensor."""
    return {
        "body_id": body_id,
        "link_index": link_index,
        "sensor_type": "imu",
        "enabled": True,
    }


def read_imu_data(sensor_info: Dict[str, Any]) -> Dict[str, Any]:
    """Read IMU data."""
    body_id = sensor_info["body_id"]

    # Get linear acceleration (simplified - would need proper calculation)
    lin_vel, ang_vel = p.getBaseVelocity(body_id)

    # For proper IMU simulation, we'd need to track velocity changes
    # This is a simplified implementation
    imu_data = {
        "linear_acceleration": Point(0, 0, -9.81),  # Gravity
        "angular_velocity": Point(ang_vel[0], ang_vel[1], ang_vel[2]),
        "orientation": read_orientation_data(body_id),
    }

    return imu_data


def get_contact_points(
    body_id: int, other_body_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get contact points for a body."""
    if other_body_id is not None:
        contacts = p.getContactPoints(bodyA=body_id, bodyB=other_body_id)
    else:
        contacts = p.getContactPoints(bodyA=body_id)

    contact_list = []
    for contact in contacts:
        contact_info = {
            "body_a": contact[1],
            "body_b": contact[2],
            "link_a": contact[3],
            "link_b": contact[4],
            "position_on_a": contact[5],
            "position_on_b": contact[6],
            "normal": contact[7],
            "distance": contact[8],
            "normal_force": contact[9],
            "lateral_friction_1": contact[10] if len(contact) > 10 else 0,
            "lateral_friction_dir_1": contact[11] if len(contact) > 11 else (0, 0, 0),
            "lateral_friction_2": contact[12] if len(contact) > 12 else 0,
            "lateral_friction_dir_2": contact[13] if len(contact) > 13 else (0, 0, 0),
        }
        contact_list.append(contact_info)

    return contact_list


def enable_sensor(sensor_info: Dict[str, Any]) -> None:
    """Enable a sensor."""
    sensor_info["enabled"] = True

    if sensor_info["sensor_type"] == "force":
        body_id = sensor_info["body_id"]
        link_index = sensor_info.get("link_index", -1)
        p.enableJointForceTorqueSensor(body_id, link_index, True)


def disable_sensor(sensor_info: Dict[str, Any]) -> None:
    """Disable a sensor."""
    sensor_info["enabled"] = False

    if sensor_info["sensor_type"] == "force":
        body_id = sensor_info["body_id"]
        link_index = sensor_info.get("link_index", -1)
        p.enableJointForceTorqueSensor(body_id, link_index, False)
