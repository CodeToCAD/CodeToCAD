"""
MuJoCo implementation of SimulationJointInterface.
"""

from typing import TYPE_CHECKING, Optional
import mujoco as mj
from codetocad.interfaces.simulation.simulation_joint_interface import (
    SimulationJointInterface,
    JointType,
)
from codetocad.core.dimensions.point import Point

if TYPE_CHECKING:
    from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody


class SimulationJoint(SimulationJointInterface):
    """MuJoCo implementation of SimulationJointInterface."""

    def __init__(self):
        super().__init__()
        self.joint_name: str | None = None
        self.joint_id: int | None = None
        self.model: mj.MjModel | None = None
        self.data: mj.MjData | None = None

    def create_fixed_joint(
        self,
        parent_body,
        child_body,
        parent_frame=(0, 0, 0),
        child_frame=(0, 0, 0),
        **kwargs,
    ):
        """Create a fixed joint between two bodies."""
        self.joint_type = JointType.FIXED
        self.parent_body = parent_body
        self.child_body = child_body

    def create_revolute_joint(
        self,
        parent_body,
        child_body,
        axis,
        parent_frame=(0, 0, 0),
        child_frame=(0, 0, 0),
        lower_limit=None,
        upper_limit=None,
        **kwargs,
    ):
        """Create a revolute joint between two bodies."""
        self.joint_type = JointType.REVOLUTE
        self.parent_body = parent_body
        self.child_body = child_body

    def create_prismatic_joint(
        self,
        parent_body,
        child_body,
        axis,
        parent_frame=(0, 0, 0),
        child_frame=(0, 0, 0),
        lower_limit=None,
        upper_limit=None,
        **kwargs,
    ):
        """Create a prismatic joint between two bodies."""
        self.joint_type = JointType.PRISMATIC
        self.parent_body = parent_body
        self.child_body = child_body

    def create_spherical_joint(
        self,
        parent_body,
        child_body,
        parent_frame=(0, 0, 0),
        child_frame=(0, 0, 0),
        **kwargs,
    ):
        """Create a spherical joint between two bodies."""
        self.joint_type = JointType.SPHERICAL
        self.parent_body = parent_body
        self.child_body = child_body

    def get_position(self) -> float:
        """Get the current joint position."""
        return 0.0

    def set_position(self, position: float) -> None:
        """Set the joint position."""
        pass

    def get_velocity(self) -> float:
        """Get the current joint velocity."""
        return 0.0

    def set_velocity(self, velocity: float) -> None:
        """Set the joint velocity."""
        pass

    def apply_force(self, force: float) -> None:
        """Apply a force/torque to the joint."""
        pass

    def set_limits(self, lower: float | None, upper: float | None) -> None:
        """Set joint limits."""
        pass

    def get_limits(self) -> tuple[float | None, float | None]:
        """Get joint limits."""
        return (None, None)

    def set_stiffness(self, stiffness: float) -> None:
        """Set joint stiffness."""
        pass

    def set_damping(self, damping: float) -> None:
        """Set joint damping."""
        pass

    def enable(self) -> None:
        """Enable the joint."""
        self.is_enabled = True

    def disable(self) -> None:
        """Disable the joint."""
        self.is_enabled = False

    def remove(self) -> None:
        """Remove the joint from the simulation."""
        pass
