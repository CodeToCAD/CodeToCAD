"""
PyBullet body management functions.
"""

from typing import Optional, Tuple, Any, Dict, List
import pybullet as p
import tempfile
import os

import pybullet_data
from codetocad.core.dimensions.point import Point


def create_body_from_urdf(
    urdf_path: str,
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
    **kwargs,
) -> int:
    """Create a body from URDF file."""
    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    body_id = p.loadURDF(
        urdf_path, basePosition=pos, baseOrientation=orientation, **kwargs
    )
    return body_id


def create_body_from_stl(
    stl_path: str,
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
    mass: float = 1.0,
    **kwargs,
) -> int:
    """Create a body from STL file."""
    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    # Create collision shape from mesh
    collision_shape = p.createCollisionShape(p.GEOM_MESH, fileName=stl_path, **kwargs)

    # Create visual shape from mesh
    visual_shape = p.createVisualShape(p.GEOM_MESH, fileName=stl_path, **kwargs)

    # Create multi-body
    body_id = p.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=collision_shape,
        baseVisualShapeIndex=visual_shape,
        basePosition=pos,
        baseOrientation=orientation,
    )

    return body_id


def create_body_from_part(
    part: Any,  # PartInterface
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    orientation: Tuple[float, float, float, float] = (0, 0, 0, 1),
    mass: float = 1.0,
    **kwargs,
) -> int:
    """Create a body from CodeToCAD Part."""
    # Export part to temporary STL file
    with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        # Export the part to STL
        part.export.stl(tmp_path)

        # Create body from STL
        body_id = create_body_from_stl(tmp_path, position, orientation, mass, **kwargs)

        return body_id
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def create_ground_plane(
    position: Point | Tuple[float, float, float] = (0, 0, 0),
    normal: Point | Tuple[float, float, float] = (0, 0, 1),
    **kwargs,
) -> int:
    """Create a ground plane."""
    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    # Create plane shape
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    plane_id = p.loadURDF("plane.urdf", basePosition=pos, **kwargs)
    return plane_id


def remove_body(body_id: int) -> None:
    """Remove a body from the simulation."""
    p.removeBody(body_id)


def set_body_position(
    body_id: int,
    position: Point | Tuple[float, float, float],
    orientation: Optional[Tuple[float, float, float, float]] = None,
) -> None:
    """Set body position and orientation."""
    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    if orientation is None:
        # Get current orientation
        _, current_orn = p.getBasePositionAndOrientation(body_id)
        orientation = current_orn

    p.resetBasePositionAndOrientation(body_id, pos, orientation)


def get_body_position(body_id: int) -> Tuple[Point, Tuple[float, float, float, float]]:
    """Get body position and orientation."""
    pos, orn = p.getBasePositionAndOrientation(body_id)
    return Point(pos[0], pos[1], pos[2]), orn


def set_body_velocity(
    body_id: int,
    linear_velocity: Point | Tuple[float, float, float],
    angular_velocity: Point | Tuple[float, float, float] = (0, 0, 0),
) -> None:
    """Set body velocity."""
    if isinstance(linear_velocity, Point):
        lin_vel = (linear_velocity.x, linear_velocity.y, linear_velocity.z)
    else:
        lin_vel = linear_velocity

    if isinstance(angular_velocity, Point):
        ang_vel = (angular_velocity.x, angular_velocity.y, angular_velocity.z)
    else:
        ang_vel = angular_velocity

    p.resetBaseVelocity(body_id, lin_vel, ang_vel)


def get_body_velocity(body_id: int) -> Tuple[Point, Point]:
    """Get body velocity."""
    lin_vel, ang_vel = p.getBaseVelocity(body_id)
    return Point(lin_vel[0], lin_vel[1], lin_vel[2]), Point(
        ang_vel[0], ang_vel[1], ang_vel[2]
    )


def apply_force_to_body(
    body_id: int,
    force: Point | Tuple[float, float, float],
    position: Optional[Point | Tuple[float, float, float]] = None,
) -> None:
    """Apply force to body."""
    if isinstance(force, Point):
        force_vec = (force.x, force.y, force.z)
    else:
        force_vec = force

    if position is None:
        # Apply at center of mass
        p.applyExternalForce(body_id, -1, force_vec, (0, 0, 0), p.LINK_FRAME)
    else:
        if isinstance(position, Point):
            pos = (position.x, position.y, position.z)
        else:
            pos = position
        p.applyExternalForce(body_id, -1, force_vec, pos, p.WORLD_FRAME)


def apply_torque_to_body(
    body_id: int, torque: Point | Tuple[float, float, float]
) -> None:
    """Apply torque to body."""
    if isinstance(torque, Point):
        torque_vec = (torque.x, torque.y, torque.z)
    else:
        torque_vec = torque

    p.applyExternalTorque(body_id, -1, torque_vec, p.LINK_FRAME)


def get_body_mass(body_id: int) -> float:
    """Get body mass."""
    dynamics_info = p.getDynamicsInfo(body_id, -1)
    return dynamics_info[0]  # Mass is the first element


def set_body_mass(body_id: int, mass: float) -> None:
    """Set body mass."""
    p.changeDynamics(body_id, -1, mass=mass)


def set_body_friction(body_id: int, friction: float) -> None:
    """Set body friction."""
    p.changeDynamics(body_id, -1, lateralFriction=friction)


def set_body_restitution(body_id: int, restitution: float) -> None:
    """Set body restitution."""
    p.changeDynamics(body_id, -1, restitution=restitution)


def get_contact_points(body_id: int) -> List[Dict[str, Any]]:
    """Get contact points for a body."""
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
        }
        contact_list.append(contact_info)

    return contact_list
