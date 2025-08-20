"""
Blender constraint interface for kinematic and geometric constraint functionality.

This interface provides methods for applying constraints to Blender objects,
such as location, rotation, scale, distance, alignment, and transformation constraints.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Tuple

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class BlenderConstraintType(Enum):
    """Types of constraints that can be applied to Blender objects."""

    # Kinematic Constraints
    COPY_LOCATION = "copy_location"
    COPY_ROTATION = "copy_rotation"
    COPY_SCALE = "copy_scale"
    LIMIT_LOCATION = "limit_location"
    LIMIT_ROTATION = "limit_rotation"
    LIMIT_SCALE = "limit_scale"
    TRACK_TO = "track_to"
    LOCKED_TRACK = "locked_track"
    DAMPED_TRACK = "damped_track"

    # Geometric Constraints
    MAINTAIN_DISTANCE = "maintain_distance"
    PARALLEL_ALIGNMENT = "parallel_alignment"
    PERPENDICULAR_ALIGNMENT = "perpendicular_alignment"
    COINCIDENT_CENTERS = "coincident_centers"
    COINCIDENT_SURFACES = "coincident_surfaces"
    FOLLOW_PATH = "follow_path"

    # Transformation Constraints
    CHILD_OF = "child_of"
    PIVOT = "pivot"
    FLOOR = "floor"
    SHRINKWRAP = "shrinkwrap"
    CLAMP_TO = "clamp_to"


class BlenderConstraintStatus(Enum):
    """Status of a Blender constraint."""

    ACTIVE = "active"
    MUTED = "muted"
    DISABLED = "disabled"
    ERROR = "error"
    UNDEFINED = "undefined"


class BlenderConstraintInterface(ABC):
    """
    Interface for applying constraints to Blender objects.

    Provides methods for creating and managing kinematic and geometric constraints
    that control object transformations and relationships.
    """

    def __init__(self, blender_object: Any):
        """
        Initialize the Blender constraint interface.

        Args:
            blender_object: The Blender object this constraint interface belongs to
        """
        self.blender_object = blender_object
        self.constraints: dict[str, "BlenderConstraint"] = {}
        self._constraint_counter = 0

    # Kinematic Constraints

    @abstractmethod
    def copy_location(
        self,
        target_object: Any,
        use_x: bool = True,
        use_y: bool = True,
        use_z: bool = True,
        use_offset: bool = False,
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a copy location constraint.

        Args:
            target_object: Object to copy location from
            use_x: Copy X coordinate
            use_y: Copy Y coordinate
            use_z: Copy Z coordinate
            use_offset: Add to existing location instead of replacing
            influence: Constraint influence (0.0 to 1.0)
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    @abstractmethod
    def copy_rotation(
        self,
        target_object: Any,
        use_x: bool = True,
        use_y: bool = True,
        use_z: bool = True,
        use_offset: bool = False,
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a copy rotation constraint.

        Args:
            target_object: Object to copy rotation from
            use_x: Copy X rotation
            use_y: Copy Y rotation
            use_z: Copy Z rotation
            use_offset: Add to existing rotation instead of replacing
            influence: Constraint influence (0.0 to 1.0)
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    @abstractmethod
    def copy_scale(
        self,
        target_object: Any,
        use_x: bool = True,
        use_y: bool = True,
        use_z: bool = True,
        use_offset: bool = False,
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a copy scale constraint.

        Args:
            target_object: Object to copy scale from
            use_x: Copy X scale
            use_y: Copy Y scale
            use_z: Copy Z scale
            use_offset: Add to existing scale instead of replacing
            influence: Constraint influence (0.0 to 1.0)
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    @abstractmethod
    def limit_location(
        self,
        min_x: float | None = None,
        max_x: float | None = None,
        min_y: float | None = None,
        max_y: float | None = None,
        min_z: float | None = None,
        max_z: float | None = None,
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a limit location constraint.

        Args:
            min_x: Minimum X location
            max_x: Maximum X location
            min_y: Minimum Y location
            max_y: Maximum Y location
            min_z: Minimum Z location
            max_z: Maximum Z location
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    @abstractmethod
    def track_to(
        self,
        target_object: Any,
        track_axis: str = "TRACK_NEGATIVE_Z",
        up_axis: str = "UP_Y",
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a track to constraint.

        Args:
            target_object: Object to track
            track_axis: Axis that points to target
            up_axis: Axis that points up
            influence: Constraint influence (0.0 to 1.0)
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    # Geometric Constraints

    @abstractmethod
    def maintain_distance(
        self, target_object: Any, distance: float, name: str | None = None
    ) -> "BlenderConstraint | None":
        """
        Create a constraint to maintain distance from target object.

        Args:
            target_object: Object to maintain distance from
            distance: Distance to maintain
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    @abstractmethod
    def follow_path(
        self,
        curve_object: Any,
        offset: float = 0.0,
        forward_axis: str = "FORWARD_Y",
        up_axis: str = "UP_Z",
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a follow path constraint.

        Args:
            curve_object: Curve object to follow
            offset: Offset along the curve (0.0 to 1.0)
            forward_axis: Axis that points forward along path
            up_axis: Axis that points up
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    # Transformation Constraints

    @abstractmethod
    def child_of(
        self, parent_object: Any, influence: float = 1.0, name: str | None = None
    ) -> "BlenderConstraint | None":
        """
        Create a child of constraint.

        Args:
            parent_object: Parent object
            influence: Constraint influence (0.0 to 1.0)
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    @abstractmethod
    def floor_constraint(
        self,
        target_object: Any,
        floor_location: str = "FLOOR_NEGATIVE_Y",
        use_rotation: bool = False,
        name: str | None = None,
    ) -> "BlenderConstraint | None":
        """
        Create a floor constraint.

        Args:
            target_object: Floor object
            floor_location: Which side is the floor
            use_rotation: Use target's rotation
            name: Optional name for the constraint

        Returns:
            Created constraint or None if creation failed
        """
        pass

    # Constraint Management Methods

    def remove_constraint(self, constraint_name: str) -> bool:
        """
        Remove a constraint by name.

        Args:
            constraint_name: Name of the constraint to remove

        Returns:
            True if constraint was removed successfully, False otherwise
        """
        if constraint_name in self.constraints:
            constraint = self.constraints[constraint_name]
            if constraint.remove():
                del self.constraints[constraint_name]
                return True
        return False

    def get_constraint(self, name: str) -> "BlenderConstraint | None":
        """
        Get a constraint by name.

        Args:
            name: Name of the constraint

        Returns:
            Constraint instance or None if not found
        """
        return self.constraints.get(name)

    def get_all_constraints(self) -> list["BlenderConstraint"]:
        """
        Get all constraints applied to this object.

        Returns:
            List of all constraints
        """
        return list(self.constraints.values())

    def clear_all_constraints(self) -> bool:
        """
        Remove all constraints from this object.

        Returns:
            True if all constraints were removed successfully, False otherwise
        """
        constraint_names = list(self.constraints.keys())
        success = True
        for name in constraint_names:
            if not self.remove_constraint(name):
                success = False
        return success

    def _generate_constraint_name(self, constraint_type: BlenderConstraintType) -> str:
        """
        Generate a unique name for a constraint.

        Args:
            constraint_type: Type of constraint

        Returns:
            Generated unique name
        """
        self._constraint_counter += 1
        return f"{constraint_type.value}_{self._constraint_counter}"


class BlenderConstraint(ABC):
    """
    Base class for Blender constraints.
    """

    def __init__(
        self,
        name: str,
        constraint_type: BlenderConstraintType,
        blender_object: Any,
        **parameters,
    ):
        """
        Initialize a Blender constraint.

        Args:
            name: Unique name for this constraint
            constraint_type: Type of constraint
            blender_object: The Blender object this constraint applies to
            **parameters: Constraint-specific parameters
        """
        self.name = name
        self.constraint_type = constraint_type
        self.blender_object = blender_object
        self.parameters = parameters
        self.status = BlenderConstraintStatus.UNDEFINED
        self.native_constraint = None  # Will hold the actual Blender constraint

    @abstractmethod
    def apply(self) -> bool:
        """
        Apply the constraint to the Blender object.

        Returns:
            True if constraint was applied successfully, False otherwise
        """
        pass

    @abstractmethod
    def remove(self) -> bool:
        """
        Remove the constraint from the Blender object.

        Returns:
            True if constraint was removed successfully, False otherwise
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Check if the constraint is valid.

        Returns:
            True if constraint is valid, False otherwise
        """
        pass

    def mute(self) -> bool:
        """
        Mute the constraint (disable temporarily).

        Returns:
            True if constraint was muted successfully, False otherwise
        """
        if self.native_constraint and self.status == BlenderConstraintStatus.ACTIVE:
            try:
                self.native_constraint.mute = True
                self.status = BlenderConstraintStatus.MUTED
                return True
            except Exception:
                return False
        return False

    def unmute(self) -> bool:
        """
        Unmute the constraint (re-enable).

        Returns:
            True if constraint was unmuted successfully, False otherwise
        """
        if self.native_constraint and self.status == BlenderConstraintStatus.MUTED:
            try:
                self.native_constraint.mute = False
                self.status = BlenderConstraintStatus.ACTIVE
                return True
            except Exception:
                return False
        return False

    def set_influence(self, influence: float) -> bool:
        """
        Set the constraint influence.

        Args:
            influence: Influence value (0.0 to 1.0)

        Returns:
            True if influence was set successfully, False otherwise
        """
        if self.native_constraint:
            try:
                self.native_constraint.influence = max(0.0, min(1.0, influence))
                self.parameters["influence"] = influence
                return True
            except Exception:
                return False
        return False

    def __str__(self) -> str:
        """String representation of the constraint."""
        return f"{self.constraint_type.value.title()}Constraint({self.name})"

    def __repr__(self) -> str:
        """Detailed string representation of the constraint."""
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"type={self.constraint_type.value}, "
            f"status={self.status.value})"
        )
