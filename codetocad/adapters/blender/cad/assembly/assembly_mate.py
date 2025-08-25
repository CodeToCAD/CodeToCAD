"""
Blender implementation of AssemblyMateInterface.

This module provides the fluent mate creation API for Blender assemblies
using Blender's native constraint system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple

from codetocad.interfaces.cad.assembly.assembly_mate_interface import (
    AssemblyMateInterface,
)
from codetocad.interfaces.cad.assembly.mate.mate_interface import MateType

# Import specific mate interface types
from codetocad.interfaces.cad.assembly.mate.kinematic_mate_interface import (
    RigidMateInterface,
    RevoluteMateInterface,
    LinearMateInterface,
    CylindricalMateInterface,
    BallMateInterface,
)
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
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly
    from codetocad.adapters.blender.cad.part.part import Part


class BlenderAssemblyMate(AssemblyMateInterface):
    """
    Blender implementation of fluent mate creation API.

    Provides intuitive methods for creating different types of mates
    between parts using Blender's native constraint system.
    """

    def __init__(self, assembly: "Assembly"):
        """
        Initialize the Blender assembly mate interface.

        Args:
            assembly: The Blender assembly this mate interface belongs to
        """
        self.assembly = assembly

    def rigid(
        self,
        part1: "Part",
        part2: "Part",
        location1: Any,
        location2: Any,
        name: str | None = None,
    ) -> RigidMateInterface | None:
        """
        Create a rigid mate between two parts using Blender constraints.

        Args:
            part1: First part (typically fixed)
            part2: Second part (constrained to part1)
            location1: Location/orientation on part1 where mate attaches
            location2: Location/orientation on part2 where mate attaches
            name: Optional name for the mate

        Returns:
            Created rigid mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.RIGID,
                part1,
                part2,
                name,
                location1=location1,
                location2=location2,
            )

        except Exception as e:
            print(f"Failed to create rigid mate: {e}")
            return None

    def revolute(
        self,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any,
        location2: Any,
        angle_range: tuple[float, float] = (0, 360),
        current_angle: float = 0,
        name: str | None = None,
    ) -> RevoluteMateInterface | None:
        """
        Create a revolute mate for hinge-like rotation using Blender constraints.

        Args:
            part1: First part (typically fixed)
            part2: Second part (rotating)
            axis: Axis of rotation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            angle_range: (min, max) angle limits in degrees
            current_angle: Initial angle in degrees
            name: Optional name for the mate

        Returns:
            Created revolute mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.REVOLUTE,
                part1,
                part2,
                name,
                axis=axis,
                location1=location1,
                location2=location2,
                angle_range=angle_range,
                current_angle=current_angle,
            )

        except Exception as e:
            print(f"Failed to create revolute mate: {e}")
            return None

    def linear(
        self,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any,
        location2: Any,
        position_range: tuple[float, float] = (0, float("inf")),
        current_position: float = 0,
        name: str | None = None,
    ) -> LinearMateInterface | None:
        """
        Create a linear mate for sliding motion using Blender constraints.

        Args:
            part1: First part (typically fixed)
            part2: Second part (sliding)
            axis: Axis of translation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            position_range: (min, max) position limits
            current_position: Initial position along axis
            name: Optional name for the mate

        Returns:
            Created linear mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.LINEAR,
                part1,
                part2,
                name,
                axis=axis,
                location1=location1,
                location2=location2,
                position_range=position_range,
                current_position=current_position,
            )

        except Exception as e:
            print(f"Failed to create linear mate: {e}")
            return None

    def cylindrical(
        self,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any,
        location2: Any,
        position_range: tuple[float, float] = (0, float("inf")),
        angle_range: tuple[float, float] = (0, 360),
        current_position: float = 0,
        current_angle: float = 0,
        name: str | None = None,
    ) -> CylindricalMateInterface | None:
        """
        Create a cylindrical mate for screw-like motion using Blender constraints.

        Args:
            part1: First part (typically fixed)
            part2: Second part (moving)
            axis: Axis of rotation and translation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            position_range: (min, max) position limits
            angle_range: (min, max) angle limits in degrees
            current_position: Initial position along axis
            current_angle: Initial angle in degrees
            name: Optional name for the mate

        Returns:
            Created cylindrical mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.CYLINDRICAL,
                part1,
                part2,
                name,
                axis=axis,
                location1=location1,
                location2=location2,
                position_range=position_range,
                angle_range=angle_range,
                current_position=current_position,
                current_angle=current_angle,
            )

        except Exception as e:
            print(f"Failed to create cylindrical mate: {e}")
            return None

    def ball(
        self,
        part1: "Part",
        part2: "Part",
        center_point: Any,
        location1: Any,
        location2: Any,
        angle_ranges: tuple[
            tuple[float, float], tuple[float, float], tuple[float, float]
        ] = ((0, 360), (0, 360), (0, 360)),
        current_angles: tuple[float, float, float] = (0, 0, 0),
        name: str | None = None,
    ) -> BallMateInterface | None:
        """
        Create a ball mate for spherical joint motion using Blender constraints.

        Args:
            part1: First part (typically fixed)
            part2: Second part (rotating)
            center_point: Center point of the spherical joint
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            angle_ranges: ((min_x, max_x), (min_y, max_y), (min_z, max_z)) angle limits
            current_angles: (x, y, z) initial angles in degrees
            name: Optional name for the mate

        Returns:
            Created ball mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.BALL,
                part1,
                part2,
                name,
                center_point=center_point,
                location1=location1,
                location2=location2,
                angle_ranges=angle_ranges,
                current_angles=current_angles,
            )

        except Exception as e:
            print(f"Failed to create ball mate: {e}")
            return None

    # Geometric Mate Methods

    def coincident(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        flip_alignment: bool = False,
        name: str | None = None,
    ) -> CoincidentMateInterface | None:
        """
        Create a coincident mate to align geometric entities using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Geometric entity on part1 (face, edge, vertex)
            entity2: Geometric entity on part2 (face, edge, vertex)
            flip_alignment: Whether to flip the alignment direction
            name: Optional name for the mate

        Returns:
            Created coincident mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.COINCIDENT,
                part1,
                part2,
                name,
                entity1=entity1,
                entity2=entity2,
                flip_alignment=flip_alignment,
            )

        except Exception as e:
            print(f"Failed to create coincident mate: {e}")
            return None

    def concentric(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> ConcentricMateInterface | None:
        """
        Create a concentric mate to align cylindrical features using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Cylindrical/circular entity on part1
            entity2: Cylindrical/circular entity on part2
            name: Optional name for the mate

        Returns:
            Created concentric mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.CONCENTRIC,
                part1,
                part2,
                name,
                entity1=entity1,
                entity2=entity2,
            )

        except Exception as e:
            print(f"Failed to create concentric mate: {e}")
            return None

    def distance(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        distance: float,
        name: str | None = None,
    ) -> DistanceMateInterface | None:
        """
        Create a distance mate to maintain specific spacing using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Geometric entity on part1
            entity2: Geometric entity on part2
            distance: Distance to maintain between entities
            name: Optional name for the mate

        Returns:
            Created distance mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.DISTANCE,
                part1,
                part2,
                name,
                entity1=entity1,
                entity2=entity2,
                distance=distance,
            )

        except Exception as e:
            print(f"Failed to create distance mate: {e}")
            return None

    def parallel(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> ParallelMateInterface | None:
        """
        Create a parallel mate to keep entities parallel using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            name: Optional name for the mate

        Returns:
            Created parallel mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.PARALLEL, part1, part2, name, entity1=entity1, entity2=entity2
            )

        except Exception as e:
            print(f"Failed to create parallel mate: {e}")
            return None

    def perpendicular(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> PerpendicularMateInterface | None:
        """
        Create a perpendicular mate to keep entities perpendicular using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            name: Optional name for the mate

        Returns:
            Created perpendicular mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.PERPENDICULAR,
                part1,
                part2,
                name,
                entity1=entity1,
                entity2=entity2,
            )

        except Exception as e:
            print(f"Failed to create perpendicular mate: {e}")
            return None

    def tangent(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> TangentMateInterface | None:
        """
        Create a tangent mate to make surfaces tangent using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Surface on part1
            entity2: Surface on part2
            name: Optional name for the mate

        Returns:
            Created tangent mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.TANGENT, part1, part2, name, entity1=entity1, entity2=entity2
            )

        except Exception as e:
            print(f"Failed to create tangent mate: {e}")
            return None

    def angle(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        angle: float,
        name: str | None = None,
    ) -> AngleMateInterface | None:
        """
        Create an angle mate to maintain specific angle using Blender constraints.

        Args:
            part1: First part
            part2: Second part
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            angle: Angle to maintain between entities (in degrees)
            name: Optional name for the mate

        Returns:
            Created angle mate or None if creation failed
        """
        try:
            from codetocad.adapters.blender.cad.assembly.mate.blender_mate_manager import (
                BlenderMateManager,
            )

            # Get or create mate manager
            if not hasattr(self.assembly, "_mate_manager"):
                self.assembly._mate_manager = BlenderMateManager(self.assembly)

            return self.assembly._mate_manager.create_mate(
                MateType.ANGLE,
                part1,
                part2,
                name,
                entity1=entity1,
                entity2=entity2,
                angle=angle,
            )

        except Exception as e:
            print(f"Failed to create angle mate: {e}")
            return None
