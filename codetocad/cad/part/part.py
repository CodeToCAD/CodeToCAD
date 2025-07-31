from typing import TYPE_CHECKING
from codetocad.cad.part.part_presets import PartPresets

if TYPE_CHECKING:
    from codetocad.cad.assembly.assembly import Assembly


class _PartPresetClassProperty(type):
    @property
    def preset(self):
        return PartPresets()


class Part(metaclass=_PartPresetClassProperty):
    def __init__(self):
        self.member_assemblies: list[Assembly] = []

        from codetocad.cad.sketch.sketch import Sketch

        self.sketch: Sketch = Sketch()

        self.name = None

    def set_name(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, name): ...

    def __repr__(self):
        return f"<Part: {self.name or 'Unnamed'}. {self.sketch}>"
