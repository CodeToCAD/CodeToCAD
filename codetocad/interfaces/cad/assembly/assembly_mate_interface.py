"""
Assembly mate interface for fluent mate creation API.

This interface provides intuitive methods for creating different types of mates
between parts in an assembly, using a fluent API approach.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Tuple

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.assembly.mate.mate_interface import MateInterface


class AssemblyMateInterface(ABC):
    """
    Interface for fluent mate creation in assemblies.

    Provides intuitive methods for creating different types of mates
    between parts using a fluent API approach.
    """

    def __init__(self, assembly: "AssemblyInterface"):
        """
        Initialize the assembly mate interface.

        Args:
            assembly: The assembly this mate interface belongs to
        """
        self.assembly = assembly

    # Kinematic Mates (Motion-based)

    @abstractmethod
    def rigid(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        location1: Any,
        location2: Any,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def revolute(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        axis: Any,
        location1: Any,
        location2: Any,
        angle_range: tuple[float, float] = (0, 360),
        current_angle: float = 0,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def linear(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        axis: Any,
        location1: Any,
        location2: Any,
        position_range: tuple[float, float] = (0, float("inf")),
        current_position: float = 0,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def cylindrical(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        axis: Any,
        location1: Any,
        location2: Any,
        position_range: tuple[float, float] = (0, float("inf")),
        angle_range: tuple[float, float] = (0, 360),
        current_position: float = 0,
        current_angle: float = 0,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def ball(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        center_point: Any,
        location1: Any,
        location2: Any,
        angle_ranges: tuple[
            tuple[float, float], tuple[float, float], tuple[float, float]
        ] = ((0, 360), (0, 360), (0, 360)),
        current_angles: tuple[float, float, float] = (0, 0, 0),
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    # Geometric Mates (Static Constraints)

    @abstractmethod
    def coincident(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        flip_alignment: bool = False,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def concentric(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def distance(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        distance: float,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def parallel(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def perpendicular(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def tangent(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass

    @abstractmethod
    def angle(
        self,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        angle: float,
        name: str | None = None,
    ) -> "MateInterface|None":
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
        pass
