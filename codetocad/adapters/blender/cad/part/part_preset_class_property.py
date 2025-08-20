from codetocad.interfaces.cad.part.part_interface import (
    _PartPresetClassPropertyInterface,
)


class _PartPresetClassProperty(_PartPresetClassPropertyInterface):
    @property
    def preset(self):
        from codetocad.adapters.blender.cad.part.part_presets import PartPresets

        return PartPresets()
