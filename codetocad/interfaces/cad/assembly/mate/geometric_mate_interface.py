"""
Interface for geometric assembly mates.

Geometric mates define static constraints between parts, such as coincident faces,
parallel edges, or concentric cylinders. These mates do not allow motion.
"""

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Union

from .mate_interface import MateInterface, MateType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class GeometricMateInterface(MateInterface):
    """
    Base interface for geometric assembly mates.

    Geometric mates constrain the position and orientation of parts
    without allowing any degrees of freedom for motion.
    """

    def __init__(
        self,
        name: str,
        mate_type: MateType,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        **kwargs,
    ):
        """
        Initialize a geometric mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of geometric mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Geometric entity on part1 (face, edge, vertex)
            entity2: Geometric entity on part2 (face, edge, vertex)
            **kwargs: Additional mate-specific parameters
        """
        super().__init__(name, mate_type, part1, part2, **kwargs)
        self.entity1 = entity1
        self.entity2 = entity2

    @abstractmethod
    def get_constraint_equations(self) -> List[Any]:
        """
        Get the mathematical constraint equations for this mate.

        Returns:
            List of constraint equations
        """
        pass

    @abstractmethod
    def calculate_transform(self) -> Optional[Tuple[float, ...]]:
        """
        Calculate the transformation needed to satisfy the mate constraint.

        Returns:
            Transformation parameters (translation, rotation) or None if invalid
        """
        pass


class CoincidentMateInterface(GeometricMateInterface):
    """
    Interface for coincident mates.

    Coincident mates align two geometric entities (faces, edges, or points)
    so they occupy the same location in space.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        flip_alignment: bool = False,
        **kwargs,
    ):
        """
        Initialize a coincident mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Geometric entity on part1
            entity2: Geometric entity on part2
            flip_alignment: Whether to flip the alignment direction
            **kwargs: Additional parameters
        """
        super().__init__(
            name, MateType.COINCIDENT, part1, part2, entity1, entity2, **kwargs
        )
        self.flip_alignment = flip_alignment


class ConcentricMateInterface(GeometricMateInterface):
    """
    Interface for concentric mates.

    Concentric mates align the axes of two cylindrical or circular features
    so they share the same centerline.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        **kwargs,
    ):
        """
        Initialize a concentric mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Cylindrical/circular entity on part1
            entity2: Cylindrical/circular entity on part2
            **kwargs: Additional parameters
        """
        super().__init__(
            name, MateType.CONCENTRIC, part1, part2, entity1, entity2, **kwargs
        )


class DistanceMateInterface(GeometricMateInterface):
    """
    Interface for distance mates.

    Distance mates maintain a specific distance between two geometric entities.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        distance: float,
        **kwargs,
    ):
        """
        Initialize a distance mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Geometric entity on part1
            entity2: Geometric entity on part2
            distance: Distance to maintain between entities
            **kwargs: Additional parameters
        """
        super().__init__(
            name, MateType.DISTANCE, part1, part2, entity1, entity2, **kwargs
        )
        self.distance = distance


class ParallelMateInterface(GeometricMateInterface):
    """
    Interface for parallel mates.

    Parallel mates keep two planar faces or linear edges parallel to each other.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        **kwargs,
    ):
        """
        Initialize a parallel mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            **kwargs: Additional parameters
        """
        super().__init__(
            name, MateType.PARALLEL, part1, part2, entity1, entity2, **kwargs
        )


class PerpendicularMateInterface(GeometricMateInterface):
    """
    Interface for perpendicular mates.

    Perpendicular mates keep two planar faces or linear edges perpendicular to each other.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        **kwargs,
    ):
        """
        Initialize a perpendicular mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            **kwargs: Additional parameters
        """
        super().__init__(
            name, MateType.PERPENDICULAR, part1, part2, entity1, entity2, **kwargs
        )


class TangentMateInterface(GeometricMateInterface):
    """
    Interface for tangent mates.

    Tangent mates make two surfaces tangent to each other at their point of contact.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        **kwargs,
    ):
        """
        Initialize a tangent mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Surface on part1
            entity2: Surface on part2
            **kwargs: Additional parameters
        """
        super().__init__(
            name, MateType.TANGENT, part1, part2, entity1, entity2, **kwargs
        )


class AngleMateInterface(GeometricMateInterface):
    """
    Interface for angle mates.

    Angle mates maintain a specific angle between two planar faces or linear edges.
    """

    def __init__(
        self,
        name: str,
        part1: "PartInterface",
        part2: "PartInterface",
        entity1: Any,
        entity2: Any,
        angle: float,
        **kwargs,
    ):
        """
        Initialize an angle mate.

        Args:
            name: Unique name for this mate
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            entity1: Planar face or linear edge on part1
            entity2: Planar face or linear edge on part2
            angle: Angle to maintain between entities (in degrees)
            **kwargs: Additional parameters
        """
        super().__init__(name, MateType.ANGLE, part1, part2, entity1, entity2, **kwargs)
        self.angle = angle
