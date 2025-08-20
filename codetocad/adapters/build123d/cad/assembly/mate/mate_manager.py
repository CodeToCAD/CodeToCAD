"""
build123d implementation of assembly mate manager.

This module provides the mate manager implementation for build123d,
handling collections of mates within an assembly.
"""

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from codetocad.interfaces.cad.assembly.mate.mate_manager_interface import (
    MateManagerInterface,
)
from codetocad.interfaces.cad.assembly.mate.mate_interface import (
    MateInterface,
    MateType,
    MateStatus,
)

# Import mate implementations
from .kinematic_mate import (
    RigidMate,
    RevoluteMate,
    LinearMate,
    CylindricalMate,
    BallMate,
)
from .geometric_mate import (
    CoincidentMate,
    ConcentricMate,
    DistanceMate,
    ParallelMate,
    PerpendicularMate,
    TangentMate,
    AngleMate,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.assembly.assembly import Assembly
    from codetocad.adapters.build123d.cad.part.part import Part


class MateManager(MateManagerInterface):
    """
    build123d implementation of MateManagerInterface.

    Manages collections of mates within a build123d assembly,
    providing methods to create, modify, delete, and solve mate constraints.
    """

    def __init__(self, assembly: "Assembly"):
        """
        Initialize the mate manager.

        Args:
            assembly: The build123d assembly this manager belongs to
        """
        super().__init__(assembly)
        self._mate_counter = 0

        # Mapping of mate types to their implementation classes
        self._mate_classes = {
            MateType.RIGID: RigidMate,
            MateType.REVOLUTE: RevoluteMate,
            MateType.LINEAR: LinearMate,
            MateType.CYLINDRICAL: CylindricalMate,
            MateType.BALL: BallMate,
            MateType.COINCIDENT: CoincidentMate,
            MateType.CONCENTRIC: ConcentricMate,
            MateType.DISTANCE: DistanceMate,
            MateType.PARALLEL: ParallelMate,
            MateType.PERPENDICULAR: PerpendicularMate,
            MateType.TANGENT: TangentMate,
            MateType.ANGLE: AngleMate,
        }

    def create_mate(
        self,
        mate_type: MateType,
        part1: "Part",
        part2: "Part",
        name: Optional[str] = None,
        **kwargs,
    ) -> Optional[MateInterface]:
        """
        Create a new mate constraint.

        Args:
            mate_type: Type of mate to create
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            name: Optional name for the mate (auto-generated if None)
            **kwargs: Mate-specific parameters

        Returns:
            Created mate instance or None if creation failed
        """
        try:
            # Generate name if not provided
            if name is None:
                name = self._generate_mate_name(mate_type)

            # Check if name already exists
            if name in self.mates:
                print(f"Mate with name '{name}' already exists")
                return None

            # Validate that both parts are in the assembly
            if part1 not in self.assembly.parts or part2 not in self.assembly.parts:
                print(f"Both parts must be in the assembly to create a mate")
                return None

            # Get the mate class for this type
            mate_class = self._mate_classes.get(mate_type)
            if mate_class is None:
                print(f"Unsupported mate type: {mate_type}")
                return None

            # Create the mate instance with proper parameter handling
            mate = self._create_mate_instance(
                mate_class, mate_type, name, part1, part2, **kwargs
            )

            # Validate the mate
            if not mate.is_valid():
                print(f"Invalid mate configuration for {name}")
                return None

            # Add to our collection
            self.mates[name] = mate

            # Apply the mate constraint
            if mate.apply():
                print(f"Successfully created and applied mate: {name}")
                return mate
            else:
                # Remove from collection if application failed
                del self.mates[name]
                print(f"Failed to apply mate: {name}")
                return None

        except Exception as e:
            print(f"Error creating mate {name}: {e}")
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
            if mate is None:
                print(f"Mate '{mate_name}' not found")
                return False

            # Remove the constraint
            if mate.remove():
                # Remove from our collection
                del self.mates[mate_name]
                print(f"Successfully removed mate: {mate_name}")
                return True
            else:
                print(f"Failed to remove mate constraint: {mate_name}")
                return False

        except Exception as e:
            print(f"Error removing mate {mate_name}: {e}")
            return False

    def solve_mates(self) -> bool:
        """
        Solve all active mate constraints.

        Returns:
            True if all mates were solved successfully, False otherwise
        """
        try:
            success = True
            active_mates = self.get_mates_by_status(MateStatus.ACTIVE)

            print(f"Solving {len(active_mates)} active mates...")

            for mate in active_mates:
                if not mate.solve_constraint():
                    print(f"Failed to solve mate: {mate.name}")
                    mate.status = MateStatus.FAILED
                    success = False
                else:
                    print(f"Successfully solved mate: {mate.name}")

            return success

        except Exception as e:
            print(f"Error solving mates: {e}")
            return False

    def validate_mates(self) -> Dict[str, bool]:
        """
        Validate all mates in the assembly.

        Returns:
            Dictionary mapping mate names to their validity status
        """
        validation_results = {}

        try:
            for name, mate in self.mates.items():
                is_valid = mate.is_valid()
                validation_results[name] = is_valid

                # Update mate status based on validation
                if not is_valid and mate.status == MateStatus.ACTIVE:
                    mate.status = MateStatus.FAILED

        except Exception as e:
            print(f"Error validating mates: {e}")

        return validation_results

    def create_coincident_mate(
        self,
        part1: "Part",
        part2: "Part",
        entity1: any,
        entity2: any,
        name: Optional[str] = None,
        flip_alignment: bool = False,
    ) -> Optional[CoincidentMate]:
        """
        Convenience method to create a coincident mate.

        Args:
            part1: First part
            part2: Second part
            entity1: Entity on part1
            entity2: Entity on part2
            name: Optional mate name
            flip_alignment: Whether to flip alignment

        Returns:
            Created coincident mate or None
        """
        return self.create_mate(
            MateType.COINCIDENT,
            part1,
            part2,
            name,
            entity1=entity1,
            entity2=entity2,
            flip_alignment=flip_alignment,
        )

    def create_revolute_mate(
        self,
        part1: "Part",
        part2: "Part",
        axis: any,
        name: Optional[str] = None,
        angle_range: tuple = (0, 360),
        current_angle: float = 0,
    ) -> Optional[RevoluteMate]:
        """
        Convenience method to create a revolute mate.

        Args:
            part1: Fixed part
            part2: Rotating part
            axis: Axis of rotation
            name: Optional mate name
            angle_range: (min, max) angle limits
            current_angle: Initial angle

        Returns:
            Created revolute mate or None
        """
        return self.create_mate(
            MateType.REVOLUTE,
            part1,
            part2,
            name,
            axis=axis,
            angle_range=angle_range,
            current_angle=current_angle,
        )

    def create_distance_mate(
        self,
        part1: "Part",
        part2: "Part",
        entity1: any,
        entity2: any,
        distance: float,
        name: Optional[str] = None,
    ) -> Optional[DistanceMate]:
        """
        Convenience method to create a distance mate.

        Args:
            part1: First part
            part2: Second part
            entity1: Entity on part1
            entity2: Entity on part2
            distance: Distance to maintain
            name: Optional mate name

        Returns:
            Created distance mate or None
        """
        return self.create_mate(
            MateType.DISTANCE,
            part1,
            part2,
            name,
            entity1=entity1,
            entity2=entity2,
            distance=distance,
        )

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
        # Handle geometric mates that need entity parameters as positional arguments
        if mate_type in [
            MateType.COINCIDENT,
            MateType.CONCENTRIC,
            MateType.DISTANCE,
            MateType.PARALLEL,
            MateType.PERPENDICULAR,
            MateType.TANGENT,
            MateType.ANGLE,
        ]:

            entity1 = kwargs.pop("entity1", None)
            entity2 = kwargs.pop("entity2", None)

            if mate_type == MateType.DISTANCE:
                distance = kwargs.pop("distance", 0.0)
                return mate_class(
                    name, part1, part2, entity1, entity2, distance, **kwargs
                )
            elif mate_type == MateType.ANGLE:
                angle = kwargs.pop("angle", 0.0)
                return mate_class(name, part1, part2, entity1, entity2, angle, **kwargs)
            else:
                return mate_class(name, part1, part2, entity1, entity2, **kwargs)

        # Handle kinematic mates
        elif mate_type in [
            MateType.RIGID,
            MateType.REVOLUTE,
            MateType.LINEAR,
            MateType.CYLINDRICAL,
            MateType.BALL,
        ]:

            if mate_type == MateType.RIGID:
                return mate_class(name, part1, part2, **kwargs)
            elif mate_type == MateType.REVOLUTE:
                axis = kwargs.pop("axis", None)
                return mate_class(name, part1, part2, axis, **kwargs)
            elif mate_type == MateType.LINEAR:
                axis = kwargs.pop("axis", None)
                return mate_class(name, part1, part2, axis, **kwargs)
            elif mate_type == MateType.CYLINDRICAL:
                axis = kwargs.pop("axis", None)
                return mate_class(name, part1, part2, axis, **kwargs)
            elif mate_type == MateType.BALL:
                center_point = kwargs.pop("center_point", None)
                return mate_class(name, part1, part2, center_point, **kwargs)

        # Default fallback
        return mate_class(name, part1, part2, **kwargs)
