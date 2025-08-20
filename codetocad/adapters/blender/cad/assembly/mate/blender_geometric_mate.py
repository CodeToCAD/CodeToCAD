"""
Blender geometric mate implementations.

This module provides geometric mate classes that use Blender's constraint system
to create alignment and positioning relationships between parts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from codetocad.interfaces.cad.assembly.mate.mate_interface import MateType
from codetocad.interfaces.cad.assembly.mate.geometric_mate_interface import (
    CoincidentMateInterface,
    ConcentricMateInterface,
    DistanceMateInterface,
    ParallelMateInterface,
    PerpendicularMateInterface,
    TangentMateInterface,
    AngleMateInterface,
)

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.part.part import Part
    import bpy


class BlenderGeometricMate:
    """
    Base class for Blender geometric mates.

    Provides common functionality for geometric constraints using Blender's constraint system.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """
        Initialize a Blender geometric mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of mate
            part1: First part
            part2: Second part (constrained)
            **kwargs: Additional parameters
        """
        self.name = name
        self.mate_type = mate_type
        self.part1 = part1
        self.part2 = part2
        self.parameters = kwargs
        self.constraints: list["bpy.types.Constraint"] = []
        self._is_applied = False

    def is_valid(self) -> bool:
        """
        Check if the mate is valid.

        Returns:
            True if mate is valid, False otherwise
        """
        try:
            # Basic validation - check if parts exist and have Blender objects
            if not self.part1 or not self.part2:
                return False

            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            return True

        except Exception:
            return False

    def apply_constraints(self) -> bool:
        """
        Apply the Blender constraints for this mate.

        Returns:
            True if constraints were applied successfully, False otherwise
        """
        try:
            if self._is_applied:
                return True

            success = self._create_blender_constraints()
            if success:
                self._is_applied = True

            return success

        except Exception as e:
            print(f"Failed to apply constraints for mate {self.name}: {e}")
            return False

    def remove_constraints(self) -> bool:
        """
        Remove the Blender constraints for this mate.

        Returns:
            True if constraints were removed successfully, False otherwise
        """
        try:
            part2_obj = self.part2.get_blender_object()
            if not part2_obj:
                return False

            # Remove all constraints created by this mate
            for constraint in self.constraints:
                if constraint in part2_obj.constraints:
                    part2_obj.constraints.remove(constraint)

            self.constraints.clear()
            self._is_applied = False
            return True

        except Exception as e:
            print(f"Failed to remove constraints for mate {self.name}: {e}")
            return False

    def _create_blender_constraints(self) -> bool:
        """
        Create the specific Blender constraints for this mate type.

        Returns:
            True if constraints were created successfully, False otherwise
        """
        # To be implemented by subclasses
        raise NotImplementedError(
            "Subclasses must implement _create_blender_constraints"
        )

    def apply(self) -> bool:
        """Apply the mate constraint."""
        return self.apply_constraints()

    def remove(self) -> bool:
        """Remove the mate constraint."""
        return self.remove_constraints()

    def update(self, **kwargs) -> bool:
        """Update mate parameters."""
        try:
            self.parameters.update(kwargs)
            # Re-apply constraints with new parameters
            self.remove_constraints()
            return self.apply_constraints()
        except Exception:
            return False

    def get_constraint_equations(self) -> list:
        """Get constraint equations (simplified for Blender implementation)."""
        return []  # Blender handles constraint equations internally

    def calculate_transform(self) -> tuple | None:
        """Calculate transformation (simplified for Blender implementation)."""
        return None  # Blender handles transformations internally


class BlenderCoincidentMate(BlenderGeometricMate, CoincidentMateInterface):
    """
    Blender implementation of coincident mate using location/rotation constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender coincident mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.flip_alignment = kwargs.get("flip_alignment", False)
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create coincident alignment using copy location and rotation."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy location to align positions
            copy_loc = part2_obj.constraints.new(type="COPY_LOCATION")
            copy_loc.name = f"{self.name}_copy_location"
            copy_loc.target = part1_obj
            copy_loc.influence = 1.0

            # Copy rotation to align orientations
            copy_rot = part2_obj.constraints.new(type="COPY_ROTATION")
            copy_rot.name = f"{self.name}_copy_rotation"
            copy_rot.target = part1_obj
            copy_rot.influence = 1.0

            # Handle flip alignment if needed
            if self.flip_alignment:
                copy_rot.invert_x = True

            self.constraints.extend([copy_loc, copy_rot])
            return True

        except Exception as e:
            print(f"Failed to create coincident mate constraints: {e}")
            return False


