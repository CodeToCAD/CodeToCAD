from typing import TYPE_CHECKING
from abc import ABC, abstractmethod, ABCMeta
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class _PartPresetClassPropertyInterface(ABCMeta):
    @property
    def preset(self):
        return PartPresetsInterface()


class PartInterface(ABC, metaclass=_PartPresetClassPropertyInterface):
    def __init__(self):
        self.member_assemblies: list[AssemblyInterface] = []

        from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface

        self.sketch: SketchInterface = SketchInterface()

        self.name: str | None = None

    def set_name(self, name: str):
        """Set the part name."""
        self.name = name

    @classmethod
    @abstractmethod
    def get_by_name(cls, name: str) -> "PartInterface| None":
        """Get a part by name."""
        ...

    def extrude_sketch(self, distance: LengthType) -> "PartInterface":
        """Extrude the part's sketch to create a solid."""
        return self

    def union(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean union with another part."""
        return self

    def difference(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean difference with another part."""
        return self

    def intersection(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean intersection with another part."""
        return self

    def translate(
        self, dx: LengthType, dy: LengthType, dz: LengthType = 0
    ) -> "PartInterface":
        """Translate the part."""
        return self

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "PartInterface":
        """Rotate the part around an axis."""
        return self

    def scale(
        self, scale_x: float, scale_y: float, scale_z: float = 1.0
    ) -> "PartInterface":
        """Scale the part."""
        return self

    def get_volume(self) -> float:
        """Get the volume of the part."""
        return 0.0

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        return ((0, 0, 0), (0, 0, 0))

    def export_step(self, _file_path: str):
        """Export the part to STEP format."""
        pass

    def export_stl(self, _file_path: str, _tolerance: float = 0.1):
        """Export the part to STL format."""
        pass

    def export_brep(self, _file_path: str):
        """Export the part to BREP format."""
        pass

    def copy(self) -> "PartInterface":
        """Create a copy of the part."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific part type
        raise NotImplementedError("copy must be implemented by concrete classes")

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        pass

    def hide(self):
        """Hide the part."""
        pass

    def show(self):
        """Show the part."""
        pass

    def delete(self):
        """Delete the part."""
        pass

    def __repr__(self):
        return f"<Part: {self.name or 'Unnamed'}. {self.sketch}>"
