from typing import TYPE_CHECKING
from abc import ABC, abstractmethod, ABCMeta
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface
from codetocad.interfaces.cad.part.part_transform_interface import (
    PartTransformInterface,
)
from codetocad.interfaces.cad.part.part_export_interface import PartExportInterface
from codetocad.interfaces.cad.part.part_boolean_interface import PartBooleanInterface
from codetocad.interfaces.cad.part.part_geometry_interface import PartGeometryInterface
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

        # Method group properties
        self.transform = PartTransformInterface(self)
        self.export = PartExportInterface(self)
        self.boolean = PartBooleanInterface(self)
        self.geometry = PartGeometryInterface(self)

    def set_name(self, name: str):
        """Set the part name."""
        self.name = name

    @classmethod
    @abstractmethod
    def get_by_name(cls, name: str) -> "PartInterface| None":
        """Get a part by name."""
        ...

    def extrude_sketch(self, _distance: LengthType) -> "PartInterface":
        """Extrude the part's sketch to create a solid."""
        return self

    def copy(self) -> "PartInterface":
        """Create a copy of the part."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific part type
        raise NotImplementedError("copy must be implemented by concrete classes")

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
