"""
build123d implementation of PartInterface.
"""

from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.interfaces.cad.part.part_interface import PartInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.cad.sketch.sketch import Sketch
from codetocad.adapters.build123d.cad.part.part_preset_class_property import (
    _PartPresetClassProperty,
)
from codetocad.adapters.build123d.build123d_actions.geometry import (
    extrude_face,
    create_face_from_wire,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.assembly.assembly import Assembly
    import build123d as bd


class Part(PartInterface, metaclass=_PartPresetClassProperty):
    """build123d implementation of PartInterface."""

    def __init__(self, name: str | None = None):
        # Initialize parent interface first
        super().__init__()

        # build123d-specific properties
        self.name = name or f"part_{str(uuid4())[:8]}"
        self.native_instance: "bd.Part | None" = None
        self.member_assemblies: list["Assembly"] = []

        # Initialize sketch
        self.sketch = Sketch(f"{self.name}_sketch")

        # Override method group properties with build123d-specific implementations
        from codetocad.adapters.build123d.cad.part.part_transform import PartTransform
        from codetocad.adapters.build123d.cad.part.part_export import PartExport
        from codetocad.adapters.build123d.cad.part.part_boolean import PartBoolean
        from codetocad.adapters.build123d.cad.part.part_geometry import PartGeometry

        self.transform = PartTransform(self)
        self.export = PartExport(self)
        self.boolean = PartBoolean(self)
        self.geometry = PartGeometry(self)

    def set_name(self, name: str):
        """Set the part name."""
        self.name = name

    @classmethod
    def get_by_name(cls, name: str) -> "Part | None":
        """Get a part by name (placeholder implementation)."""
        # TODO: Implement part registry/lookup system
        _ = name  # Suppress unused parameter warning
        return None

    def extrude_sketch(self, distance: LengthType) -> "Part":
        """Extrude the part's sketch to create a solid."""
        if not self.sketch.wires:
            raise ValueError("No wires in sketch to extrude")

        # Get the first wire and create a face
        first_wire = self.sketch.wires[0]
        if hasattr(first_wire, "native_instance") and first_wire.native_instance:
            face = create_face_from_wire(first_wire.native_instance)
            self.native_instance = extrude_face(face, distance)

        return self

    def copy(self) -> "Part":
        """Create a copy of the part."""
        new_part = Part(f"{self.name}_copy")

        # Copy the sketch using operations interface
        new_part.sketch = self.sketch.operations.copy()

        # Copy the native instance if it exists
        if self.native_instance:
            # build123d objects are immutable, so we can share the reference
            # or create a copy if needed
            new_part.native_instance = self.native_instance

        return new_part

    def __repr__(self):
        return f"<Part: {self.name or 'Unnamed'}. {self.sketch}>"
