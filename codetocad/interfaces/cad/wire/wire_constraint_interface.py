"""
Wire constraint interface for geometric constraint functionality.

This interface provides methods for applying geometric constraints to wires,
such as tangent, parallel, perpendicular, coincident, and distance constraints.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


class ConstraintType(Enum):
    """Types of geometric constraints that can be applied to wires."""

    TANGENT = "tangent"
    PARALLEL = "parallel"
    PERPENDICULAR = "perpendicular"
    COINCIDENT = "coincident"
    DISTANCE = "distance"
    LENGTH = "length"
    CONTINUITY = "continuity"


class ConstraintStatus(Enum):
    """Status of a geometric constraint."""

    ACTIVE = "active"
    SUPPRESSED = "suppressed"
    FAILED = "failed"
    UNDEFINED = "undefined"


class WireConstraintInterface(ABC):
    """
    Interface for applying geometric constraints to wires.

    Provides methods for creating and managing geometric constraints
    that control wire shape, position, and relationships to other entities.
    """

    def __init__(self, wire: "WireInterface"):
        """
        Initialize the wire constraint interface.

        Args:
            wire: The wire this constraint interface belongs to
        """
        self.wire = wire
        self.constraints: dict[str, "GeometricConstraint"] = {}
        self._constraint_counter = 0

    @abstractmethod
    def tangent(
        self, target_entity: Any, point: Any, name: str | None = None
    ) -> "GeometricConstraint" | None:
        """
        Create a tangent constraint between the wire and another entity.

        Args:
            target_entity: The entity to be tangent to (curve, surface, etc.)
            point: The point where tangency should occur
            name: Optional name for the constraint

        Returns:
            Created tangent constraint or None if creation failed
        """
        pass

    @abstractmethod
    def parallel(
        self, reference_entity: Any, name: str | None = None
    ) -> "GeometricConstraint" | None:
        """
        Create a parallel constraint between the wire and a reference entity.

        Args:
            reference_entity: The entity to be parallel to (line, edge, etc.)
            name: Optional name for the constraint

        Returns:
            Created parallel constraint or None if creation failed
        """
        pass

    @abstractmethod
    def perpendicular(
        self, reference_entity: Any, name: str | None = None
    ) -> "GeometricConstraint" | None:
        """
        Create a perpendicular constraint between the wire and a reference entity.

        Args:
            reference_entity: The entity to be perpendicular to
            name: Optional name for the constraint

        Returns:
            Created perpendicular constraint or None if creation failed
        """
        pass

    @abstractmethod
    def coincident(
        self, target_point: Any, wire_point: Any = None, name: str | None = None
    ) -> "GeometricConstraint" | None:
        """
        Create a coincident constraint between wire point and target point.

        Args:
            target_point: The point to be coincident with
            wire_point: Point on wire (start, end, or parameter). If None, uses closest point
            name: Optional name for the constraint

        Returns:
            Created coincident constraint or None if creation failed
        """
        pass

    @abstractmethod
    def distance(
        self, target_entity: Any, distance_value: float, name: str | None = None
    ) -> "GeometricConstraint" | None:
        """
        Create a distance constraint between the wire and another entity.

        Args:
            target_entity: The entity to maintain distance from
            distance_value: The distance to maintain
            name: Optional name for the constraint

        Returns:
            Created distance constraint or None if creation failed
        """
        pass

    @abstractmethod
    def length(
        self, length_value: float, name: str | None = None
    ) -> "GeometricConstraint" | None:
        """
        Create a length constraint for the wire.

        Args:
            length_value: The target length for the wire
            name: Optional name for the constraint

        Returns:
            Created length constraint or None if creation failed
        """
        pass

    @abstractmethod
    def continuity(
        self,
        other_wire: "WireInterface",
        continuity_order: int = 1,
        name: str | None = None,
    ) -> "GeometricConstraint" | None:
        """
        Create a continuity constraint between this wire and another wire.

        Args:
            other_wire: The wire to maintain continuity with
            continuity_order: Order of continuity (0=position, 1=tangent, 2=curvature)
            name: Optional name for the constraint

        Returns:
            Created continuity constraint or None if creation failed
        """
        pass

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

    def get_constraint(self, name: str) -> "GeometricConstraint" | None:
        """
        Get a constraint by name.

        Args:
            name: Name of the constraint

        Returns:
            Constraint instance or None if not found
        """
        return self.constraints.get(name)

    def get_all_constraints(self) -> list["GeometricConstraint"]:
        """
        Get all constraints applied to this wire.

        Returns:
            List of all constraints
        """
        return list(self.constraints.values())

    def validate_constraints(self) -> dict[str, bool]:
        """
        Validate all constraints applied to this wire.

        Returns:
            Dictionary mapping constraint names to their validity status
        """
        validation_results = {}
        for name, constraint in self.constraints.items():
            validation_results[name] = constraint.is_valid()
        return validation_results

    def solve_constraints(self) -> bool:
        """
        Solve all active constraints applied to this wire.

        Returns:
            True if all constraints were solved successfully, False otherwise
        """
        success = True
        for constraint in self.constraints.values():
            if constraint.status == ConstraintStatus.ACTIVE:
                if not constraint.solve():
                    success = False
        return success

    def clear_all_constraints(self) -> bool:
        """
        Remove all constraints from this wire.

        Returns:
            True if all constraints were removed successfully, False otherwise
        """
        constraint_names = list(self.constraints.keys())
        success = True
        for name in constraint_names:
            if not self.remove_constraint(name):
                success = False
        return success

    def _generate_constraint_name(self, constraint_type: ConstraintType) -> str:
        """
        Generate a unique name for a constraint.

        Args:
            constraint_type: Type of constraint

        Returns:
            Generated unique name
        """
        self._constraint_counter += 1
        return f"{constraint_type.value}_{self._constraint_counter}"


class GeometricConstraint(ABC):
    """
    Base class for geometric constraints applied to wires.
    """

    def __init__(
        self,
        name: str,
        constraint_type: ConstraintType,
        wire: "WireInterface",
        **parameters,
    ):
        """
        Initialize a geometric constraint.

        Args:
            name: Unique name for this constraint
            constraint_type: Type of constraint
            wire: The wire this constraint applies to
            **parameters: Constraint-specific parameters
        """
        self.name = name
        self.constraint_type = constraint_type
        self.wire = wire
        self.parameters = parameters
        self.status = ConstraintStatus.UNDEFINED

    @abstractmethod
    def apply(self) -> bool:
        """
        Apply the constraint to the wire.

        Returns:
            True if constraint was applied successfully, False otherwise
        """
        pass

    @abstractmethod
    def remove(self) -> bool:
        """
        Remove the constraint from the wire.

        Returns:
            True if constraint was removed successfully, False otherwise
        """
        pass

    @abstractmethod
    def solve(self) -> bool:
        """
        Solve the constraint equations.

        Returns:
            True if constraint was solved successfully, False otherwise
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

    def suppress(self) -> bool:
        """
        Suppress the constraint (temporarily disable it).

        Returns:
            True if constraint was suppressed successfully, False otherwise
        """
        if self.status == ConstraintStatus.ACTIVE:
            self.status = ConstraintStatus.SUPPRESSED
            return True
        return False

    def unsuppress(self) -> bool:
        """
        Unsuppress the constraint (re-enable it).

        Returns:
            True if constraint was unsuppressed successfully, False otherwise
        """
        if self.status == ConstraintStatus.SUPPRESSED:
            self.status = ConstraintStatus.ACTIVE
            return True
        return False

    def update_parameters(self, **kwargs) -> bool:
        """
        Update constraint parameters.

        Args:
            **kwargs: Updated parameters

        Returns:
            True if parameters were updated successfully, False otherwise
        """
        try:
            self.parameters.update(kwargs)
            # Re-apply constraint with new parameters if it's active
            if self.status == ConstraintStatus.ACTIVE:
                return self.apply()
            return True
        except Exception:
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
