from typing import TYPE_CHECKING
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class _PartPresetClassPropertyInterface(type):
    @property
    def preset(self):
        return PartPresetsInterface()


class PartInterface(metaclass=_PartPresetClassPropertyInterface):
    def __init__(self):
        self.member_assemblies: list[AssemblyInterface] = []

        from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface

        self.sketch: SketchInterface = SketchInterface()

        self.name = None

    def set_name(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, name): ...

    def __repr__(self):
        return f"<Part: {self.name or 'Unnamed'}. {self.sketch}>"
