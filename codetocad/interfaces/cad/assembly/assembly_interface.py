from abc import ABC
from typing import TYPE_CHECKING
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
from codetocad.interfaces.cad.assembly.mate.mate_manager_interface import (
    MateManagerInterface,
)
from codetocad.interfaces.cad.assembly.assembly_mate_interface import (
    AssemblyMateInterface,
)

if TYPE_CHECKING:
    from codetocad.interfaces.cad.camera_interface import CameraInterface
    from codetocad.interfaces.cad.light_interface import LightInterface


class AssemblyInterface(ABC):
    def __init__(self):
        self.parts: list[PartInterface] = []
        self.name: str | None = None

        # Scene objects
        self.cameras: list["CameraInterface"] = []
        self.lights: list["LightInterface"] = []

        self.add = AssemblyAddInterface(self)
        self.get = AssemblyGetInterface(self)

        # Method group properties
        self.transform = AssemblyTransformInterface(self)
        self.export = AssemblyExportInterface(self)
        self.geometry = AssemblyGeometryInterface(self)
        self.mate = None  # To be overridden by concrete implementations

        # Mate manager (to be overridden by concrete implementations)
        self.mate_manager: MateManagerInterface = None

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

    def add_camera(self, camera: "CameraInterface"):
        """Add a camera to the assembly."""
        if camera not in self.cameras:
            self.cameras.append(camera)

    def remove_camera(self, camera: "CameraInterface"):
        """Remove a camera from the assembly."""
        if camera in self.cameras:
            self.cameras.remove(camera)

    def add_light(self, light: "LightInterface"):
        """Add a light to the assembly."""
        if light not in self.lights:
            self.lights.append(light)

    def remove_light(self, light: "LightInterface"):
        """Remove a light from the assembly."""
        if light in self.lights:
            self.lights.remove(light)

    def get_cameras(self) -> list["CameraInterface"]:
        """Get all cameras in the assembly."""
        return self.cameras.copy()

    def get_lights(self) -> list["LightInterface"]:
        """Get all lights in the assembly."""
        return self.lights.copy()

    def get_camera_by_name(self, name: str) -> "CameraInterface | None":
        """Get a camera by name."""
        for camera in self.cameras:
            if camera.name == name:
                return camera
        return None

    def get_light_by_name(self, name: str) -> "LightInterface | None":
        """Get a light by name."""
        for light in self.lights:
            if light.name == name:
                return light
        return None

    def get_part_by_name(self, name: str) -> "PartInterface | None":
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
        # Clear all mates first (if mate manager is available)
        if hasattr(self, "mate_manager") and self.mate_manager:
            self.mate_manager.clear_all_mates()

        for part in self.parts[:]:  # Create a copy of the list to iterate over
            self.remove_part(part)

    # Mate management methods (delegate to mate_manager)
    def remove_mate(self, mate_name: str) -> bool:
        """Remove a mate by name."""
        if hasattr(self, "mate_manager") and self.mate_manager:
            return self.mate_manager.remove_mate(mate_name)
        return False

    def get_mate(self, mate_name: str):
        """Get a mate by name."""
        if hasattr(self, "mate_manager") and self.mate_manager:
            return self.mate_manager.get_mate(mate_name)
        return None

    def get_all_mates(self):
        """Get all mates in the assembly."""
        if hasattr(self, "mate_manager") and self.mate_manager:
            return self.mate_manager.get_all_mates()
        return []

    def solve_mates(self) -> bool:
        """Solve all active mate constraints."""
        if hasattr(self, "mate_manager") and self.mate_manager:
            return self.mate_manager.solve_mates()
        return True  # No mates to solve

    def validate_mates(self):
        """Validate all mates in the assembly."""
        if hasattr(self, "mate_manager") and self.mate_manager:
            return self.mate_manager.validate_mates()
        return {}

    def get_mate_statistics(self):
        """Get statistics about mates in the assembly."""
        if hasattr(self, "mate_manager") and self.mate_manager:
            return self.mate_manager.get_mate_statistics()
        return {"total": 0}

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
