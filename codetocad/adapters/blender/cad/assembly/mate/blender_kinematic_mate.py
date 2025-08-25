"""
Blender kinematic mate implementations.

This module provides kinematic mate classes that use Blender's constraint system
to create joints and motion relationships between parts.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple

from codetocad.interfaces.cad.assembly.mate.mate_interface import MateType
from codetocad.interfaces.cad.assembly.mate.kinematic_mate_interface import (
    RigidMateInterface,
    RevoluteMateInterface,
    LinearMateInterface,
    CylindricalMateInterface,
    BallMateInterface,
)

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.part.part import Part
    import bpy


class BlenderKinematicMate:
    """
    Base class for Blender kinematic mates.

    Provides common functionality for kinematic constraints using Blender's constraint system.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """
        Initialize a Blender kinematic mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of mate
            part1: First part (typically fixed)
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


class BlenderRigidMate(BlenderKinematicMate, RigidMateInterface):
    """
    Blender implementation of rigid mate using Child Of constraint.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender rigid mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        # Apply constraints immediately for rigid mates
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create rigid connection using Child Of constraint."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Create Child Of constraint to make part2 follow part1 rigidly
            child_constraint = part2_obj.constraints.new(type="CHILD_OF")
            child_constraint.name = f"{self.name}_child_of"
            child_constraint.target = part1_obj
            child_constraint.influence = 1.0

            # Set the inverse matrix to maintain current relative position
            child_constraint.inverse_matrix = (
                part1_obj.matrix_world.inverted() @ part2_obj.matrix_world
            )

            self.constraints.append(child_constraint)
            return True

        except Exception as e:
            print(f"Failed to create rigid mate constraints: {e}")
            return False

    def get_degrees_of_freedom(self) -> int:
        """Get degrees of freedom (0 for rigid mate)."""
        return 0

    def set_position(self, **kwargs) -> bool:
        """Set position (no-op for rigid mate)."""
        return True  # Rigid mates don't allow position changes

    def get_position(self) -> dict:
        """Get position (returns empty dict for rigid mate)."""
        return {}  # Rigid mates have no controllable position


class BlenderRevoluteMate(BlenderKinematicMate, RevoluteMateInterface):
    """
    Blender implementation of revolute mate using rotation constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender revolute mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.axis = kwargs.get("axis")
        self.angle_range = kwargs.get("angle_range", (0, 360))
        self.current_angle = kwargs.get("current_angle", 0)
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create revolute joint using location copy and rotation limits."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy location to maintain position
            copy_loc = part2_obj.constraints.new(type="COPY_LOCATION")
            copy_loc.name = f"{self.name}_copy_location"
            copy_loc.target = part1_obj
            copy_loc.influence = 1.0

            # Limit rotation to the specified axis and range
            limit_rot = part2_obj.constraints.new(type="LIMIT_ROTATION")
            limit_rot.name = f"{self.name}_limit_rotation"
            limit_rot.use_limit_x = True
            limit_rot.use_limit_y = True
            limit_rot.use_limit_z = True

            # Set limits based on axis (simplified - assumes Z-axis rotation)
            min_angle, max_angle = self.angle_range
            limit_rot.min_z = min_angle * 3.14159 / 180  # Convert to radians
            limit_rot.max_z = max_angle * 3.14159 / 180

            self.constraints.extend([copy_loc, limit_rot])
            return True

        except Exception as e:
            print(f"Failed to create revolute mate constraints: {e}")
            return False

    def set_angle(self, angle: float) -> bool:
        """Set the current angle of the revolute joint."""
        try:
            self.current_angle = angle
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                # Set rotation (simplified - assumes Z-axis)
                part2_obj.rotation_euler[2] = angle * 3.14159 / 180
                return True
            return False
        except Exception:
            return False

    def get_angle(self) -> float:
        """Get the current angle of the revolute joint."""
        try:
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                return part2_obj.rotation_euler[2] * 180 / 3.14159
            return self.current_angle
        except Exception:
            return self.current_angle

    def get_degrees_of_freedom(self) -> int:
        """Get degrees of freedom (1 for revolute mate)."""
        return 1

    def set_position(self, **kwargs) -> bool:
        """Set position (angle for revolute mate)."""
        angle = kwargs.get("angle")
        if angle is not None:
            return self.set_angle(angle)
        return False

    def get_position(self) -> dict:
        """Get position (angle for revolute mate)."""
        return {"angle": self.get_angle()}


