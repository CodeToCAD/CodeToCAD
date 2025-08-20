"""
Blender implementation of constraint interfaces.

This module provides concrete implementations of kinematic and geometric constraints
for Blender objects using Blender's native constraint system.
"""

from typing import TYPE_CHECKING, Any
import math

from codetocad.adapters.blender.cad.blender_constraint_interface import (
    BlenderConstraintInterface,
    BlenderConstraint,
    BlenderConstraintType,
    BlenderConstraintStatus,
)

# Import existing Blender constraint actions
from codetocad.adapters.blender.blender_actions.constraints import (
    apply_constraint,
    apply_copy_location_constraint,
    apply_copy_rotation_constraint,
    apply_limit_location_constraint,
    apply_limit_rotation_constraint,
    apply_pivot_constraint,
    get_constraint,
)
from codetocad.adapters.blender.blender_definitions import BlenderConstraintTypes

if TYPE_CHECKING:
    import bpy


class BlenderObjectConstraint(BlenderConstraintInterface):
    """
    Blender implementation of BlenderConstraintInterface.

    Provides constraint functionality for Blender objects using Blender's
    native constraint system.
    """

    def __init__(self, blender_object: "bpy.types.Object"):
        """
        Initialize the Blender constraint implementation.

        Args:
            blender_object: The Blender object this constraint interface belongs to
        """
        super().__init__(blender_object)
        self.blender_object: "bpy.types.Object" = blender_object

    def copy_location(
        self,
        target_object: "bpy.types.Object",
        use_x: bool = True,
        use_y: bool = True,
        use_z: bool = True,
        use_offset: bool = False,
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl|None":
        """Create a copy location constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.COPY_LOCATION)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.COPY_LOCATION,
                blender_object=self.blender_object,
                target_object=target_object,
                use_x=use_x,
                use_y=use_y,
                use_z=use_z,
                use_offset=use_offset,
                influence=influence,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create copy location constraint: {e}")
            return None

    def copy_rotation(
        self,
        target_object: "bpy.types.Object",
        use_x: bool = True,
        use_y: bool = True,
        use_z: bool = True,
        use_offset: bool = False,
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl|None":
        """Create a copy rotation constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.COPY_ROTATION)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.COPY_ROTATION,
                blender_object=self.blender_object,
                target_object=target_object,
                use_x=use_x,
                use_y=use_y,
                use_z=use_z,
                use_offset=use_offset,
                influence=influence,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create copy rotation constraint: {e}")
            return None

    def copy_scale(
        self,
        target_object: "bpy.types.Object",
        use_x: bool = True,
        use_y: bool = True,
        use_z: bool = True,
        use_offset: bool = False,
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a copy scale constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.COPY_SCALE)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.COPY_SCALE,
                blender_object=self.blender_object,
                target_object=target_object,
                use_x=use_x,
                use_y=use_y,
                use_z=use_z,
                use_offset=use_offset,
                influence=influence,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create copy scale constraint: {e}")
            return None

    def limit_location(
        self,
        min_x: float | None = None,
        max_x: float | None = None,
        min_y: float | None = None,
        max_y: float | None = None,
        min_z: float | None = None,
        max_z: float | None = None,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a limit location constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.LIMIT_LOCATION)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.LIMIT_LOCATION,
                blender_object=self.blender_object,
                min_x=min_x,
                max_x=max_x,
                min_y=min_y,
                max_y=max_y,
                min_z=min_z,
                max_z=max_z,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create limit location constraint: {e}")
            return None

    def track_to(
        self,
        target_object: "bpy.types.Object",
        track_axis: str = "TRACK_NEGATIVE_Z",
        up_axis: str = "UP_Y",
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a track to constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.TRACK_TO)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.TRACK_TO,
                blender_object=self.blender_object,
                target_object=target_object,
                track_axis=track_axis,
                up_axis=up_axis,
                influence=influence,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create track to constraint: {e}")
            return None

    def maintain_distance(
        self,
        target_object: "bpy.types.Object",
        distance: float,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a constraint to maintain distance from target object."""
        if name is None:
            name = self._generate_constraint_name(
                BlenderConstraintType.MAINTAIN_DISTANCE
            )

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.MAINTAIN_DISTANCE,
                blender_object=self.blender_object,
                target_object=target_object,
                distance=distance,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create maintain distance constraint: {e}")
            return None

    def follow_path(
        self,
        curve_object: "bpy.types.Object",
        offset: float = 0.0,
        forward_axis: str = "FORWARD_Y",
        up_axis: str = "UP_Z",
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a follow path constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.FOLLOW_PATH)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.FOLLOW_PATH,
                blender_object=self.blender_object,
                curve_object=curve_object,
                offset=offset,
                forward_axis=forward_axis,
                up_axis=up_axis,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create follow path constraint: {e}")
            return None

    def child_of(
        self,
        parent_object: "bpy.types.Object",
        influence: float = 1.0,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a child of constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.CHILD_OF)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.CHILD_OF,
                blender_object=self.blender_object,
                parent_object=parent_object,
                influence=influence,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create child of constraint: {e}")
            return None

    def floor_constraint(
        self,
        target_object: "bpy.types.Object",
        floor_location: str = "FLOOR_NEGATIVE_Y",
        use_rotation: bool = False,
        name: str | None = None,
    ) -> "BlenderObjectConstraintImpl | None":
        """Create a floor constraint."""
        if name is None:
            name = self._generate_constraint_name(BlenderConstraintType.FLOOR)

        try:
            constraint = BlenderObjectConstraintImpl(
                name=name,
                constraint_type=BlenderConstraintType.FLOOR,
                blender_object=self.blender_object,
                target_object=target_object,
                floor_location=floor_location,
                use_rotation=use_rotation,
            )

            if constraint.apply():
                self.constraints[name] = constraint
                return constraint
            return None

        except Exception as e:
            print(f"Failed to create floor constraint: {e}")
            return None


class BlenderObjectConstraintImpl(BlenderConstraint):
    """
    Blender implementation of BlenderConstraint.

    Represents a constraint applied to a Blender object using Blender's native constraint system.
    """

    def __init__(
        self,
        name: str,
        constraint_type: BlenderConstraintType,
        blender_object: "bpy.types.Object",
        **parameters,
    ):
        """Initialize a Blender constraint implementation."""
        super().__init__(name, constraint_type, blender_object, **parameters)
        self.blender_object: "bpy.types.Object" = blender_object

    def apply(self) -> bool:
        """Apply the constraint to the Blender object."""
        try:
            # Apply constraint based on type using existing Blender actions
            success = self._apply_constraint()

            if success:
                self.status = BlenderConstraintStatus.ACTIVE
                return True
            else:
                self.status = BlenderConstraintStatus.ERROR
                return False

        except Exception as e:
            print(f"Failed to apply constraint {self.name}: {e}")
            self.status = BlenderConstraintStatus.ERROR
            return False

    def remove(self) -> bool:
        """Remove the constraint from the Blender object."""
        try:
            if self.native_constraint and self.blender_object:
                # Remove the constraint from the object
                self.blender_object.constraints.remove(self.native_constraint)
                self.native_constraint = None
                self.status = BlenderConstraintStatus.UNDEFINED
                return True
            return False

        except Exception as e:
            print(f"Failed to remove constraint {self.name}: {e}")
            return False

    def is_valid(self) -> bool:
        """Check if the constraint is valid."""
        try:
            # Basic validation - check if object exists
            if not self.blender_object:
                return False

            # Check if constraint still exists in Blender
            if self.native_constraint:
                return self.native_constraint in self.blender_object.constraints

            return True

        except Exception:
            return False

    def _apply_constraint(self) -> bool:
        """Apply the specific constraint based on its type."""
        if self.constraint_type == BlenderConstraintType.COPY_LOCATION:
            return self._apply_copy_location()
        elif self.constraint_type == BlenderConstraintType.COPY_ROTATION:
            return self._apply_copy_rotation()
        elif self.constraint_type == BlenderConstraintType.COPY_SCALE:
            return self._apply_copy_scale()
        elif self.constraint_type == BlenderConstraintType.LIMIT_LOCATION:
            return self._apply_limit_location()
        elif self.constraint_type == BlenderConstraintType.TRACK_TO:
            return self._apply_track_to()
        elif self.constraint_type == BlenderConstraintType.MAINTAIN_DISTANCE:
            return self._apply_maintain_distance()
        elif self.constraint_type == BlenderConstraintType.FOLLOW_PATH:
            return self._apply_follow_path()
        elif self.constraint_type == BlenderConstraintType.CHILD_OF:
            return self._apply_child_of()
        elif self.constraint_type == BlenderConstraintType.FLOOR:
            return self._apply_floor()
        else:
            print(f"Unknown constraint type: {self.constraint_type}")
            return False

    def _apply_copy_location(self) -> bool:
        """Apply copy location constraint using existing Blender actions."""
        try:
            target_object = self.parameters.get("target_object")
            if not target_object:
                return False

            # Use existing Blender action
            apply_copy_location_constraint(
                blender_object=self.blender_object,
                copied_blender_object=target_object,
                copy_x=self.parameters.get("use_x", True),
                copy_y=self.parameters.get("use_y", True),
                copy_z=self.parameters.get("use_z", True),
                use_offset=self.parameters.get("use_offset", False),
            )

            # Get the created constraint
            constraint = get_constraint(
                self.blender_object,
                BlenderConstraintTypes.COPY_LOCATION.get_default_blender_name(),
            )

            if constraint:
                self.native_constraint = constraint
                return True
            return False

        except Exception as e:
            print(f"Failed to apply copy location constraint: {e}")
            return False

    def _apply_copy_rotation(self) -> bool:
        """Apply copy rotation constraint using existing Blender actions."""
        try:
            target_object = self.parameters.get("target_object")
            if not target_object:
                return False

            # Use existing Blender action
            apply_copy_rotation_constraint(
                blender_object=self.blender_object,
                copied_blender_object=target_object,
                copy_x=self.parameters.get("use_x", True),
                copy_y=self.parameters.get("use_y", True),
                copy_z=self.parameters.get("use_z", True),
            )

            # Get the created constraint
            constraint = get_constraint(
                self.blender_object,
                BlenderConstraintTypes.COPY_ROTATION.get_default_blender_name(),
            )

            if constraint:
                self.native_constraint = constraint
                return True
            return False

        except Exception as e:
            print(f"Failed to apply copy rotation constraint: {e}")
            return False

    def _apply_copy_scale(self) -> bool:
        """Apply copy scale constraint."""
        try:
            target_object = self.parameters.get("target_object")
            if not target_object:
                return False

            # Add copy scale constraint directly since it's not in existing actions
            constraint = self.blender_object.constraints.new(type="COPY_SCALE")
            constraint.name = self.name
            constraint.target = target_object

            # Apply parameters
            constraint.use_x = self.parameters.get("use_x", True)
            constraint.use_y = self.parameters.get("use_y", True)
            constraint.use_z = self.parameters.get("use_z", True)
            constraint.use_offset = self.parameters.get("use_offset", False)
            constraint.influence = self.parameters.get("influence", 1.0)

            self.native_constraint = constraint
            return True

        except Exception as e:
            print(f"Failed to apply copy scale constraint: {e}")
            return False

    def _apply_limit_location(self) -> bool:
        """Apply limit location constraint using existing Blender actions."""
        try:
            # Use existing Blender action
            min_x = self.parameters.get("min_x")
            max_x = self.parameters.get("max_x")
            min_y = self.parameters.get("min_y")
            max_y = self.parameters.get("max_y")
            min_z = self.parameters.get("min_z")
            max_z = self.parameters.get("max_z")

            x = [min_x, max_x] if min_x is not None or max_x is not None else None
            y = [min_y, max_y] if min_y is not None or max_y is not None else None
            z = [min_z, max_z] if min_z is not None or max_z is not None else None

            apply_limit_location_constraint(
                blender_object=self.blender_object,
                x=x,
                y=y,
                z=z,
                relative_to_object=None,  # No relative object for basic limit location
            )

            # Get the created constraint
            constraint = get_constraint(
                self.blender_object,
                BlenderConstraintTypes.LIMIT_LOCATION.get_default_blender_name(),
            )

            if constraint:
                self.native_constraint = constraint
                return True
            return False

        except Exception as e:
            print(f"Failed to apply limit location constraint: {e}")
            return False

    def _apply_track_to(self) -> bool:
        """Apply track to constraint."""
        try:
            target_object = self.parameters.get("target_object")
            if not target_object:
                return False

            # Add track to constraint directly
            constraint = self.blender_object.constraints.new(type="TRACK_TO")
            constraint.name = self.name
            constraint.target = target_object

            # Apply parameters
            constraint.track_axis = self.parameters.get(
                "track_axis", "TRACK_NEGATIVE_Z"
            )
            constraint.up_axis = self.parameters.get("up_axis", "UP_Y")
            constraint.influence = self.parameters.get("influence", 1.0)

            self.native_constraint = constraint
            return True

        except Exception as e:
            print(f"Failed to apply track to constraint: {e}")
            return False

    def _apply_maintain_distance(self) -> bool:
        """Apply maintain distance constraint using limit distance."""
        try:
            target_object = self.parameters.get("target_object")
            distance = self.parameters.get("distance", 1.0)
            if not target_object:
                return False

            # Use limit distance constraint to maintain distance
            constraint = self.blender_object.constraints.new(type="LIMIT_DISTANCE")
            constraint.name = self.name
            constraint.target = target_object
            constraint.distance = distance
            constraint.limit_mode = "LIMITDIST_ONSURFACE"

            self.native_constraint = constraint
            return True

        except Exception as e:
            print(f"Failed to apply maintain distance constraint: {e}")
            return False

    def _apply_follow_path(self) -> bool:
        """Apply follow path constraint."""
        try:
            curve_object = self.parameters.get("curve_object")
            if not curve_object:
                return False

            # Add follow path constraint
            constraint = self.blender_object.constraints.new(type="FOLLOW_PATH")
            constraint.name = self.name
            constraint.target = curve_object

            # Apply parameters
            constraint.offset = self.parameters.get("offset", 0.0)
            constraint.forward_axis = self.parameters.get("forward_axis", "FORWARD_Y")
            constraint.up_axis = self.parameters.get("up_axis", "UP_Z")

            self.native_constraint = constraint
            return True

        except Exception as e:
            print(f"Failed to apply follow path constraint: {e}")
            return False

    def _apply_child_of(self) -> bool:
        """Apply child of constraint."""
        try:
            parent_object = self.parameters.get("parent_object")
            if not parent_object:
                return False

            # Add child of constraint
            constraint = self.blender_object.constraints.new(type="CHILD_OF")
            constraint.name = self.name
            constraint.target = parent_object
            constraint.influence = self.parameters.get("influence", 1.0)

            self.native_constraint = constraint
            return True

        except Exception as e:
            print(f"Failed to apply child of constraint: {e}")
            return False

    def _apply_floor(self) -> bool:
        """Apply floor constraint."""
        try:
            target_object = self.parameters.get("target_object")
            if not target_object:
                return False

            # Add floor constraint
            constraint = self.blender_object.constraints.new(type="FLOOR")
            constraint.name = self.name
            constraint.target = target_object

            # Apply parameters
            constraint.floor_location = self.parameters.get(
                "floor_location", "FLOOR_NEGATIVE_Y"
            )
            constraint.use_rotation = self.parameters.get("use_rotation", False)

            self.native_constraint = constraint
            return True

        except Exception as e:
            print(f"Failed to apply floor constraint: {e}")
            return False
