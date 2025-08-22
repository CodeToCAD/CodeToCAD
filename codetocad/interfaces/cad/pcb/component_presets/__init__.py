"""
Electronic component presets for PCB design.

This module provides preset definitions for common electronic components
including footprints, electrical properties, and pin configurations.
"""

from codetocad.interfaces.cad.pcb.component_presets.component_presets_interface import (
    ComponentPresetsInterface,
)
from codetocad.interfaces.cad.pcb.component_presets.resistor_presets import (
    ResistorPresets,
)
from codetocad.interfaces.cad.pcb.component_presets.capacitor_presets import (
    CapacitorPresets,
)
from codetocad.interfaces.cad.pcb.component_presets.led_presets import LEDPresets
from codetocad.interfaces.cad.pcb.component_presets.transistor_presets import (
    TransistorPresets,
)
from codetocad.interfaces.cad.pcb.component_presets.ic_presets import ICPresets
from codetocad.interfaces.cad.pcb.component_presets.connector_presets import (
    ConnectorPresets,
)
