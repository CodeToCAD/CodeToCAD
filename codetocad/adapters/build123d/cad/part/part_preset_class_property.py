"""
Metaclass for build123d Part preset class property.
"""

from codetocad.interfaces.cad.part.part_interface import (
    _PartPresetClassPropertyInterface,
)


class _PartPresetClassProperty(_PartPresetClassPropertyInterface):
    @property
    def preset(self):
        from codetocad.adapters.build123d.cad.part.part_presets import PartPresets

        return PartPresets()
