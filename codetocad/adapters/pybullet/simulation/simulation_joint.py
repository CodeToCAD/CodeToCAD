"""
PyBullet implementation of SimulationJointInterface.
"""

from typing import TYPE_CHECKING, Optional
import pybullet as p
from codetocad.interfaces.simulation.simulation_joint_interface import (
    SimulationJointInterface,
    JointType,
)
from codetocad.core.dimensions.point import Point
from codetocad.adapters.pybullet.pybullet_actions import joint_management

if TYPE_CHECKING:
    from codetocad.adapters.pybullet.simulation.simulation_body import SimulationBody


class SimulationJoint(SimulationJointInterface):
    """PyBullet implementation of SimulationJointInterface."""

    def __init__(self):
        super().__init__()
        self.constraint_id: int | None = None
        self.body_id: int | None = None
        self.joint_index: int | None = None

    def create_fixed_joint(
        self,
        parent_body: "SimulationBody",
        child_body: "SimulationBody",
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """Create a fixed joint between two bodies."""
        self.joint_type = JointType.FIXED
        self.parent_body = parent_body
        self.child_body = child_body

        if parent_body.body_id is not None and child_body.body_id is not None:
            self.constraint_id = joint_management.create_fixed_joint(
                parent_body.body_id,
                child_body.body_id,
                parent_frame,
                child_frame,
                **kwargs,
            )

    def create_revolute_joint(
        self,
        parent_body: "SimulationBody",
        child_body: "SimulationBody",
        axis: Point | tuple[float, float, float],
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        lower_limit: float | None = None,
        upper_limit: float | None = None,
        **kwargs,
    ) -> None:
        """Create a revolute joint between two bodies."""
        self.joint_type = JointType.REVOLUTE
        self.parent_body = parent_body
        self.child_body = child_body

        if parent_body.body_id is not None and child_body.body_id is not None:
            self.constraint_id = joint_management.create_revolute_joint(
                parent_body.body_id,
                child_body.body_id,
                axis,
                parent_frame,
                child_frame,
                **kwargs,
            )

    def create_prismatic_joint(
        self,
        parent_body: "SimulationBody",
        child_body: "SimulationBody",
        axis: Point | tuple[float, float, float],
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        lower_limit: float | None = None,
        upper_limit: float | None = None,
        **kwargs,
    ) -> None:
        """Create a prismatic joint between two bodies."""
        self.joint_type = JointType.PRISMATIC
        self.parent_body = parent_body
        self.child_body = child_body

        if parent_body.body_id is not None and child_body.body_id is not None:
            self.constraint_id = joint_management.create_prismatic_joint(
                parent_body.body_id,
                child_body.body_id,
                axis,
                parent_frame,
                child_frame,
                **kwargs,
            )

    def create_spherical_joint(
        self,
        parent_body: "SimulationBody",
        child_body: "SimulationBody",
        parent_frame: Point | tuple[float, float, float] = (0, 0, 0),
        child_frame: Point | tuple[float, float, float] = (0, 0, 0),
        **kwargs,
    ) -> None:
        """Create a spherical joint between two bodies."""
        self.joint_type = JointType.SPHERICAL
        self.parent_body = parent_body
        self.child_body = child_body

        if parent_body.body_id is not None and child_body.body_id is not None:
            self.constraint_id = joint_management.create_spherical_joint(
                parent_body.body_id,
                child_body.body_id,
                parent_frame,
                child_frame,
                **kwargs,
            )

    def get_position(self) -> float:
        """Get the current joint position."""
        if self.body_id is not None and self.joint_index is not None:
            return joint_management.get_joint_position(self.body_id, self.joint_index)
        return 0.0

    def set_position(self, position: float) -> None:
        """Set the joint position."""
        if self.body_id is not None and self.joint_index is not None:
            joint_management.set_joint_motor_control(
                self.body_id,
                self.joint_index,
                p.POSITION_CONTROL,
                target_position=position,
            )

    def get_velocity(self) -> float:
        """Get the current joint velocity."""
        if self.body_id is not None and self.joint_index is not None:
            return joint_management.get_joint_velocity(self.body_id, self.joint_index)
        return 0.0

    def set_velocity(self, velocity: float) -> None:
        """Set the joint velocity."""
        if self.body_id is not None and self.joint_index is not None:
            joint_management.set_joint_velocity(
                self.body_id, self.joint_index, velocity
            )

    def apply_force(self, force: float) -> None:
        """Apply a force/torque to the joint."""
        if self.body_id is not None and self.joint_index is not None:
            joint_management.apply_joint_force(self.body_id, self.joint_index, force)

    def set_limits(self, lower: float | None, upper: float | None) -> None:
        """Set joint limits."""
        if (
            self.body_id is not None
            and self.joint_index is not None
            and lower is not None
            and upper is not None
        ):
            joint_management.set_joint_limits(
                self.body_id, self.joint_index, lower, upper
            )

    def get_limits(self) -> tuple[float | None, float | None]:
        """Get joint limits."""
        if self.body_id is not None and self.joint_index is not None:
            return joint_management.get_joint_limits(self.body_id, self.joint_index)
        return (None, None)

    def set_stiffness(self, stiffness: float) -> None:
        """Set joint stiffness."""
        # PyBullet handles stiffness through PID gains
        pass

    def set_damping(self, damping: float) -> None:
        """Set joint damping."""
        # PyBullet handles damping through joint properties
        pass

    def enable(self) -> None:
        """Enable the joint."""
        self.is_enabled = True

    def disable(self) -> None:
        """Disable the joint."""
        self.is_enabled = False

    def remove(self) -> None:
        """Remove the joint from the simulation."""
        if self.constraint_id is not None:
            joint_management.remove_joint(self.constraint_id)
            self.constraint_id = None