class BlenderLinearMate(BlenderKinematicMate, LinearMateInterface):
    """
    Blender implementation of linear mate using location constraints.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender linear mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.axis = kwargs.get("axis")
        self.position_range = kwargs.get("position_range", (0, float("inf")))
        self.current_position = kwargs.get("current_position", 0)
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create linear joint using rotation copy and location limits."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy rotation to maintain orientation
            copy_rot = part2_obj.constraints.new(type="COPY_ROTATION")
            copy_rot.name = f"{self.name}_copy_rotation"
            copy_rot.target = part1_obj
            copy_rot.influence = 1.0

            # Limit location to the specified axis and range
            limit_loc = part2_obj.constraints.new(type="LIMIT_LOCATION")
            limit_loc.name = f"{self.name}_limit_location"
            limit_loc.use_min_x = True
            limit_loc.use_max_x = True
            limit_loc.use_min_y = True
            limit_loc.use_max_y = True
            limit_loc.use_min_z = True
            limit_loc.use_max_z = True

            # Set limits based on axis (simplified - assumes Z-axis movement)
            min_pos, max_pos = self.position_range
            if max_pos != float("inf"):
                limit_loc.min_z = min_pos
                limit_loc.max_z = max_pos

            self.constraints.extend([copy_rot, limit_loc])
            return True

        except Exception as e:
            print(f"Failed to create linear mate constraints: {e}")
            return False

    def set_position(self, position: float) -> bool:
        """Set the current position of the linear joint."""
        try:
            self.current_position = position
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                # Set position (simplified - assumes Z-axis)
                part2_obj.location[2] = position
                return True
            return False
        except Exception:
            return False

    def get_position(self) -> float:
        """Get the current position of the linear joint."""
        try:
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                return part2_obj.location[2]
            return self.current_position
        except Exception:
            return self.current_position

    def get_degrees_of_freedom(self) -> int:
        """Get degrees of freedom (1 for linear mate)."""
        return 1


class BlenderCylindricalMate(BlenderKinematicMate, CylindricalMateInterface):
    """
    Blender implementation of cylindrical mate combining rotation and translation.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender cylindrical mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.axis = kwargs.get("axis")
        self.position_range = kwargs.get("position_range", (0, float("inf")))
        self.angle_range = kwargs.get("angle_range", (0, 360))
        self.current_position = kwargs.get("current_position", 0)
        self.current_angle = kwargs.get("current_angle", 0)
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create cylindrical joint allowing both rotation and translation."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Limit location for translation along axis
            limit_loc = part2_obj.constraints.new(type="LIMIT_LOCATION")
            limit_loc.name = f"{self.name}_limit_location"
            limit_loc.use_min_z = True
            limit_loc.use_max_z = True

            min_pos, max_pos = self.position_range
            if max_pos != float("inf"):
                limit_loc.min_z = min_pos
                limit_loc.max_z = max_pos

            # Limit rotation for rotation around axis
            limit_rot = part2_obj.constraints.new(type="LIMIT_ROTATION")
            limit_rot.name = f"{self.name}_limit_rotation"
            limit_rot.use_limit_z = True

            min_angle, max_angle = self.angle_range
            limit_rot.min_z = min_angle * 3.14159 / 180
            limit_rot.max_z = max_angle * 3.14159 / 180

            self.constraints.extend([limit_loc, limit_rot])
            return True

        except Exception as e:
            print(f"Failed to create cylindrical mate constraints: {e}")
            return False

    def set_position(self, position: float) -> bool:
        """Set the current position of the cylindrical joint."""
        return self.set_position_and_angle(position, self.current_angle)

    def set_angle(self, angle: float) -> bool:
        """Set the current angle of the cylindrical joint."""
        return self.set_position_and_angle(self.current_position, angle)

    def set_position_and_angle(self, position: float, angle: float) -> bool:
        """Set both position and angle of the cylindrical joint."""
        try:
            self.current_position = position
            self.current_angle = angle
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                part2_obj.location[2] = position
                part2_obj.rotation_euler[2] = angle * 3.14159 / 180
                return True
            return False
        except Exception:
            return False

    def get_position(self) -> float:
        """Get the current position of the cylindrical joint."""
        try:
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                return part2_obj.location[2]
            return self.current_position
        except Exception:
            return self.current_position

    def get_angle(self) -> float:
        """Get the current angle of the cylindrical joint."""
        try:
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                return part2_obj.rotation_euler[2] * 180 / 3.14159
            return self.current_angle
        except Exception:
            return self.current_angle

    def get_degrees_of_freedom(self) -> int:
        """Get degrees of freedom (2 for cylindrical mate)."""
        return 2


