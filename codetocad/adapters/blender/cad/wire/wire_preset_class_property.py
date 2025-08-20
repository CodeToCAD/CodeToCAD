from codetocad.interfaces.cad.wire.wire_interface import (
    _WirePresetClassPropertyInterface,
)
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface


class _WirePresetClassProperty(_WirePresetClassPropertyInterface):
    """Metaclass to provide a preset property for the Wire class."""

    @property
    def preset(self):
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.wire.wire import Wire

        return WirePresetsInterface(Wire, None)
