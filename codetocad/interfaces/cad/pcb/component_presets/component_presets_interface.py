"""
Component presets interface for PCB design.

This module defines the abstract interface for electronic component presets
with metaclass pattern for easy access similar to Part.preset pattern.
"""

from abc import ABC, ABCMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.pcb.pcb_component_interface import (
        PCBComponentInterface,
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


class _ComponentPresetClassPropertyInterface(ABCMeta):
    """Metaclass to provide a preset property for PCB components."""

    @property
    def preset(cls):
        """Access to component presets."""
        return ComponentPresetsInterface()


class ComponentPresetsInterface:
    """
    Interface for accessing electronic component presets.

    This class provides access to preset definitions for common electronic
    components including resistors, capacitors, LEDs, transistors, ICs, and connectors.
    """

    def __init__(self):
        pass

    @property
    def resistor(self) -> "ResistorPresets":
        """Access resistor presets."""
        from .resistor_presets import ResistorPresets

        return ResistorPresets()

    @property
    def capacitor(self) -> "CapacitorPresets":
        """Access capacitor presets."""
        from .capacitor_presets import CapacitorPresets

        return CapacitorPresets()

    @property
    def led(self) -> "LEDPresets":
        """Access LED presets."""
        from .led_presets import LEDPresets

        return LEDPresets()

    @property
    def transistor(self) -> "TransistorPresets":
        """Access transistor presets."""
        from .transistor_presets import TransistorPresets

        return TransistorPresets()

    @property
    def ic(self) -> "ICPresets":
        """Access IC presets."""
        from .ic_presets import ICPresets

        return ICPresets()

    @property
    def connector(self) -> "ConnectorPresets":
        """Access connector presets."""
        from .connector_presets import ConnectorPresets

        return ConnectorPresets()

    def create_custom_component(
        self,
        reference_designator: str,
        footprint_name: str,
        value: str = "",
        description: str = "",
    ) -> "PCBComponentInterface":
        """
        Create a custom component with basic properties.

        Args:
            reference_designator: Component reference (e.g., "U1", "R5")
            footprint_name: Name of the footprint to use
            value: Component value
            description: Component description

        Returns:
            PCBComponentInterface: The created component
        """
        # This would be implemented by concrete adapters
        raise NotImplementedError(
            "create_custom_component must be implemented by concrete adapter"
        )
