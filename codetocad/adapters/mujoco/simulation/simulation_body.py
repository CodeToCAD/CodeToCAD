"""
MuJoCo implementation of SimulationBodyInterface.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional
import mujoco as mj
import numpy as np
from codetocad.interfaces.simulation.simulation_body_interface import (
    SimulationBodyInterface,
)
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class SimulationBody(SimulationBodyInterface):
    """MuJoCo implementation of SimulationBodyInterface."""

    def __init__(self):
        super().__init__()
        self.body_name: str | None = None
        self.body_id: int | None = None
        self.model: mj.MjModel | None = None
        self.data: mj.MjData | None = None

    def _get_body_id(self) -> int:
        """Get MuJoCo body ID from name."""
        if self.model and self.body_name:
            try:
                return mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_BODY, self.body_name)
            except:
                return -1
        return -1

    def get_position(self) -> Point:
        """Get the current position of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                pos = self.data.xpos[body_id]
                return Point(pos[0], pos[1], pos[2])
        return Point(0, 0, 0)

    def set_position(self, position: Point | tuple[float, float, float]) -> None:
        """Set the position of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                if isinstance(position, Point):
                    pos = np.array([position.x, position.y, position.z])
                else:
                    pos = np.array(position)

                # For MuJoCo, we need to set qpos for free bodies
                # This is a simplified implementation
                if body_id < len(self.data.qpos):
                    self.data.qpos[body_id * 7 : body_id * 7 + 3] = pos

    def get_orientation(self) -> tuple[float, float, float, float]:
        """Get the current orientation of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                quat = self.data.xquat[body_id]
                return (quat[1], quat[2], quat[3], quat[0])  # Convert to (x,y,z,w)
        return (0, 0, 0, 1)

    def set_orientation(self, orientation: tuple[float, float, float, float]) -> None:
        """Set the orientation of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                # Convert from (x,y,z,w) to MuJoCo (w,x,y,z)
                quat = np.array(
                    [orientation[3], orientation[0], orientation[1], orientation[2]]
                )

                # Set quaternion in qpos for free bodies
                if body_id < len(self.data.qpos):
                    self.data.qpos[body_id * 7 + 3 : body_id * 7 + 7] = quat

    def get_linear_velocity(self) -> Point:
        """Get the current linear velocity of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0 and body_id < len(self.data.cvel):
                vel = self.data.cvel[body_id][:3]  # Linear velocity
                return Point(vel[0], vel[1], vel[2])
        return Point(0, 0, 0)

    def set_linear_velocity(self, velocity: Point | tuple[float, float, float]) -> None:
        """Set the linear velocity of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                if isinstance(velocity, Point):
                    vel = np.array([velocity.x, velocity.y, velocity.z])
                else:
                    vel = np.array(velocity)

                # Set velocity in qvel for free bodies
                if body_id < len(self.data.qvel):
                    self.data.qvel[body_id * 6 : body_id * 6 + 3] = vel

    def get_angular_velocity(self) -> Point:
        """Get the current angular velocity of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0 and body_id < len(self.data.cvel):
                vel = self.data.cvel[body_id][3:]  # Angular velocity
                return Point(vel[0], vel[1], vel[2])
        return Point(0, 0, 0)

    def set_angular_velocity(
        self, velocity: Point | tuple[float, float, float]
    ) -> None:
        """Set the angular velocity of the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                if isinstance(velocity, Point):
                    vel = np.array([velocity.x, velocity.y, velocity.z])
                else:
                    vel = np.array(velocity)

                # Set angular velocity in qvel for free bodies
                if body_id < len(self.data.qvel):
                    self.data.qvel[body_id * 6 + 3 : body_id * 6 + 6] = vel

    def apply_force(
        self,
        force: Point | tuple[float, float, float],
        position: Point | tuple[float, float, float] | None = None,
    ) -> None:
        """Apply a force to the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                if isinstance(force, Point):
                    force_vec = np.array([force.x, force.y, force.z])
                else:
                    force_vec = np.array(force)

                # Apply external force
                if body_id < len(self.data.xfrc_applied):
                    self.data.xfrc_applied[body_id][:3] += force_vec

    def apply_torque(self, torque: Point | tuple[float, float, float]) -> None:
        """Apply a torque to the body."""
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                if isinstance(torque, Point):
                    torque_vec = np.array([torque.x, torque.y, torque.z])
                else:
                    torque_vec = np.array(torque)

                # Apply external torque
                if body_id < len(self.data.xfrc_applied):
                    self.data.xfrc_applied[body_id][3:] += torque_vec

    def apply_impulse(
        self,
        impulse: Point | tuple[float, float, float],
        position: Point | tuple[float, float, float] | None = None,
    ) -> None:
        """Apply an impulse to the body."""
        # MuJoCo doesn't have direct impulse - simulate with force
        self.apply_force(impulse, position)

    def get_mass(self) -> float:
        """Get the mass of the body."""
        if self.model:
            body_id = self._get_body_id()
            if body_id >= 0 and body_id < len(self.model.body_mass):
                return self.model.body_mass[body_id]
        return self.mass

    def set_mass(self, mass: float) -> None:
        """Set the mass of the body."""
        self.mass = mass
        # MuJoCo requires model recompilation to change mass

    def get_inertia(self) -> tuple[float, float, float]:
        """Get the inertia tensor diagonal of the body."""
        if self.model:
            body_id = self._get_body_id()
            if body_id >= 0 and body_id < len(self.model.body_inertia):
                inertia = self.model.body_inertia[body_id]
                return (inertia[0], inertia[1], inertia[2])
        return (self.mass, self.mass, self.mass)

    def set_inertia(self, inertia: tuple[float, float, float]) -> None:
        """Set the inertia tensor diagonal of the body."""
        # MuJoCo requires model recompilation to change inertia
        pass

    def set_friction(self, friction: float) -> None:
        """Set the friction coefficient of the body."""
        # MuJoCo friction is set per geom, not per body
        pass

    def set_restitution(self, restitution: float) -> None:
        """Set the restitution of the body."""
        # MuJoCo doesn't have direct restitution control
        pass

    def set_static(self, is_static: bool) -> None:
        """Set whether the body is static."""
        self.is_static = is_static
        # MuJoCo handles static bodies through body type

    def set_kinematic(self, is_kinematic: bool) -> None:
        """Set whether the body is kinematic."""
        self.is_kinematic = is_kinematic

    def get_contact_points(self) -> list[dict[str, Any]]:
        """Get contact points for this body."""
        contacts = []
        if self.model and self.data:
            body_id = self._get_body_id()
            if body_id >= 0:
                for i in range(self.data.ncon):
                    contact = self.data.contact[i]
                    if contact.geom1 == body_id or contact.geom2 == body_id:
                        contact_info = {
                            "position": contact.pos.copy(),
                            "normal": contact.frame[:3].copy(),
                            "distance": contact.dist,
                            "force": 0.0,  # Would need to calculate from contact forces
                        }
                        contacts.append(contact_info)
        return contacts

    def enable_collision(self, enable: bool = True) -> None:
        """Enable or disable collision detection for this body."""
        # MuJoCo collision is controlled through geom properties
        pass

    def remove(self) -> None:
        """Remove this body from the simulation."""
        # MuJoCo requires model recompilation to remove bodies
        pass

    def __repr__(self) -> str:
        return f"<MuJoCoSimulationBody: {self.name or 'Unnamed'}, ID: {self.body_id}, Mass: {self.mass}kg>"
