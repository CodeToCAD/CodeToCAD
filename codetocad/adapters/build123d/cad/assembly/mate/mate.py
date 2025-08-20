"""
build123d implementation of assembly mates.

This module provides the base implementation for assembly mates using build123d's
joint system and geometric constraint solving capabilities.
"""

from typing import TYPE_CHECKING, Any, Optional

from codetocad.interfaces.cad.assembly.mate.mate_interface import (
    MateInterface,
    MateType,
    MateStatus,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.part.part import Part


class Mate(MateInterface):
    """
    build123d implementation of MateInterface.

    This base class provides common functionality for all mate types
    in the build123d adapter.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """
        Initialize a build123d mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of mate constraint
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            **kwargs: Additional mate-specific parameters
        """
        # Call MateInterface.__init__ directly to avoid conflicts with multiple inheritance
        from codetocad.interfaces.cad.assembly.mate.mate_interface import MateInterface

        MateInterface.__init__(self, name, mate_type, part1, part2, **kwargs)

        # build123d-specific properties
        self._native_joint = None
        self._constraint_equations = []
        self._last_solve_result = None

    def apply(self) -> bool:
        """
        Apply the mate constraint.

        Returns:
            True if the mate was successfully applied, False otherwise
        """
        try:
            if self._apply_constraint():
                self.status = MateStatus.ACTIVE
                return True
            else:
                self.status = MateStatus.FAILED
                return False
        except Exception as e:
            print(f"Error applying mate {self.name}: {e}")
            self.status = MateStatus.FAILED
            return False

    def remove(self) -> bool:
        """
        Remove the mate constraint.

        Returns:
            True if the mate was successfully removed, False otherwise
        """
        try:
            if self._remove_constraint():
                self.status = MateStatus.UNDEFINED
                return True
            else:
                return False
        except Exception as e:
            print(f"Error removing mate {self.name}: {e}")
            return False

    def update(self, **kwargs) -> bool:
        """
        Update mate parameters.

        Args:
            **kwargs: Updated parameters

        Returns:
            True if the mate was successfully updated, False otherwise
        """
        try:
            # Update parameters
            for key, value in kwargs.items():
                self.parameters[key] = value

            # Re-apply the constraint with new parameters
            if self.status == MateStatus.ACTIVE:
                return self.apply()
            return True
        except Exception as e:
            print(f"Error updating mate {self.name}: {e}")
            return False

    def is_valid(self) -> bool:
        """
        Check if the mate constraint is valid.

        Returns:
            True if the mate is valid, False otherwise
        """
        try:
            # Check if parts are valid
            if not self.part1 or not self.part2:
                return False

            # Check if parts have the required attributes
            if not hasattr(self.part1, "name") or not hasattr(self.part2, "name"):
                return False

            # For now, we'll be less strict about native instances
            # In a full implementation, you might want to check for native instances
            # if not hasattr(self.part1, 'native_instance') or not hasattr(self.part2, 'native_instance'):
            #     return False
            #
            # if not self.part1.native_instance or not self.part2.native_instance:
            #     return False

            # Perform mate-specific validation
            return self._validate_constraint()
        except Exception:
            return False

    def _apply_constraint(self) -> bool:
        """
        Apply the specific constraint for this mate type.

        This method should be overridden by subclasses.

        Returns:
            True if constraint was applied successfully, False otherwise
        """
        # Default implementation - subclasses should override
        return True

    def _remove_constraint(self) -> bool:
        """
        Remove the specific constraint for this mate type.

        This method should be overridden by subclasses.

        Returns:
            True if constraint was removed successfully, False otherwise
        """
        # Default implementation - subclasses should override
        return True

    def _validate_constraint(self) -> bool:
        """
        Validate the specific constraint for this mate type.

        This method should be overridden by subclasses.

        Returns:
            True if constraint is valid, False otherwise
        """
        # Default implementation - subclasses should override
        return True

    def get_native_joint(self) -> Optional[Any]:
        """
        Get the underlying build123d joint object.

        Returns:
            Native build123d joint or None if not applicable
        """
        return self._native_joint

    def set_native_joint(self, joint: Any) -> None:
        """
        Set the underlying build123d joint object.

        Args:
            joint: Native build123d joint
        """
        self._native_joint = joint

    def get_constraint_equations(self) -> list:
        """
        Get the mathematical constraint equations for this mate.

        Returns:
            List of constraint equations
        """
        return self._constraint_equations

    def solve_constraint(self) -> bool:
        """
        Solve the constraint equations for this mate.

        Returns:
            True if constraint was solved successfully, False otherwise
        """
        try:
            # This is a placeholder for constraint solving logic
            # In a full implementation, this would use a constraint solver
            # to determine the positions and orientations needed to satisfy the mate

            if self.is_valid():
                self._last_solve_result = True
                return True
            else:
                self._last_solve_result = False
                return False
        except Exception as e:
            print(f"Error solving constraint for mate {self.name}: {e}")
            self._last_solve_result = False
            return False

    def get_last_solve_result(self) -> Optional[bool]:
        """
        Get the result of the last constraint solve operation.

        Returns:
            True if last solve was successful, False if failed, None if never solved
        """
        return self._last_solve_result
