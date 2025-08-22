"""
KiCad PCB Component implementation for CodeToCAD.

This module provides KiCad-specific implementation of PCB component operations.
"""

from typing import TYPE_CHECKING
from codetocad.interfaces.cad.pcb.pcb_component_interface import (
    PCBComponentInterface,
    FootprintDefinition,
    ElectricalProperties,
)
from codetocad.interfaces.cad.pcb.component_presets.component_presets_interface import (
    _ComponentPresetClassPropertyInterface,
)
from codetocad.core.dimensions.length_expression import LengthType

# Board operations are now handled directly through kipy

from kipy import KiCad


class PCBComponent(
    PCBComponentInterface, metaclass=_ComponentPresetClassPropertyInterface
):
    """
    KiCad-specific implementation of PCB component operations.

    This class provides KiCad-specific implementations for component placement,
    footprint management, and electrical properties using KiCad's pcbnew API.
    """

    def __init__(self):
        super().__init__()
        self._kicad_footprint = None
        self._board = None

    @property
    def kicad_footprint(self):
        """Get the underlying KiCad footprint object."""
        if self._kicad_footprint is None:
            raise RuntimeError("Component footprint not created")
        return self._kicad_footprint

    def set_footprint(self, footprint: FootprintDefinition) -> "PCBComponentInterface":
        """Set the component footprint."""

        try:
            from ..kicad_actions.component_operations import create_footprint

            # Convert footprint definition to KiCad format
            pins = []
            for pin in footprint.pins:
                pin_data = {
                    "number": pin.number,
                    "name": pin.name,
                    "x": pin.x,
                    "y": pin.y,
                    "drill_diameter": pin.drill_diameter,
                    "pad_width": pin.pad_width,
                    "pad_height": pin.pad_height,
                    "shape": pin.shape,
                }
                pins.append(pin_data)

            # Create KiCad footprint
            self._kicad_footprint = create_footprint(
                "CodeToCAD", footprint.name, pins  # Library name
            )

            self.footprint = footprint
            return self

        except Exception as e:
            raise RuntimeError(f"Failed to set footprint: {str(e)}")

    def set_position(
        self, x: LengthType, y: LengthType, rotation: float = 0.0
    ) -> "PCBComponentInterface":
        """Set component position and rotation."""

        try:
            if self._kicad_footprint is None:
                raise RuntimeError("Component footprint not created")

            from ..kicad_actions.component_operations import move_component

            move_component(self._kicad_footprint, float(x), float(y), rotation)

            self.position = (float(x), float(y))
            self.rotation = rotation

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to set position: {str(e)}")

    def set_layer(self, layer: str) -> "PCBComponentInterface":
        """Set which layer the component is on."""
        self.layer = layer

        if self._kicad_footprint is not None:
            # Flip component if moving to bottom layer
            if layer.lower() == "bottom" and not self._kicad_footprint.IsFlipped():
                self._kicad_footprint.Flip(self._kicad_footprint.GetPosition(), False)
            elif layer.lower() == "top" and self._kicad_footprint.IsFlipped():
                self._kicad_footprint.Flip(self._kicad_footprint.GetPosition(), False)

        return self

    def connect_pin_to_net(
        self, pin_number: str, net_name: str
    ) -> "PCBComponentInterface":
        """Connect a component pin to a net."""

        try:
            if self._kicad_footprint is None or self._board is None:
                raise RuntimeError("Component not properly initialized")

            from ..kicad_actions.component_operations import connect_component_to_net

            connect_component_to_net(
                self._board.kicad_board, self._kicad_footprint, pin_number, net_name
            )

            self.nets[pin_number] = net_name
            return self

        except Exception as e:
            raise RuntimeError(f"Failed to connect pin to net: {str(e)}")

    def set_electrical_properties(
        self, properties: ElectricalProperties
    ) -> "PCBComponentInterface":
        """Set electrical properties of the component."""
        self.electrical_properties = properties

        if self._kicad_footprint is not None:
            from ..kicad_actions.component_operations import set_component_properties

            # Convert properties to KiCad format
            kicad_properties = {
                "description": properties.custom_properties.get("description", ""),
                "keywords": f"{properties.package} {properties.value}",
            }

            set_component_properties(
                self._kicad_footprint,
                self.reference_designator,
                properties.value,
                kicad_properties,
            )

        return self

    def get_pin_position(self, pin_number: str) -> tuple[float, float] | None:
        """Get the absolute position of a pin."""
        if self._kicad_footprint is None:
            return None

        try:
            from ..kicad_actions.component_operations import get_component_info

            info = get_component_info(self._kicad_footprint)
            for pin in info["pins"]:
                if pin["number"] == pin_number:
                    return (pin["position"]["x"], pin["position"]["y"])

            return None

        except Exception:
            return None

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """Get component bounding box."""
        if self._kicad_footprint is None:
            return (0, 0, 0, 0)

        try:
            bbox = self._kicad_footprint.GetBoundingBox()
            return (
                bbox.GetX() / 1000000.0,  # Convert to mm
                bbox.GetY() / 1000000.0,
                bbox.GetRight() / 1000000.0,
                bbox.GetBottom() / 1000000.0,
            )

        except Exception:
            return (0, 0, 0, 0)

    def flip_to_bottom(self) -> "PCBComponentInterface":
        """Flip component to bottom layer."""
        return self.set_layer("bottom")

    def validate_footprint(self) -> list[str]:
        """Validate the component footprint."""
        errors = []

        if self.footprint is None:
            errors.append("No footprint defined")
            return errors

        if not self.footprint.pins:
            errors.append("Footprint has no pins")

        if self.footprint.body_width <= 0 or self.footprint.body_height <= 0:
            errors.append("Invalid body dimensions")

        return errors

    def set_board(self, board: "PCBBoard") -> None:
        """Set the parent board (internal method)."""
        self._board = board
