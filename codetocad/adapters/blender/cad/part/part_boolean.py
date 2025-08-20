"""
Blender implementation of PartBooleanInterface.
"""

from codetocad.interfaces.cad.part.part_boolean_interface import PartBooleanInterface
from codetocad.adapters.blender.blender_actions.modifiers import (
    apply_boolean_modifier,
    BlenderBooleanTypes,
)


class PartBoolean(PartBooleanInterface):
    """Blender implementation of part boolean operations."""

    def union(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean union with another part."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.part.part import Part

        if not isinstance(other, Part):
            raise TypeError(
                "Can only perform boolean operations with other Blender Parts"
            )

        result_part = Part(f"{self.part.name}_union_{other.name}")

        # Copy this part's data to result
        result_part.sketch = self.part.sketch.operations.copy()
        result_part.create_from_sketch()

        # Apply boolean union
        if result_part._blender_object and other._blender_object:
            apply_boolean_modifier(
                result_part._blender_object,
                BlenderBooleanTypes.UNION,
                other._blender_object,
            )

        return result_part

    def difference(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean difference with another part."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.part.part import Part

        if not isinstance(other, Part):
            raise TypeError(
                "Can only perform boolean operations with other Blender Parts"
            )

        result_part = Part(f"{self.part.name}_difference_{other.name}")

        # Copy this part's data to result
        result_part.sketch = self.part.sketch.operations.copy()
        result_part.create_from_sketch()

        # Apply boolean difference
        if result_part._blender_object and other._blender_object:
            apply_boolean_modifier(
                result_part._blender_object,
                BlenderBooleanTypes.DIFFERENCE,
                other._blender_object,
            )

        return result_part

    def intersection(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean intersection with another part."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.part.part import Part

        if not isinstance(other, Part):
            raise TypeError(
                "Can only perform boolean operations with other Blender Parts"
            )

        result_part = Part(f"{self.part.name}_intersection_{other.name}")

        # Copy this part's data to result
        result_part.sketch = self.part.sketch.operations.copy()
        result_part.create_from_sketch()

        # Apply boolean intersection
        if result_part._blender_object and other._blender_object:
            apply_boolean_modifier(
                result_part._blender_object,
                BlenderBooleanTypes.INTERSECT,
                other._blender_object,
            )

        return result_part
