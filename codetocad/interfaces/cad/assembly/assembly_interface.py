from abc import ABC
from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAddInterface
from codetocad.interfaces.cad.assembly.assembly_get import AssemblyGetInterface
from codetocad.interfaces.cad.assembly.assembly_transform_interface import (
    AssemblyTransformInterface,
)
from codetocad.interfaces.cad.assembly.assembly_export_interface import (
    AssemblyExportInterface,
)
from codetocad.interfaces.cad.assembly.assembly_geometry_interface import (
    AssemblyGeometryInterface,
)
from codetocad.interfaces.cad.part.part_interface import PartInterface


class AssemblyInterface(ABC):
    def __init__(self):
        self.parts: list[PartInterface] = []
        self.name: str | None = None

        self.add = AssemblyAddInterface(self)
        self.get = AssemblyGetInterface(self)

        # Method group properties
        self.transform = AssemblyTransformInterface(self)
        self.export = AssemblyExportInterface(self)
        self.geometry = AssemblyGeometryInterface(self)

    def set_name(self, name: str):
        """Set the assembly name."""
        self.name = name

    def add_part(self, part: PartInterface):
        """Add a part to the assembly."""
        if part not in self.parts:
            self.parts.append(part)
            if self not in part.member_assemblies:
                part.member_assemblies.append(self)

    def remove_part(self, part: PartInterface):
        """Remove a part from the assembly."""
        if part in self.parts:
            self.parts.remove(part)
            if self in part.member_assemblies:
                part.member_assemblies.remove(self)

    def get_part_by_name(self, name: str) -> PartInterface | None:
        """Get a part by name."""
        for part in self.parts:
            if part.name == name:
                return part
        return None

    def get_part_by_index(self, index: int) -> PartInterface:
        """Get a part by index."""
        return self.parts[index]

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the entire assembly."""
        if not self.parts:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes of all parts
        part_boxes = [part.get_bounding_box() for part in self.parts]

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

    def translate_all(self, _dx: float, _dy: float, _dz: float = 0):
        """Translate all parts in the assembly."""
        for part in self.parts:
            part.translate(_dx, _dy, _dz)

    def rotate_all(self, _axis: tuple[float, float, float], _angle: float):
        """Rotate all parts in the assembly."""
        for part in self.parts:
            part.rotate(_axis, _angle)

    def scale_all(self, _scale_x: float, _scale_y: float, _scale_z: float = 1.0):
        """Scale all parts in the assembly."""
        for part in self.parts:
            part.scale(_scale_x, _scale_y, _scale_z)

    def export_step(self, _file_path: str):
        """Export the assembly to STEP format."""
        pass

    def export_stl(self, _file_path: str, _tolerance: float = 0.1):
        """Export the assembly to STL format."""
        pass

    def export_brep(self, _file_path: str):
        """Export the assembly to BREP format."""
        pass

    def copy(self) -> "AssemblyInterface":
        """Create a copy of the assembly."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific assembly type
        raise NotImplementedError("copy must be implemented by concrete classes")

    def clear(self):
        """Remove all parts from the assembly."""
        for part in self.parts[:]:  # Create a copy of the list to iterate over
            self.remove_part(part)

    def move(self, _x: float, _y: float, _z: float):
        """Move all parts in the assembly."""
        for part in self.parts:
            part.move(_x, _y, _z)

    def rotate(self, _x: float, _y: float, _z: float):
        """Rotate all parts in the assembly."""
        for part in self.parts:
            # Convert to axis-angle representation for consistency
            import math

            # This is a simplified rotation - adapters should implement proper rotation
            magnitude = math.sqrt(_x * _x + _y * _y + _z * _z)
            if magnitude > 0:
                axis = (_x / magnitude, _y / magnitude, _z / magnitude)
                part.rotate(axis, magnitude)

    def scale(self, _x: float, _y: float | None = None, _z: float | None = None):
        """Scale all parts in the assembly."""
        y_val = _y if _y is not None else _x
        z_val = _z if _z is not None else _x
        for part in self.parts:
            part.scale(_x, y_val, z_val)

    def hide(self):
        """Hide the assembly."""
        for part in self.parts:
            part.hide()

    def show(self):
        """Show the assembly."""
        for part in self.parts:
            part.show()

    def delete(self):
        """Delete the assembly and all its parts."""
        for part in self.parts:
            part.delete()
        self.parts.clear()

    def __len__(self):
        """Get the number of parts in the assembly."""
        return len(self.parts)

    def __repr__(self):
        return f"<Assembly: {self.name}, {len(self.parts)} parts>"
