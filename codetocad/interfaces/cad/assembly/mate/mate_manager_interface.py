"""
Interface for managing assembly mates.

The mate manager handles collections of mates within an assembly,
providing methods to create, modify, delete, and solve mate constraints.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from .mate_interface import MateInterface, MateType, MateStatus

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class MateManagerInterface(ABC):
    """
    Interface for managing assembly mates.

    The mate manager is responsible for:
    - Creating and managing mate constraints
    - Solving constraint systems
    - Maintaining mate relationships
    - Handling mate conflicts and failures
    """

    def __init__(self, assembly: "AssemblyInterface"):
        """
        Initialize the mate manager.

        Args:
            assembly: The assembly this manager belongs to
        """
        self.assembly = assembly
        self.mates: Dict[str, MateInterface] = {}
        self._mate_counter = 0

    @abstractmethod
    def create_mate(
        self,
        mate_type: MateType,
        part1: "PartInterface",
        part2: "PartInterface",
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
        pass

    @abstractmethod
    def remove_mate(self, mate_name: str) -> bool:
        """
        Remove a mate constraint.

        Args:
            mate_name: Name of the mate to remove

        Returns:
            True if mate was removed successfully, False otherwise
        """
        pass

    @abstractmethod
    def solve_mates(self) -> bool:
        """
        Solve all active mate constraints.

        Returns:
            True if all mates were solved successfully, False otherwise
        """
        pass

    @abstractmethod
    def validate_mates(self) -> Dict[str, bool]:
        """
        Validate all mates in the assembly.

        Returns:
            Dictionary mapping mate names to their validity status
        """
        pass

    def get_mate(self, name: str) -> Optional[MateInterface]:
        """
        Get a mate by name.

        Args:
            name: Name of the mate

        Returns:
            Mate instance or None if not found
        """
        return self.mates.get(name)

    def get_mates_by_type(self, mate_type: MateType) -> List[MateInterface]:
        """
        Get all mates of a specific type.

        Args:
            mate_type: Type of mates to retrieve

        Returns:
            List of mates of the specified type
        """
        return [mate for mate in self.mates.values() if mate.mate_type == mate_type]

    def get_mates_by_part(self, part: "PartInterface") -> List[MateInterface]:
        """
        Get all mates involving a specific part.

        Args:
            part: Part to search for

        Returns:
            List of mates involving the specified part
        """
        return [
            mate
            for mate in self.mates.values()
            if mate.part1 == part or mate.part2 == part
        ]

    def get_mates_by_status(self, status: MateStatus) -> List[MateInterface]:
        """
        Get all mates with a specific status.

        Args:
            status: Status to filter by

        Returns:
            List of mates with the specified status
        """
        return [mate for mate in self.mates.values() if mate.status == status]

    def get_all_mates(self) -> List[MateInterface]:
        """
        Get all mates in the assembly.

        Returns:
            List of all mates
        """
        return list(self.mates.values())

    def suppress_mate(self, mate_name: str) -> bool:
        """
        Suppress a mate (temporarily disable it).

        Args:
            mate_name: Name of the mate to suppress

        Returns:
            True if mate was suppressed successfully, False otherwise
        """
        mate = self.get_mate(mate_name)
        if mate:
            return mate.suppress()
        return False

    def unsuppress_mate(self, mate_name: str) -> bool:
        """
        Unsuppress a mate (re-enable it).

        Args:
            mate_name: Name of the mate to unsuppress

        Returns:
            True if mate was unsuppressed successfully, False otherwise
        """
        mate = self.get_mate(mate_name)
        if mate:
            return mate.unsuppress()
        return False

    def update_mate(self, mate_name: str, **kwargs) -> bool:
        """
        Update a mate's parameters.

        Args:
            mate_name: Name of the mate to update
            **kwargs: Updated parameters

        Returns:
            True if mate was updated successfully, False otherwise
        """
        mate = self.get_mate(mate_name)
        if mate:
            return mate.update(**kwargs)
        return False

    def clear_all_mates(self) -> bool:
        """
        Remove all mates from the assembly.

        Returns:
            True if all mates were removed successfully, False otherwise
        """
        mate_names = list(self.mates.keys())
        success = True
        for name in mate_names:
            if not self.remove_mate(name):
                success = False
        return success

    def get_mate_count(self) -> int:
        """
        Get the total number of mates.

        Returns:
            Number of mates in the assembly
        """
        return len(self.mates)

    def get_mate_statistics(self) -> Dict[str, int]:
        """
        Get statistics about mates in the assembly.

        Returns:
            Dictionary with mate statistics
        """
        stats = {
            "total": len(self.mates),
            "active": len(self.get_mates_by_status(MateStatus.ACTIVE)),
            "suppressed": len(self.get_mates_by_status(MateStatus.SUPPRESSED)),
            "failed": len(self.get_mates_by_status(MateStatus.FAILED)),
            "undefined": len(self.get_mates_by_status(MateStatus.UNDEFINED)),
        }

        # Add counts by mate type
        for mate_type in MateType:
            stats[mate_type.value] = len(self.get_mates_by_type(mate_type))

        return stats

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

    def __len__(self) -> int:
        """Return the number of mates."""
        return len(self.mates)

    def __contains__(self, mate_name: str) -> bool:
        """Check if a mate exists."""
        return mate_name in self.mates

    def __iter__(self):
        """Iterate over mates."""
        return iter(self.mates.values())

    def __str__(self) -> str:
        """String representation of the mate manager."""
        return f"MateManager({len(self.mates)} mates)"

    def __repr__(self) -> str:
        """Detailed string representation of the mate manager."""
        stats = self.get_mate_statistics()
        return (
            f"{self.__class__.__name__}("
            f"assembly='{self.assembly.name}', "
            f"total_mates={stats['total']}, "
            f"active={stats['active']}, "
            f"suppressed={stats['suppressed']}, "
            f"failed={stats['failed']})"
        )
