"""
Blender mate manager for assembly constraints.

This module provides the mate management functionality for Blender assemblies,
creating and managing constraints between parts using Blender's constraint system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from codetocad.interfaces.cad.assembly.mate.mate_interface import MateType
from codetocad.interfaces.cad.assembly.mate.mate_manager_interface import (
    MateManagerInterface,
)

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly
    from codetocad.adapters.blender.cad.part.part import Part
    from codetocad.interfaces.cad.assembly.mate.mate_interface import MateInterface


class BlenderMateManager(MateManagerInterface):
    """
    Blender implementation of MateManagerInterface.

    Manages the creation and lifecycle of mates between parts in a Blender assembly
    using Blender's native constraint system.
    """

    def __init__(self, assembly: "Assembly"):
        """
        Initialize the Blender mate manager.

        Args:
            assembly: The Blender assembly this manager belongs to
        """
        super().__init__(assembly)
        self._mate_counter = 0

        # Mapping of mate types to their Blender implementations
        self._mate_classes = {
            MateType.RIGID: self._get_rigid_mate_class,
            MateType.REVOLUTE: self._get_revolute_mate_class,
            MateType.LINEAR: self._get_linear_mate_class,
            MateType.CYLINDRICAL: self._get_cylindrical_mate_class,
            MateType.BALL: self._get_ball_mate_class,
            MateType.COINCIDENT: self._get_coincident_mate_class,
            MateType.CONCENTRIC: self._get_concentric_mate_class,
            MateType.DISTANCE: self._get_distance_mate_class,
            MateType.PARALLEL: self._get_parallel_mate_class,
            MateType.PERPENDICULAR: self._get_perpendicular_mate_class,
            MateType.TANGENT: self._get_tangent_mate_class,
            MateType.ANGLE: self._get_angle_mate_class,
        }

    def create_mate(
        self,
        mate_type: MateType,
        part1: "Part",
        part2: "Part",
        name: str | None = None,
        **kwargs,
    ) -> "MateInterface" | None:
        """
        Create a mate between two parts using Blender constraints.

        Args:
            mate_type: Type of mate to create
            part1: First part
            part2: Second part
            name: Optional name for the mate
            **kwargs: Additional parameters specific to the mate type

        Returns:
            Created mate or None if creation failed
        """
        try:
            # Generate name if not provided
            if name is None:
                name = self._generate_mate_name(mate_type)

            # Get the appropriate mate class
            mate_class_getter = self._mate_classes.get(mate_type)
            if not mate_class_getter:
                print(f"Unsupported mate type: {mate_type}")
                return None

            mate_class = mate_class_getter()
            if not mate_class:
                print(f"Failed to get mate class for type: {mate_type}")
                return None

            # Create the mate instance with proper parameter handling
            mate = self._create_mate_instance(
                mate_class, mate_type, name, part1, part2, **kwargs
            )

            if mate and mate.is_valid():
                # Store the mate
                self.mates[name] = mate
                return mate
            else:
                print(f"Failed to create or validate mate: {name}")
                return None

        except Exception as e:
            print(f"Error creating mate: {e}")
            return None

    def _generate_mate_name(self, mate_type: MateType) -> str:
        """
        Generate a unique name for a mate.

        Args:
            mate_type: Type of mate

        Returns:
            Generated unique name
        """
        self._mate_counter += 1
        return f"{mate_type.value}_{self._mate_counter}"

    def _create_mate_instance(
        self, mate_class, mate_type: MateType, name: str, part1, part2, **kwargs
    ):
        """
        Create a mate instance with proper parameter handling for different mate types.

        Args:
            mate_class: The mate class to instantiate
            mate_type: Type of mate being created
            name: Name for the mate
            part1: First part
            part2: Second part
            **kwargs: Additional parameters

        Returns:
            Created mate instance
        """
        try:
            # Create the mate instance
            mate = mate_class(name, mate_type, part1, part2, **kwargs)
            return mate
        except Exception as e:
            print(f"Failed to create mate instance: {e}")
            return None

    # Mate class getters - these import the actual mate classes when needed

    def _get_rigid_mate_class(self):
        """Get the RigidMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_kinematic_mate import (
                BlenderRigidMate,
            )

            return BlenderRigidMate
        except ImportError as e:
            print(f"Failed to import BlenderRigidMate: {e}")
            return None

    def _get_revolute_mate_class(self):
        """Get the RevoluteMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_kinematic_mate import (
                BlenderRevoluteMate,
            )

            return BlenderRevoluteMate
        except ImportError as e:
            print(f"Failed to import BlenderRevoluteMate: {e}")
            return None

    def _get_linear_mate_class(self):
        """Get the LinearMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_kinematic_mate import (
                BlenderLinearMate,
            )

            return BlenderLinearMate
        except ImportError as e:
            print(f"Failed to import BlenderLinearMate: {e}")
            return None

    def _get_cylindrical_mate_class(self):
        """Get the CylindricalMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_kinematic_mate import (
                BlenderCylindricalMate,
            )

            return BlenderCylindricalMate
        except ImportError as e:
            print(f"Failed to import BlenderCylindricalMate: {e}")
            return None

    def _get_ball_mate_class(self):
        """Get the BallMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_kinematic_mate import (
                BlenderBallMate,
            )

            return BlenderBallMate
        except ImportError as e:
            print(f"Failed to import BlenderBallMate: {e}")
            return None

    def _get_coincident_mate_class(self):
        """Get the CoincidentMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderCoincidentMate,
            )

            return BlenderCoincidentMate
        except ImportError as e:
            print(f"Failed to import BlenderCoincidentMate: {e}")
            return None

    def _get_concentric_mate_class(self):
        """Get the ConcentricMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderConcentricMate,
            )

            return BlenderConcentricMate
        except ImportError as e:
            print(f"Failed to import BlenderConcentricMate: {e}")
            return None

    def _get_distance_mate_class(self):
        """Get the DistanceMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderDistanceMate,
            )

            return BlenderDistanceMate
        except ImportError as e:
            print(f"Failed to import BlenderDistanceMate: {e}")
            return None

    def _get_parallel_mate_class(self):
        """Get the ParallelMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderParallelMate,
            )

            return BlenderParallelMate
        except ImportError as e:
            print(f"Failed to import BlenderParallelMate: {e}")
            return None

    def _get_perpendicular_mate_class(self):
        """Get the PerpendicularMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderPerpendicularMate,
            )

            return BlenderPerpendicularMate
        except ImportError as e:
            print(f"Failed to import BlenderPerpendicularMate: {e}")
            return None

    def _get_tangent_mate_class(self):
        """Get the TangentMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderTangentMate,
            )

            return BlenderTangentMate
        except ImportError as e:
            print(f"Failed to import BlenderTangentMate: {e}")
            return None

    def _get_angle_mate_class(self):
        """Get the AngleMate class."""
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_geometric_mate import (
                BlenderAngleMate,
            )

            return BlenderAngleMate
        except ImportError as e:
            print(f"Failed to import BlenderAngleMate: {e}")
            return None

    def remove_mate(self, mate_name: str) -> bool:
        """
        Remove a mate constraint.

        Args:
            mate_name: Name of the mate to remove

        Returns:
            True if mate was removed successfully, False otherwise
        """
        try:
            mate = self.mates.get(mate_name)
            if not mate:
                print(f"Mate not found: {mate_name}")
                return False

            # Remove the mate's constraints
            if hasattr(mate, "remove_constraints"):
                mate.remove_constraints()

            # Remove from mates dictionary
            del self.mates[mate_name]
            return True

        except Exception as e:
            print(f"Failed to remove mate {mate_name}: {e}")
            return False

    def solve_mates(self) -> bool:
        """
        Solve all active mate constraints.

        For Blender, this involves updating the dependency graph to ensure
        all constraints are properly evaluated.

        Returns:
            True if all mates were solved successfully, False otherwise
        """
        try:
            # In Blender, constraints are solved automatically by the dependency graph
            # We just need to trigger an update
            import bpy

            # Update the scene to trigger constraint evaluation
            if hasattr(bpy.context, "scene"):
                bpy.context.scene.frame_set(bpy.context.scene.frame_current)

            return True

        except Exception as e:
            print(f"Failed to solve mates: {e}")
            return False

    def validate_mates(self) -> dict[str, bool]:
        """
        Validate all mates in the assembly.

        Returns:
            Dictionary mapping mate names to their validity status
        """
        validation_results = {}

        try:
            for mate_name, mate in self.mates.items():
                if hasattr(mate, "is_valid"):
                    validation_results[mate_name] = mate.is_valid()
                else:
                    validation_results[mate_name] = False

            return validation_results

        except Exception as e:
            print(f"Failed to validate mates: {e}")
            return {mate_name: False for mate_name in self.mates.keys()}
