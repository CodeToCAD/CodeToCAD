"""
build123d implementation of PartBooleanInterface.
"""

from codetocad.interfaces.cad.part.part_boolean_interface import PartBooleanInterface
from codetocad.adapters.build123d.build123d_actions.geometry import (
    boolean_union,
    boolean_difference,
    boolean_intersection,
)
from codetocad.interfaces.cad.part.part_interface import PartInterface


class PartBoolean(PartBooleanInterface):
    """build123d implementation of part boolean operations."""

    def union(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean union with another part."""
        if not self.part.native_instance or not other.native_instance:
            raise ValueError(
                "Both parts must have native instances for boolean operations"
            )

        # Import here to avoid circular imports
        from codetocad.adapters.build123d.cad.part.part import Part

        result_part = Part(f"{self.part.name}_union_{other.name}")
        result_part.native_instance = boolean_union(
            self.part.native_instance, other.native_instance
        )
        return result_part

    def difference(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean difference with another part."""
        if not self.part.native_instance or not other.native_instance:
            raise ValueError(
                "Both parts must have native instances for boolean operations"
            )

        # Import here to avoid circular imports
        from codetocad.adapters.build123d.cad.part.part import Part

        result_part = Part(f"{self.part.name}_difference_{other.name}")
        result_part.native_instance = boolean_difference(
            self.part.native_instance, other.native_instance
        )
        return result_part

    def intersection(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean intersection with another part."""
        if not self.part.native_instance or not other.native_instance:
            raise ValueError(
                "Both parts must have native instances for boolean operations"
            )

        # Import here to avoid circular imports
        from codetocad.adapters.build123d.cad.part.part import Part

        result_part = Part(f"{self.part.name}_intersection_{other.name}")
        result_part.native_instance = boolean_intersection(
            self.part.native_instance, other.native_instance
        )
        return result_part
