import bmesh
from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.adapters.blender.cad.blender_constraint import BlenderObjectConstraint


from codetocad.interfaces.cad.part.part_interface import PartInterface
from codetocad.core.dimensions.length_expression import LengthType, LengthExpression
from codetocad.adapters.blender.cad.sketch.sketch import Sketch
from codetocad.adapters.blender.blender_actions.objects import (
    create_object,
    update_object_data_name,
    update_object_name,
    get_object,
    remove_object,
)
from codetocad.adapters.blender.blender_actions.objects_transmute import (
    create_mesh_from_curve,
)
from codetocad.adapters.blender.blender_actions.modifiers import (
    apply_solidify_modifier,
    apply_boolean_modifier,
)
from codetocad.adapters.blender.blender_definitions import BlenderBooleanTypes
from codetocad.adapters.blender.cad.part.part_preset_class_property import (
    _PartPresetClassProperty,
)

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly
    import bpy


class Part(PartInterface, metaclass=_PartPresetClassProperty):
    """Blender implementation of PartInterface."""

    def __init__(self, name: str | None = None):
        # Initialize parent interface first
        super().__init__()

        # Blender-specific properties
        self.name = name or f"part_{str(uuid4())[:8]}"
        self._blender_object: bpy.types.Object | None = None

        self.sketch: Sketch = Sketch(f"{self.name}_sketch")

        # Override method group properties with Blender-specific implementations
        from codetocad.adapters.blender.cad.part.part_transform import PartTransform
        from codetocad.adapters.blender.cad.part.part_export import PartExport
        from codetocad.adapters.blender.cad.part.part_boolean import PartBoolean
        from codetocad.adapters.blender.cad.part.part_geometry import PartGeometry

        self.transform = PartTransform(self)
        self.export = PartExport(self)
        self.boolean = PartBoolean(self)
        self.geometry = PartGeometry(self)

        # Initialize constraints property (will be set when Blender object is created)
        self._constraints: BlenderObjectConstraint | None = None

    def set_name(self, name: str):
        """Set the part name and update Blender object."""
        self.name = name
        if self._blender_object:
            update_object_name(self._blender_object, name)
            update_object_data_name(self._blender_object, name)

    @classmethod
    def get_by_name(cls, name: str) -> "Part| None":
        """Get a part by name from the Blender scene."""
        blender_obj = get_object(name)
        if blender_obj:
            part = cls(name)
            part._blender_object = blender_obj
            return part
        return None

    def get_blender_object(self) -> "bpy.types.Object | None":
        """Get the Blender object representing this part."""
        return self._blender_object

    @property
    def constraints(self):
        """Initialize the constraints interface when Blender object is available."""
        if not self._blender_object:
            raise ValueError("Blender object not created for part")
        if self._constraints is None:
            self._constraints = BlenderObjectConstraint(self._blender_object)
        return self._constraints

    def create_from_sketch(self):
        """Create a 3D part from the sketch by extruding."""
        if not self.sketch.wires:
            return

        # Convert sketch wires to mesh
        for wire in self.sketch.wires:
            wire_obj = wire.get_blender_object()
            if wire_obj and isinstance(wire_obj.data, bpy.types.Curve):
                # Convert curve to mesh
                mesh_obj = create_mesh_from_curve(wire_obj, f"{self.name}_mesh")
                if mesh_obj:
                    self._blender_object = mesh_obj

    def extrude_sketch(self, distance: LengthType) -> "Part":
        """Extrude the part's sketch to create a solid."""
        if not self.sketch.wires:
            raise ValueError("No wires in sketch to extrude")

        # Create from sketch first if not already done
        if not self._blender_object:
            self.create_from_sketch()

        # Apply extrusion
        self.extrude(distance)
        return self

    def extrude(self, distance: LengthType):
        """Extrude the part along its normal."""
        if not self._blender_object:
            self.create_from_sketch()

        if self._blender_object and isinstance(
            self._blender_object.data, bpy.types.Mesh
        ):
            # Add solidify modifier for extrusion
            apply_solidify_modifier(self._blender_object, float(distance))

    def copy(self) -> "Part":
        """Create a copy of the part."""
        new_part = Part(f"{self.name}_copy")

        # Copy the sketch using operations interface
        new_part.sketch = self.sketch.operations.copy()

        # Create Blender representation for the copy
        new_part.create_from_sketch()

        return new_part

    def hide(self):
        """Hide the part in Blender."""
        if self._blender_object:
            self._blender_object.hide_viewport = True

    def show(self):
        """Show the part in Blender."""
        if self._blender_object:
            self._blender_object.hide_viewport = False

    def delete(self):
        """Delete the part from Blender."""
        if self._blender_object:
            # Remove from scene
            remove_object(self._blender_object)
            self._blender_object = None

    def __repr__(self):
        return f"<Part(name='{self.name}'): {self.sketch}>"
