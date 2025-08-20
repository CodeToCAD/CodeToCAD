"""
Base interface for assembly mates.

Assembly mates define relationships and constraints between parts in an assembly.
They can be geometric constraints (like coincident, parallel) or kinematic joints
(like revolute, linear) that allow controlled motion.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class MateType(Enum):
    """Types of assembly mates."""

    # Geometric constraint mates (no motion)
    COINCIDENT = "coincident"
    CONCENTRIC = "concentric"
    DISTANCE = "distance"
    PARALLEL = "parallel"
    PERPENDICULAR = "perpendicular"
    TANGENT = "tangent"
    ANGLE = "angle"

    # Kinematic mates (allow motion)
    RIGID = "rigid"
    REVOLUTE = "revolute"
    LINEAR = "linear"
    CYLINDRICAL = "cylindrical"
    BALL = "ball"


class MateStatus(Enum):
    """Status of a mate constraint."""

    ACTIVE = "active"
    SUPPRESSED = "suppressed"
    FAILED = "failed"
    UNDEFINED = "undefined"


class MateInterface(ABC):
    """
    Base interface for assembly mates.

    A mate defines a relationship between two parts in an assembly,
    constraining their relative position and/or orientation.
    """

    def __init__(
        self,
        name: str,
        mate_type: MateType,
        part1: "PartInterface",
        part2: "PartInterface",
        **kwargs,
    ):
        """
        Initialize a mate.

        Args:
            name: Unique name for this mate
            mate_type: Type of mate constraint
            part1: First part in the mate relationship
            part2: Second part in the mate relationship
            **kwargs: Additional mate-specific parameters
        """
        self.name = name
        self.mate_type = mate_type
        self.part1 = part1
        self.part2 = part2
        self.status = MateStatus.UNDEFINED
        self.parameters = kwargs

    @abstractmethod
    def apply(self) -> bool:
        """
        Apply the mate constraint.

        Returns:
            True if the mate was successfully applied, False otherwise
        """
        pass

    @abstractmethod
    def remove(self) -> bool:
        """
        Remove the mate constraint.

        Returns:
            True if the mate was successfully removed, False otherwise
        """
        pass

    @abstractmethod
    def update(self, **kwargs) -> bool:
        """
        Update mate parameters.

        Args:
            **kwargs: Updated parameters

        Returns:
            True if the mate was successfully updated, False otherwise
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Check if the mate constraint is valid.

        Returns:
            True if the mate is valid, False otherwise
        """
        pass

    def suppress(self) -> bool:
        """
        Suppress the mate (temporarily disable it).

        Returns:
            True if successfully suppressed, False otherwise
        """
        if self.status == MateStatus.ACTIVE:
            self.status = MateStatus.SUPPRESSED
            return True
        return False

    def unsuppress(self) -> bool:
        """
        Unsuppress the mate (re-enable it).

        Returns:
            True if successfully unsuppressed, False otherwise
        """
        if self.status == MateStatus.SUPPRESSED:
            self.status = MateStatus.ACTIVE
            return self.apply()
        return False

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a mate parameter value.

        Args:
            key: Parameter name
            default: Default value if parameter doesn't exist

        Returns:
            Parameter value or default
        """
        return self.parameters.get(key, default)

    def set_parameter(self, key: str, value: Any) -> bool:
        """
        Set a mate parameter value.

        Args:
            key: Parameter name
            value: Parameter value

        Returns:
            True if parameter was set successfully, False otherwise
        """
        self.parameters[key] = value
        return self.update(**{key: value})

    def __str__(self) -> str:
        """String representation of the mate."""
        return f"{self.mate_type.value.title()}Mate({self.name}): {self.part1.name} <-> {self.part2.name}"

    def __repr__(self) -> str:
        """Detailed string representation of the mate."""
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"type={self.mate_type.value}, "
            f"part1='{self.part1.name}', "
            f"part2='{self.part2.name}', "
            f"status={self.status.value})"
        )
