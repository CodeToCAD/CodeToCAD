"""
build123d implementation of WireConstraintInterface.

This module provides concrete implementations of geometric constraints
for wires using build123d's constraint solving capabilities.
"""

from typing import TYPE_CHECKING, Any
import math

from codetocad.interfaces.cad.wire.wire_constraint import (
    WireConstraintInterface,
    GeometricConstraint,
    ConstraintType,
    ConstraintStatus,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.wire.wire import Wire
    import build123d as bd


class WireConstraint(WireConstraintInterface):
    """
    build123d implementation of WireConstraintInterface.

    Provides geometric constraint functionality for build123d wires.
    """

    def __init__(self, wire: "Wire"):
        """
        Initialize the wire constraint implementation.

        Args:
            wire: The build123d wire this constraint interface belongs to
        """
        super().__init__(wire)
        self.wire: "Wire" = wire  # Type hint for build123d wire

    def tangent_to(
        self, target_entity: Any, point: Any, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a tangent constraint between the wire and another entity.

        Args:
            target_entity: The entity to be tangent to (curve, surface, etc.)
            point: The point where tangency should occur
            name: Optional name for the constraint

        Returns:
            Created tangent constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.TANGENT)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.TANGENT,
                wire=self.wire,
                target_entity=target_entity,
                point=point,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create tangent constraint: {e}")
            return None

    def parallel_to(
        self, reference_entity: Any, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a parallel constraint between the wire and a reference entity.

        Args:
            reference_entity: The entity to be parallel to (line, edge, etc.)
            name: Optional name for the constraint

        Returns:
            Created parallel constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.PARALLEL)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.PARALLEL,
                wire=self.wire,
                reference_entity=reference_entity,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create parallel constraint: {e}")
            return None

    def perpendicular_to(
        self, reference_entity: Any, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a perpendicular constraint between the wire and a reference entity.

        Args:
            reference_entity: The entity to be perpendicular to
            name: Optional name for the constraint

        Returns:
            Created perpendicular constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.PERPENDICULAR)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.PERPENDICULAR,
                wire=self.wire,
                reference_entity=reference_entity,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create perpendicular constraint: {e}")
            return None

    def coincident_points(
        self, target_point: Any, wire_point: Any = None, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a coincident constraint between wire point and target point.

        Args:
            target_point: The point to be coincident with
            wire_point: Point on wire (start, end, or parameter). If None, uses closest point
            name: Optional name for the constraint

        Returns:
            Created coincident constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.COINCIDENT)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.COINCIDENT,
                wire=self.wire,
                target_point=target_point,
                wire_point=wire_point,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create coincident constraint: {e}")
            return None

    def distance_from(
        self, target_entity: Any, distance_value: float, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a distance constraint between the wire and another entity.

        Args:
            target_entity: The entity to maintain distance from
            distance_value: The distance to maintain
            name: Optional name for the constraint

        Returns:
            Created distance constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.DISTANCE)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.DISTANCE,
                wire=self.wire,
                target_entity=target_entity,
                distance_value=distance_value,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create distance constraint: {e}")
            return None

    def set_length(
        self, length_value: float, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a length constraint for the wire.

        Args:
            length_value: The target length for the wire
            name: Optional name for the constraint

        Returns:
            Created length constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.LENGTH)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.LENGTH,
                wire=self.wire,
                length_value=length_value,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create length constraint: {e}")
            return None

    def continuous_with(
        self, other_wire: "Wire", continuity_order: int = 1, name: str | None = None
    ) -> "Build123dConstraint|None":
        """
        Create a continuity constraint between this wire and another wire.

        Args:
            other_wire: The wire to maintain continuity with
            continuity_order: Order of continuity (0=position, 1=tangent, 2=curvature)
            name: Optional name for the constraint

        Returns:
            Created continuity constraint or None if creation failed
        """
        if name is None:
            name = self._generate_constraint_name(ConstraintType.CONTINUITY)

        try:
            constraint = Build123dConstraint(
                name=name,
                constraint_type=ConstraintType.CONTINUITY,
                wire=self.wire,
                other_wire=other_wire,
                continuity_order=continuity_order,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create continuity constraint: {e}")
            return None


class Build123dConstraint(GeometricConstraint):
    """
    build123d implementation of GeometricConstraint.

    Represents a geometric constraint applied to a build123d wire.
    """

    def __init__(
        self, name: str, constraint_type: ConstraintType, wire: "Wire", **parameters
    ):
        """
        Initialize a build123d geometric constraint.

        Args:
            name: Unique name for this constraint
            constraint_type: Type of constraint
            wire: The wire this constraint applies to
            **parameters: Constraint-specific parameters
        """
        super().__init__(name, constraint_type, wire, **parameters)
        self.wire: "Wire" = wire  # Type hint for build123d wire
        self._original_geometry = None  # Store original geometry for rollback

    def apply(self) -> bool:
        """
        Apply the constraint to the wire.

        Returns:
            True if constraint was applied successfully, False otherwise
        """
        try:
            # Store original geometry for potential rollback
            if self.wire.native_instance:
                self._original_geometry = self.wire.native_instance

            # Apply constraint based on type
            success = self._apply_constraint()

            if success:
                self.status = ConstraintStatus.ACTIVE
                return True
            else:
                self.status = ConstraintStatus.FAILED
                return False

        except Exception as e:
            print(f"Failed to apply constraint {self.name}: {e}")
            self.status = ConstraintStatus.FAILED
            return False

    def remove(self) -> bool:
        """
        Remove the constraint from the wire.

        Returns:
            True if constraint was removed successfully, False otherwise
        """
        try:
            # Restore original geometry if available
            if self._original_geometry and self.wire.native_instance:
                self.wire.native_instance = self._original_geometry

            self.status = ConstraintStatus.UNDEFINED
            return True

        except Exception as e:
            print(f"Failed to remove constraint {self.name}: {e}")
            return False

    def solve(self) -> bool:
        """
        Solve the constraint equations.

        Returns:
            True if constraint was solved successfully, False otherwise
        """
        if self.status != ConstraintStatus.ACTIVE:
            return False

        try:
            # Re-apply the constraint to solve it
            return self._apply_constraint()

        except Exception as e:
            print(f"Failed to solve constraint {self.name}: {e}")
            self.status = ConstraintStatus.FAILED
            return False

    def is_valid(self) -> bool:
        """
        Check if the constraint is valid.

        Returns:
            True if constraint is valid, False otherwise
        """
        try:
            # Basic validation - check if wire exists and has geometry
            if not self.wire or not self.wire.native_instance:
                return False

            # Constraint-specific validation
            return self._validate_constraint()

        except Exception:
            return False

    def _apply_constraint(self) -> bool:
        """
        Apply the specific constraint based on its type.

        Returns:
            True if constraint was applied successfully, False otherwise
        """
        if self.constraint_type == ConstraintType.TANGENT:
            return self._apply_tangent_constraint()
        elif self.constraint_type == ConstraintType.PARALLEL:
            return self._apply_parallel_constraint()
        elif self.constraint_type == ConstraintType.PERPENDICULAR:
            return self._apply_perpendicular_constraint()
        elif self.constraint_type == ConstraintType.COINCIDENT:
            return self._apply_coincident_constraint()
        elif self.constraint_type == ConstraintType.DISTANCE:
            return self._apply_distance_constraint()
        elif self.constraint_type == ConstraintType.LENGTH:
            return self._apply_length_constraint()
        elif self.constraint_type == ConstraintType.CONTINUITY:
            return self._apply_continuity_constraint()
        else:
            print(f"Unknown constraint type: {self.constraint_type}")
            return False

    def _validate_constraint(self) -> bool:
        """
        Validate the constraint parameters.

        Returns:
            True if constraint parameters are valid, False otherwise
        """
        if self.constraint_type == ConstraintType.TANGENT:
            return "target_entity" in self.parameters and "point" in self.parameters
        elif self.constraint_type == ConstraintType.PARALLEL:
            return "reference_entity" in self.parameters
        elif self.constraint_type == ConstraintType.PERPENDICULAR:
            return "reference_entity" in self.parameters
        elif self.constraint_type == ConstraintType.COINCIDENT:
            return "target_point" in self.parameters
        elif self.constraint_type == ConstraintType.DISTANCE:
            return (
                "target_entity" in self.parameters
                and "distance_value" in self.parameters
            )
        elif self.constraint_type == ConstraintType.LENGTH:
            return "length_value" in self.parameters
        elif self.constraint_type == ConstraintType.CONTINUITY:
            return "other_wire" in self.parameters
        return False

    def _apply_tangent_constraint(self) -> bool:
        """Apply tangent constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying tangent constraint {self.name}")
        return True

    def _apply_parallel_constraint(self) -> bool:
        """Apply parallel constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying parallel constraint {self.name}")
        return True

    def _apply_perpendicular_constraint(self) -> bool:
        """Apply perpendicular constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying perpendicular constraint {self.name}")
        return True

    def _apply_coincident_constraint(self) -> bool:
        """Apply coincident constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying coincident constraint {self.name}")
        return True

    def _apply_distance_constraint(self) -> bool:
        """Apply distance constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying distance constraint {self.name}")
        return True

    def _apply_length_constraint(self) -> bool:
        """Apply length constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying length constraint {self.name}")
        return True

    def _apply_continuity_constraint(self) -> bool:
        """Apply continuity constraint."""
        # Placeholder implementation - would use build123d's constraint solver
        print(f"Applying continuity constraint {self.name}")
        return True
