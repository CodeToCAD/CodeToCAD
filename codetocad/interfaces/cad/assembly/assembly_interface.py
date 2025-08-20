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

    def copy(self) -> "AssemblyInterface":
        """Create a copy of the assembly."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific assembly type
        raise NotImplementedError("copy must be implemented by concrete classes")

    def clear(self):
        """Remove all parts from the assembly."""
        for part in self.parts[:]:  # Create a copy of the list to iterate over
            self.remove_part(part)

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
