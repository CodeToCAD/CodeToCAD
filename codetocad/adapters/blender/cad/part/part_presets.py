from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.adapters.blender.blender_actions.context import get_selected_objects
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.blender.blender_actions.objects import (
    add_primitive,
    update_object_data_name,
    update_object_name,
)
from codetocad.adapters.blender.blender_definitions import BlenderObjectPrimitiveTypes

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly
    from codetocad.adapters.blender.cad.part.part import Part


class PartPresets(PartPresetsInterface):
    """Blender-specific part presets."""

    def __init__(self, assembly: "Assembly|None" = None):
        self.assembly = assembly

    def _post_creation_do_this(self, part: "Part"):
        blender_obj = get_selected_objects()[0]
        if not blender_obj:
            raise Exception("Failed to create cube.")

        part._blender_object = blender_obj
        part.set_name(part.name)

        if self.assembly:
            self.assembly.parts.append(part)

    def cube(self, x: LengthType, y: LengthType, z: LengthType) -> "Part":
        """Create a cube part using Blender primitives."""
        from codetocad.adapters.blender.cad.part.part import Part

        part = Part()
        part.set_name(f"cube_{str(uuid4())[:8]}")

        # Create cube using Blender primitive
        dimensions = [float(x), float(y), float(z)]
        add_primitive(BlenderObjectPrimitiveTypes.cube, dimensions)

        self._post_creation_do_this(part)

        return part

    def cylinder(self, radius: LengthType, height: LengthType) -> "Part":
        """Create a cylinder part using Blender primitives."""
        from codetocad.adapters.blender.cad.part.part import Part

        part = Part()
        part.set_name(f"cylinder_{str(uuid4())[:8]}")

        # Create cylinder using Blender primitive
        dimensions = [float(radius), float(height)]
        add_primitive(BlenderObjectPrimitiveTypes.cylinder, dimensions)

        self._post_creation_do_this(part)

        return part

    def sphere(self, radius: LengthType) -> "Part":
        """Create a sphere part using Blender primitives."""
        from codetocad.adapters.blender.cad.part.part import Part

        part = Part()
        part.set_name(f"sphere_{str(uuid4())[:8]}")

        # Create sphere using Blender primitive
        dimensions = [float(radius)]
        add_primitive(BlenderObjectPrimitiveTypes.uvsphere, dimensions)

        self._post_creation_do_this(part)

        return part
