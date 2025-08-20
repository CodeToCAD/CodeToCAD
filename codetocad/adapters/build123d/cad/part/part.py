"""
build123d implementation of PartInterface.
"""

from typing import TYPE_CHECKING, List, Optional
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
    boolean_union,
    boolean_difference,
    boolean_intersection,
)
from codetocad.adapters.build123d.build123d_actions.transformations import (
    translate_object,
    rotate_object,
    scale_object,
    get_volume,
    get_bounding_box,
)
from codetocad.adapters.build123d.build123d_actions.export import (
    export_step,
    export_stl,
    export_brep,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.assembly.assembly import Assembly
    import build123d as bd


class Part(PartInterface, metaclass=_PartPresetClassProperty):
    """build123d implementation of PartInterface."""

    def __init__(self, name: str | None = None):
        # build123d-specific properties
        self.name = name or f"part_{str(uuid4())[:8]}"
        self.native_instance: Optional["bd.Solid"] = None
        self.member_assemblies: List["Assembly"] = []

        # Initialize sketch
        self.sketch = Sketch(f"{self.name}_sketch")

    def set_name(self, name: str):
        """Set the part name."""
        self.name = name

    @classmethod
    def get_by_name(cls, name: str) -> "Part| None":
        """Get a part by name (placeholder implementation)."""
        # TODO: Implement part registry/lookup system
        return None

    def extrude_sketch(self, distance: LengthType) -> "Part":
        """Extrude the part's sketch to create a solid."""
        if not self.sketch.wires:
            raise ValueError("No wires in sketch to extrude")

        # Get the first wire and create a face
        first_wire = self.sketch.wires[0]
        if first_wire.native_instance:
            face = create_face_from_wire(first_wire.native_instance)
            self.native_instance = extrude_face(face, distance)

        return self

    def union(self, other: "Part") -> "Part":
        """Perform boolean union with another part."""
        if not self.native_instance or not other.native_instance:
            raise ValueError(
                "Both parts must have native instances for boolean operations"
            )

        result_part = Part(f"{self.name}_union_{other.name}")
        result_part.native_instance = boolean_union(
            self.native_instance, other.native_instance
        )

        return result_part

    def difference(self, other: "Part") -> "Part":
        """Perform boolean difference with another part."""
        if not self.native_instance or not other.native_instance:
            raise ValueError(
                "Both parts must have native instances for boolean operations"
            )

        result_part = Part(f"{self.name}_difference_{other.name}")
        result_part.native_instance = boolean_difference(
            self.native_instance, other.native_instance
        )

        return result_part

    def intersection(self, other: "Part") -> "Part":
        """Perform boolean intersection with another part."""
        if not self.native_instance or not other.native_instance:
            raise ValueError(
                "Both parts must have native instances for boolean operations"
            )

        result_part = Part(f"{self.name}_intersection_{other.name}")
        result_part.native_instance = boolean_intersection(
            self.native_instance, other.native_instance
        )

        return result_part

    def translate(self, dx: LengthType, dy: LengthType, dz: LengthType = 0) -> "Part":
        """Translate the part."""
        if self.native_instance:
            self.native_instance = translate_object(self.native_instance, dx, dy, dz)
        return self

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "Part":
        """Rotate the part around an axis."""
        if self.native_instance:
            import build123d as bd

            axis_vector = bd.Vector(*axis)
            self.native_instance = rotate_object(
                self.native_instance, axis_vector, angle
            )
        return self

    def scale(self, scale_x: float, scale_y: float, scale_z: float = 1.0) -> "Part":
        """Scale the part."""
        if self.native_instance:
            self.native_instance = scale_object(
                self.native_instance, scale_x, scale_y, scale_z
            )
        return self

    def get_volume(self) -> float:
        """Get the volume of the part."""
        if not self.native_instance:
            return 0.0
        return get_volume(self.native_instance)

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        if not self.native_instance:
            return ((0, 0, 0), (0, 0, 0))

        bbox = get_bounding_box(self.native_instance)
        min_point = (bbox.min.X, bbox.min.Y, bbox.min.Z)
        max_point = (bbox.max.X, bbox.max.Y, bbox.max.Z)

        return (min_point, max_point)

    def export_step(self, file_path: str):
        """Export the part to STEP format."""
        if not self.native_instance:
            raise ValueError("No native instance to export")
        export_step(self.native_instance, file_path)

    def export_stl(self, file_path: str, tolerance: float = 0.1):
        """Export the part to STL format."""
        if not self.native_instance:
            raise ValueError("No native instance to export")
        export_stl(self.native_instance, file_path, tolerance)

    def export_brep(self, file_path: str):
        """Export the part to BREP format."""
        if not self.native_instance:
            raise ValueError("No native instance to export")
        export_brep(self.native_instance, file_path)

    def copy(self) -> "Part":
        """Create a copy of the part."""
        new_part = Part(f"{self.name}_copy")

        # Copy the sketch
        new_part.sketch = self.sketch.copy()

        # Copy the native instance if it exists
        if self.native_instance:
            # build123d objects are immutable, so we can share the reference
            # or create a copy if needed
            new_part.native_instance = self.native_instance

        return new_part

    def __repr__(self):
        return f"<Part: {self.name or 'Unnamed'}. {self.sketch}>"