class BlenderBallMate(BlenderKinematicMate, BallMateInterface):
    """
    Blender implementation of ball mate allowing multi-axis rotation.
    """

    def __init__(
        self, name: str, mate_type: MateType, part1: "Part", part2: "Part", **kwargs
    ):
        """Initialize Blender ball mate."""
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.center_point = kwargs.get("center_point")
        self.angle_ranges = kwargs.get("angle_ranges", ((0, 360), (0, 360), (0, 360)))
        self.current_angles = kwargs.get("current_angles", (0, 0, 0))
        self.apply_constraints()

    def _create_blender_constraints(self) -> bool:
        """Create ball joint allowing rotation around all axes."""
        try:
            part1_obj = self.part1.get_blender_object()
            part2_obj = self.part2.get_blender_object()

            if not part1_obj or not part2_obj:
                return False

            # Copy location to maintain position at ball center
            copy_loc = part2_obj.constraints.new(type="COPY_LOCATION")
            copy_loc.name = f"{self.name}_copy_location"
            copy_loc.target = part1_obj
            copy_loc.influence = 1.0

            # Limit rotation for all axes
            limit_rot = part2_obj.constraints.new(type="LIMIT_ROTATION")
            limit_rot.name = f"{self.name}_limit_rotation"
            limit_rot.use_limit_x = True
            limit_rot.use_limit_y = True
            limit_rot.use_limit_z = True

            # Set limits for each axis
            (min_x, max_x), (min_y, max_y), (min_z, max_z) = self.angle_ranges
            limit_rot.min_x = min_x * 3.14159 / 180
            limit_rot.max_x = max_x * 3.14159 / 180
            limit_rot.min_y = min_y * 3.14159 / 180
            limit_rot.max_y = max_y * 3.14159 / 180
            limit_rot.min_z = min_z * 3.14159 / 180
            limit_rot.max_z = max_z * 3.14159 / 180

            self.constraints.extend([copy_loc, limit_rot])
            return True

        except Exception as e:
            print(f"Failed to create ball mate constraints: {e}")
            return False

    def set_angles(self, x_angle: float, y_angle: float, z_angle: float) -> bool:
        """Set the current angles of the ball joint."""
        try:
            self.current_angles = (x_angle, y_angle, z_angle)
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                part2_obj.rotation_euler[0] = x_angle * 3.14159 / 180
                part2_obj.rotation_euler[1] = y_angle * 3.14159 / 180
                part2_obj.rotation_euler[2] = z_angle * 3.14159 / 180
                return True
            return False
        except Exception:
            return False

    def get_angles(self) -> tuple[float, float, float]:
        """Get the current angles of the ball joint."""
        try:
            part2_obj = self.part2.get_blender_object()
            if part2_obj:
                return (
                    part2_obj.rotation_euler[0] * 180 / 3.14159,
                    part2_obj.rotation_euler[1] * 180 / 3.14159,
                    part2_obj.rotation_euler[2] * 180 / 3.14159,
                )
            return self.current_angles
        except Exception:
            return self.current_angles

    def get_degrees_of_freedom(self) -> int:
        """Get degrees of freedom (3 for ball mate)."""
        return 3

    def set_position(self, **kwargs) -> bool:
        """Set position (angles for ball mate)."""
        x_angle = kwargs.get("x_angle", self.current_angles[0])
        y_angle = kwargs.get("y_angle", self.current_angles[1])
        z_angle = kwargs.get("z_angle", self.current_angles[2])
        return self.set_angles(x_angle, y_angle, z_angle)

    def get_position(self) -> dict:
        """Get position (angles for ball mate)."""
        angles = self.get_angles()
        return {"x_angle": angles[0], "y_angle": angles[1], "z_angle": angles[2]}
