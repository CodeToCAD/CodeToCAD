"""
build123d implementation of AssemblyMateInterface.

This module provides the fluent mate creation API for build123d assemblies.
"""

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
    from codetocad.adapters.build123d.cad.assembly.assembly import Assembly
    from codetocad.adapters.build123d.cad.part.part import Part


class AssemblyMate(AssemblyMateInterface):
    """
    build123d implementation of fluent mate creation API.

    Provides intuitive methods for creating different types of mates
    between parts using a fluent API approach.
    """

    def __init__(self, assembly: "Assembly"):
        """
        Initialize the assembly mate interface.

        Args:
            assembly: The build123d assembly this mate interface belongs to
        """
        super().__init__(assembly)

    # Kinematic Mates (Motion-based)

    def rigid(
        self,
        part1: "Part",
        part2: "Part",
        location1: Any,
        location2: Any,
        name: str | None = None,
    ) -> "RigidMateInterface | None":
        """
        Create a rigid mate that fixes two parts together.

        Args:
            part1: First part (typically fixed)
            part2: Second part (to be positioned)
            location1: Location/orientation on part1
            location2: Location/orientation on part2
            name: Optional name for the mate

        Returns:
            Created rigid mate or None if creation failed
        """
        mate = self.assembly.mate_manager.create_mate(
            MateType.RIGID, part1, part2, name, location1=location1, location2=location2
        )
        return mate  # type: ignore[return-value]

    def revolute(
        self,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any,
        location2: Any,
        angle_range: Tuple[float, float] = (0, 360),
        current_angle: float = 0,
        name: str | None = None,
    ) -> "RevoluteMateInterface | None":
        """
        Create a revolute mate for hinge-like rotation.

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
        mate = self.assembly.mate_manager.create_mate(
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
        return mate  # type: ignore[return-value]

    def linear(
        self,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any,
        location2: Any,
        position_range: Tuple[float, float] = (0, float("inf")),
        current_position: float = 0,
        name: str | None = None,
    ) -> "LinearMateInterface | None":
        """
        Create a linear mate for sliding motion.

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
        mate = self.assembly.mate_manager.create_mate(
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
        return mate  # type: ignore[return-value]

    def cylindrical(
        self,
        part1: "Part",
        part2: "Part",
        axis: Any,
        location1: Any,
        location2: Any,
        position_range: Tuple[float, float] = (0, float("inf")),
        angle_range: Tuple[float, float] = (0, 360),
        current_position: float = 0,
        current_angle: float = 0,
        name: str | None = None,
    ) -> "CylindricalMateInterface | None":
        """
        Create a cylindrical mate for screw-like motion.

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
        mate = self.assembly.mate_manager.create_mate(
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
        return mate  # type: ignore[return-value]

    def ball(
        self,
        part1: "Part",
        part2: "Part",
        center_point: Any,
        location1: Any,
        location2: Any,
        angle_ranges: Tuple[
            Tuple[float, float], Tuple[float, float], Tuple[float, float]
        ] = ((0, 360), (0, 360), (0, 360)),
        current_angles: Tuple[float, float, float] = (0, 0, 0),
        name: str | None = None,
    ) -> "BallMateInterface | None":
        """
        Create a ball mate for gimbal-like motion.

        Args:
            part1: First part (typically fixed)
            part2: Second part (rotating)
            center_point: Center point of rotation
            location1: Location/orientation on part1 where joint attaches
            location2: Location/orientation on part2 where joint attaches
            angle_ranges: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) angle limits
            current_angles: (x, y, z) initial angles in degrees
            name: Optional name for the mate

        Returns:
            Created ball mate or None if creation failed
        """
        mate = self.assembly.mate_manager.create_mate(
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
        return mate  # type: ignore[return-value]

    # Geometric Mates (Static Constraints)

    def coincident(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        flip_alignment: bool = False,
        name: str | None = None,
    ) -> "CoincidentMateInterface | None":
        """
        Create a coincident mate to align geometric entities.

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
        mate = self.assembly.mate_manager.create_mate(
            MateType.COINCIDENT,
            part1,
            part2,
            name,
            entity1=entity1,
            entity2=entity2,
            flip_alignment=flip_alignment,
        )
        return mate  # type: ignore[return-value]

    def concentric(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "ConcentricMateInterface | None":
        """
        Create a concentric mate to align cylindrical features.

        Args:
            part1: First part
            part2: Second part
            entity1: Cylindrical/circular entity on part1
            entity2: Cylindrical/circular entity on part2
            name: Optional name for the mate

        Returns:
            Created concentric mate or None if creation failed
        """
        mate = self.assembly.mate_manager.create_mate(
            MateType.CONCENTRIC, part1, part2, name, entity1=entity1, entity2=entity2
        )
        return mate  # type: ignore[return-value]

    def distance(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        distance: float,
        name: str | None = None,
    ) -> "DistanceMateInterface | None":
        """
        Create a distance mate to maintain specific spacing.

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
        mate = self.assembly.mate_manager.create_mate(
            MateType.DISTANCE,
            part1,
            part2,
            name,
            entity1=entity1,
            entity2=entity2,
            distance=distance,
        )
        return mate  # type: ignore[return-value]

    def parallel(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "ParallelMateInterface | None":
        """
        Create a parallel mate to keep entities parallel.

        Args:
            part1: First part
            part2: Second part
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            name: Optional name for the mate

        Returns:
            Created parallel mate or None if creation failed
        """
        mate = self.assembly.mate_manager.create_mate(
            MateType.PARALLEL, part1, part2, name, entity1=entity1, entity2=entity2
        )
        return mate  # type: ignore[return-value]

    def perpendicular(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "PerpendicularMateInterface | None":
        """
        Create a perpendicular mate to keep entities perpendicular.

        Args:
            part1: First part
            part2: Second part
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            name: Optional name for the mate

        Returns:
            Created perpendicular mate or None if creation failed
        """
        mate = self.assembly.mate_manager.create_mate(
            MateType.PERPENDICULAR, part1, part2, name, entity1=entity1, entity2=entity2
        )
        return mate  # type: ignore[return-value]

    def tangent(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "TangentMateInterface | None":
        """
        Create a tangent mate to make surfaces tangent.

        Args:
            part1: First part
            part2: Second part
            entity1: Surface on part1
            entity2: Surface on part2
            name: Optional name for the mate

        Returns:
            Created tangent mate or None if creation failed
        """
        mate = self.assembly.mate_manager.create_mate(
            MateType.TANGENT, part1, part2, name, entity1=entity1, entity2=entity2
        )
        return mate  # type: ignore[return-value]

    def angle(
        self,
        part1: "Part",
        part2: "Part",
        entity1: Any,
        entity2: Any,
        angle: float,
        name: str | None = None,
    ) -> "AngleMateInterface | None":
        """
        Create an angle mate to maintain specific angle.

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
        mate = self.assembly.mate_manager.create_mate(
            MateType.ANGLE,
            part1,
            part2,
            name,
            entity1=entity1,
            entity2=entity2,
            angle=angle,
        )
        return mate  # type: ignore[return-value]
