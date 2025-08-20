"""
build123d implementation of AssemblyInterface.
"""

from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAddInterface
from codetocad.interfaces.cad.assembly.assembly_get import AssemblyGetInterface

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

        # Override method group properties with build123d-specific implementations
        from codetocad.adapters.build123d.cad.assembly.assembly_transform import (
            AssemblyTransform,
        )
        from codetocad.adapters.build123d.cad.assembly.assembly_export import (
            AssemblyExport,
        )
        from codetocad.adapters.build123d.cad.assembly.assembly_geometry import (
            AssemblyGeometry,
        )

        self.transform = AssemblyTransform(self)
        self.export = AssemblyExport(self)
        self.geometry = AssemblyGeometry(self)

        # Initialize mate manager and fluent mate interface
        from codetocad.adapters.build123d.cad.assembly.mate.mate_manager import (
            MateManager,
        )
        from codetocad.adapters.build123d.cad.assembly.assembly_mate import AssemblyMate

        self.mate_manager = MateManager(self)
        self.mate = AssemblyMate(self)

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
            # Remove any mates involving this part
            mates_to_remove = self.mate_manager.get_mates_by_part(part)
            for mate in mates_to_remove:
                self.mate_manager.remove_mate(mate.name)

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
            result = result.boolean.union(part)

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
        # Clear all mates first
        self.mate_manager.clear_all_mates()

        for part in self.parts[:]:  # Create a copy of the list to iterate over
            self.remove_part(part)

    # Mate management methods (delegate to mate_manager)
    def remove_mate(self, mate_name: str) -> bool:
        """Remove a mate by name."""
        return self.mate_manager.remove_mate(mate_name)

    def get_mate(self, mate_name: str):
        """Get a mate by name."""
        return self.mate_manager.get_mate(mate_name)

    def get_all_mates(self):
        """Get all mates in the assembly."""
        return self.mate_manager.get_all_mates()

    def solve_mates(self) -> bool:
        """Solve all active mate constraints."""
        return self.mate_manager.solve_mates()

    def validate_mates(self):
        """Validate all mates in the assembly."""
        return self.mate_manager.validate_mates()

    def get_mate_statistics(self):
        """Get statistics about mates in the assembly."""
        return self.mate_manager.get_mate_statistics()

    def __len__(self):
        """Get the number of parts in the assembly."""
        return len(self.parts)

    def __repr__(self):
        return f"<Assembly: {self.name}, {len(self.parts)} parts>"
