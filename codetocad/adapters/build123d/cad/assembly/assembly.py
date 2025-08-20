"""
build123d implementation of AssemblyInterface.
"""

from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAddInterface
from codetocad.interfaces.cad.assembly.assembly_get import AssemblyGetInterface
from codetocad.adapters.build123d.build123d_actions.export import (
    export_step,
    export_stl,
    export_brep,
)
from codetocad.adapters.build123d.build123d_actions.transformations import (
    translate_object,
    rotate_object,
    scale_object,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.part.part import Part
    import build123d as bd


class Assembly(AssemblyInterface):
    """build123d implementation of AssemblyInterface."""

    def __init__(self, name: str | None = None):
        # Initialize parent interface first
        super().__init__()

        # build123d-specific properties
        self.name = name or f"assembly_{str(uuid4())[:8]}"

        # Initialize parent interface
        from codetocad.adapters.build123d.cad.part.part import Part

        self.parts: list[Part] = []  # type: ignore

        self.add = AssemblyAddInterface(self)
        self.get = AssemblyGetInterface(self)

    def set_name(self, name: str):
        """Set the assembly name."""
        self.name = name

    def add_part(self, part: "Part"):
        """Add a part to the assembly."""
        if part not in self.parts:
            self.parts.append(part)
            if self not in part.member_assemblies:
                part.member_assemblies.append(self)

    def remove_part(self, part: "Part"):
        """Remove a part from the assembly."""
        if part in self.parts:
            self.parts.remove(part)
            if self in part.member_assemblies:
                part.member_assemblies.remove(self)

    def get_part_by_name(self, name: str) -> "Part | None":
        """Get a part by name."""
        for part in self.parts:
            if part.name == name:
                return part
        return None

    def get_part_by_index(self, index: int) -> "Part":
        """Get a part by index."""
        return self.parts[index]

    def get_all_native_instances(self) -> list["bd.Solid"]:
        """Get all native build123d instances from parts."""
        instances = []
        for part in self.parts:
            if part.native_instance:
                instances.append(part.native_instance)
        return instances

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the entire assembly."""
        if not self.parts:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes of all parts
        part_boxes = [
            part.get_bounding_box() for part in self.parts if part.native_instance
        ]

        if not part_boxes:
            return ((0, 0, 0), (0, 0, 0))

        # Find overall min and max
        min_x = min(box[0][0] for box in part_boxes)
        min_y = min(box[0][1] for box in part_boxes)
        min_z = min(box[0][2] for box in part_boxes)

        max_x = max(box[1][0] for box in part_boxes)
        max_y = max(box[1][1] for box in part_boxes)
        max_z = max(box[1][2] for box in part_boxes)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def get_total_volume(self) -> float:
        """Get the total volume of all parts in the assembly."""
        return sum(part.get_volume() for part in self.parts)

    def translate_all(self, dx, dy, dz=0):
        """Translate all parts in the assembly."""
        for part in self.parts:
            part.translate(dx, dy, dz)

    def rotate_all(self, axis: tuple[float, float, float], angle: float):
        """Rotate all parts in the assembly."""
        for part in self.parts:
            part.rotate(axis, angle)

    def scale_all(self, scale_x: float, scale_y: float, scale_z: float = 1.0):
        """Scale all parts in the assembly."""
        for part in self.parts:
            part.scale(scale_x, scale_y, scale_z)

    def export_step(self, file_path: str):
        """Export the assembly to STEP format."""
        instances = self.get_all_native_instances()
        if not instances:
            raise ValueError("No parts with native instances to export")
        export_step(instances, file_path)

    def export_stl(self, file_path: str, tolerance: float = 0.1):
        """Export the assembly to STL format."""
        instances = self.get_all_native_instances()
        if not instances:
            raise ValueError("No parts with native instances to export")
        export_stl(instances, file_path, tolerance)

    def export_brep(self, file_path: str):
        """Export the assembly to BREP format."""
        instances = self.get_all_native_instances()
        if not instances:
            raise ValueError("No parts with native instances to export")
        export_brep(instances, file_path)

    def create_compound(self) -> "bd.Compound":
        """Create a build123d compound from all parts."""
        import build123d as bd

        instances = self.get_all_native_instances()
        if not instances:
            raise ValueError("No parts with native instances to create compound")
        return bd.Compound.make_compound(instances)

    def union_all(self) -> "Part":
        """Create a single part by unioning all parts in the assembly."""
        if not self.parts:
            raise ValueError("No parts in assembly to union")

        if len(self.parts) == 1:
            return self.parts[0].copy()

        # Start with the first part
        result = self.parts[0].copy()

        # Union with all other parts
        for part in self.parts[1:]:
            result = result.union(part)

        result.set_name(f"{self.name}_union")
        return result

    def copy(self) -> "Assembly":
        """Create a copy of the assembly."""
        new_assembly = Assembly(f"{self.name}_copy")

        # Copy all parts
        for part in self.parts:
            new_part = part.copy()
            new_assembly.add_part(new_part)

        return new_assembly

    def clear(self):
        """Remove all parts from the assembly."""
        for part in self.parts[:]:  # Create a copy of the list to iterate over
            self.remove_part(part)

    def __len__(self):
        """Get the number of parts in the assembly."""
        return len(self.parts)

    def __repr__(self):
        return f"<Assembly: {self.name}, {len(self.parts)} parts>"
