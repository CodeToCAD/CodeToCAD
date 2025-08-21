"""
PyBullet implementation of SimulationBodyInterface.
"""

from typing import TYPE_CHECKING, Any, List, Dict, Optional
from codetocad.interfaces.simulation.simulation_body_interface import (
    SimulationBodyInterface,
)
from codetocad.core.dimensions.point import Point
from codetocad.adapters.pybullet.pybullet_actions import body_management

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class SimulationBody(SimulationBodyInterface):
    """PyBullet implementation of SimulationBodyInterface."""

    def __init__(self):
        super().__init__()
        self.body_id: Optional[int] = None

    def get_position(self) -> Point:
        """Get the current position of the body."""
        if self.body_id is None:
            return Point(0, 0, 0)

        position, _ = body_management.get_body_position(self.body_id)
        return position

    def set_position(self, position: Point | tuple[float, float, float]) -> None:
        """Set the position of the body."""
        if self.body_id is None:
            return

        body_management.set_body_position(self.body_id, position)

    def get_orientation(self) -> tuple[float, float, float, float]:
        """Get the current orientation of the body."""
        if self.body_id is None:
            return (0, 0, 0, 1)

        _, orientation = body_management.get_body_position(self.body_id)
        return orientation

    def set_orientation(self, orientation: tuple[float, float, float, float]) -> None:
        """Set the orientation of the body."""
        if self.body_id is None:
            return

        current_pos = self.get_position()
        body_management.set_body_position(self.body_id, current_pos, orientation)

    def get_linear_velocity(self) -> Point:
        """Get the current linear velocity of the body."""
        if self.body_id is None:
            return Point(0, 0, 0)

        linear_vel, _ = body_management.get_body_velocity(self.body_id)
        return linear_vel

    def set_linear_velocity(self, velocity: Point | tuple[float, float, float]) -> None:
        """Set the linear velocity of the body."""
        if self.body_id is None:
            return

        current_angular_vel = self.get_angular_velocity()
        body_management.set_body_velocity(self.body_id, velocity, current_angular_vel)

    def get_angular_velocity(self) -> Point:
        """Get the current angular velocity of the body."""
        if self.body_id is None:
            return Point(0, 0, 0)

        _, angular_vel = body_management.get_body_velocity(self.body_id)
        return angular_vel

    def set_angular_velocity(
        self, velocity: Point | tuple[float, float, float]
    ) -> None:
        """Set the angular velocity of the body."""
        if self.body_id is None:
            return

        current_linear_vel = self.get_linear_velocity()
        body_management.set_body_velocity(self.body_id, current_linear_vel, velocity)

    def apply_force(
        self,
        force: Point | tuple[float, float, float],
        position: Point | tuple[float, float, float] | None = None,
    ) -> None:
        """Apply a force to the body."""
        if self.body_id is None:
            return

        body_management.apply_force_to_body(self.body_id, force, position)

    def apply_torque(self, torque: Point | tuple[float, float, float]) -> None:
        """Apply a torque to the body."""
        if self.body_id is None:
            return

        body_management.apply_torque_to_body(self.body_id, torque)

    def apply_impulse(
        self,
        impulse: Point | tuple[float, float, float],
        position: Point | tuple[float, float, float] | None = None,
    ) -> None:
        """Apply an impulse to the body."""
        # PyBullet doesn't have direct impulse application
        # We simulate it by applying force for one time step
        self.apply_force(impulse, position)

    def get_mass(self) -> float:
        """Get the mass of the body."""
        if self.body_id is None:
            return self.mass

        return body_management.get_body_mass(self.body_id)

    def set_mass(self, mass: float) -> None:
        """Set the mass of the body."""
        self.mass = mass
        if self.body_id is not None:
            body_management.set_body_mass(self.body_id, mass)

    def get_inertia(self) -> tuple[float, float, float]:
        """Get the inertia tensor diagonal of the body."""
        # PyBullet doesn't provide direct inertia access
        # Return default values based on mass
        return (self.mass, self.mass, self.mass)

    def set_inertia(self, inertia: tuple[float, float, float]) -> None:
        """Set the inertia tensor diagonal of the body."""
        # PyBullet doesn't allow direct inertia modification after creation
        # This would need to be set during body creation
        pass

    def set_friction(self, friction: float) -> None:
        """Set the friction coefficient of the body."""
        if self.body_id is not None:
            body_management.set_body_friction(self.body_id, friction)

    def set_restitution(self, restitution: float) -> None:
        """Set the restitution (bounciness) of the body."""
        if self.body_id is not None:
            body_management.set_body_restitution(self.body_id, restitution)

    def set_static(self, is_static: bool) -> None:
        """Set whether the body is static (immovable)."""
        self.is_static = is_static
        if self.body_id is not None:
            if is_static:
                # Set mass to 0 to make it static
                body_management.set_body_mass(self.body_id, 0.0)
            else:
                # Restore original mass
                body_management.set_body_mass(self.body_id, self.mass)

    def set_kinematic(self, is_kinematic: bool) -> None:
        """Set whether the body is kinematic (position controlled)."""
        self.is_kinematic = is_kinematic
        # PyBullet handles kinematic bodies through mass = 0 and position control
        if is_kinematic:
            self.set_static(True)

    def get_contact_points(self) -> List[Dict[str, Any]]:
        """Get contact points for this body."""
        if self.body_id is None:
            return []

        return body_management.get_contact_points(self.body_id)

    def enable_collision(self, enable: bool = True) -> None:
        """Enable or disable collision detection for this body."""
        # PyBullet doesn't have a direct collision enable/disable
        # This would typically be handled through collision groups/masks
        pass

    def remove(self) -> None:
        """Remove this body from the simulation."""
        if self.body_id is not None:
            body_management.remove_body(self.body_id)
            self.body_id = None

    def __repr__(self) -> str:
        return f"<PyBulletSimulationBody: {self.name or 'Unnamed'}, ID: {self.body_id}, Mass: {self.mass}kg>"