class BlenderConcentricMate(BlenderGeometricMate, ConcentricMateInterface):
    """
    Blender implementation of concentric mate using location constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender concentric mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create concentric alignment using copy location."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy location to align centers (X and Y only for cylindrical features)
            copy_loc = part2_obj.constraints.new(type="COPY_LOCATION")
            copy_loc.name = f"{self.name}_copy_location"
            copy_loc.target = part1_obj
            copy_loc.use_x = True
            copy_loc.use_y = True
            copy_loc.use_z = False  # Allow Z movement for concentric alignment
            copy_loc.influence = 1.0

            self.constraints.append(copy_loc)
            return True

        except Exception as e:
            print(f"Failed to create concentric mate constraints: {e}")
            return False


class BlenderDistanceMate(BlenderGeometricMate, DistanceMateInterface):
    """
    Blender implementation of distance mate using limit distance constraint.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender distance mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.distance = kwargs.get("distance", 1.0)
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create distance constraint using limit distance."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Use limit distance constraint to maintain specific distance
            limit_dist = part2_obj.constraints.new(type="LIMIT_DISTANCE")
            limit_dist.name = f"{self.name}_limit_distance"
            limit_dist.target = part1_obj
            limit_dist.distance = self.distance
            limit_dist.limit_mode = "LIMITDIST_ONSURFACE"

            self.constraints.append(limit_dist)
            return True

        except Exception as e:
            print(f"Failed to create distance mate constraints: {e}")
            return False

    def set_distance(self, distance: float) -> bool:
        """Set the distance value."""
        try:
            self.distance = distance
            if self.constraints:
                for constraint in self.constraints:
                    if hasattr(constraint, "distance"):
                        constraint.distance = distance
            return True
        except Exception:
            return False

    def get_distance(self) -> float:
        """Get the current distance value."""
        return self.distance


class BlenderParallelMate(BlenderGeometricMate, ParallelMateInterface):
    """
    Blender implementation of parallel mate using rotation constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender parallel mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create parallel alignment using copy rotation."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy rotation to maintain parallel orientation
            copy_rot = part2_obj.constraints.new(type="COPY_ROTATION")
            copy_rot.name = f"{self.name}_copy_rotation"
            copy_rot.target = part1_obj
            copy_rot.influence = 1.0

            self.constraints.append(copy_rot)
            return True

        except Exception as e:
            print(f"Failed to create parallel mate constraints: {e}")
            return False


class BlenderPerpendicularMate(BlenderGeometricMate, PerpendicularMateInterface):
    """
    Blender implementation of perpendicular mate using rotation constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender perpendicular mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create perpendicular alignment using copy rotation with offset."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy rotation with 90-degree offset for perpendicular alignment
            copy_rot = part2_obj.constraints.new(type="COPY_ROTATION")
            copy_rot.name = f"{self.name}_copy_rotation"
            copy_rot.target = part1_obj
            copy_rot.influence = 1.0
            copy_rot.use_offset = True

            # Add 90-degree offset (simplified - assumes Z-axis rotation)
            part2_obj.rotation_euler[2] += 3.14159 / 2  # 90 degrees in radians

            self.constraints.append(copy_rot)
            return True

        except Exception as e:
            print(f"Failed to create perpendicular mate constraints: {e}")
            return False


class BlenderTangentMate(BlenderGeometricMate, TangentMateInterface):
    """
    Blender implementation of tangent mate using shrinkwrap constraint.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender tangent mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create tangent relationship using shrinkwrap constraint."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Use shrinkwrap constraint to maintain surface contact
            shrinkwrap = part2_obj.constraints.new(type="SHRINKWRAP")
            shrinkwrap.name = f"{self.name}_shrinkwrap"
            shrinkwrap.target = part1_obj
            shrinkwrap.shrinkwrap_type = "NEAREST_SURFACE"

            self.constraints.append(shrinkwrap)
            return True

        except Exception as e:
            print(f"Failed to create tangent mate constraints: {e}")
            return False


class BlenderAngleMate(BlenderGeometricMate, AngleMateInterface):
    """
    Blender implementation of angle mate using rotation constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender angle mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = kwargs.get("entity1")
        self.entity2 = kwargs.get("entity2")
        self.angle = kwargs.get("angle", 0.0)
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create angle relationship using copy rotation with offset."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy rotation with angle offset
            copy_rot = part2_obj.constraints.new(type="COPY_ROTATION")
            copy_rot.name = f"{self.name}_copy_rotation"
            copy_rot.target = part1_obj
            copy_rot.influence = 1.0
            copy_rot.use_offset = True

            # Add angle offset (simplified - assumes Z-axis rotation)
            part2_obj.rotation_euler[2] += self.angle * 3.14159 / 180

            self.constraints.append(copy_rot)
            return True

        except Exception as e:
            print(f"Failed to create angle mate constraints: {e}")
            return False

    def set_angle(self, angle: float) -> bool:
        """Set the angle value."""
        try:
            self.angle = angle
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                # Update rotation with new angle
                part2_obj.rotation_euler[2] = angle * 3.14159 / 180
            return True
        except Exception:
            return False

    def get_angle(self) -> float:
        """Get the current angle value."""
        return self.angle
