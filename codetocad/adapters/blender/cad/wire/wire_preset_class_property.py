from codetocad.interfaces.cad.wire.wire_interface import (
    _WirePresetClassPropertyInterface,
)


class _WirePresetClassProperty(_WirePresetClassPropertyInterface):
    """Metaclass to provide a preset property for the Wire class."""

    @property
    def preset(self):
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.wire.wire import Wire
        from codetocad.adapters.blender.cad.wire.wire_presets import BlenderWirePresets

        return BlenderWirePresets(Wire, None)
