"""
PCB Component interface for CodeToCAD.

This module defines the abstract interface for PCB component operations including
component placement, footprint management, and electrical properties.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from enum import Enum
from dataclasses import dataclass
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.pcb.pcb_board_interface import PCBBoardInterface


class ComponentType(Enum):
    """Enumeration of electronic component types."""

    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    INDUCTOR = "inductor"
    DIODE = "diode"
    LED = "led"
    TRANSISTOR = "transistor"
    IC = "ic"
    CONNECTOR = "connector"
    CRYSTAL = "crystal"
    SWITCH = "switch"
    RELAY = "relay"
    TRANSFORMER = "transformer"
    FUSE = "fuse"
    JUMPER = "jumper"
    TEST_POINT = "test_point"
    MECHANICAL = "mechanical"
    CUSTOM = "custom"


class MountType(Enum):
    """Component mounting types."""

    SMD = "smd"  # Surface Mount Device
    THT = "tht"  # Through Hole Technology
    MIXED = "mixed"  # Both SMD and THT pins


@dataclass
class PinDefinition:
    """Definition of a component pin."""

    number: str  # Pin number/name
    name: str  # Pin function name
    x: float  # X position relative to component center (mm)
    y: float  # Y position relative to component center (mm)
    drill_diameter: float = 0.0  # 0 for SMD, >0 for THT (mm)
    pad_width: float = 1.0  # Pad width (mm)
    pad_height: float = 1.0  # Pad height (mm)
    shape: str = "circle"  # "circle", "rectangle", "oval"


@dataclass
class FootprintDefinition:
    """Definition of a component footprint."""

    name: str
    description: str
    mount_type: MountType
    pins: list[PinDefinition]
    body_width: float  # Component body width (mm)
    body_height: float  # Component body height (mm)
    body_thickness: float = 1.0  # Component height (mm)
    courtyard_margin: float = 0.25  # Courtyard margin (mm)
    silkscreen_width: float = 0.12  # Silkscreen line width (mm)


@dataclass
class ElectricalProperties:
    """Electrical properties of a component."""

    value: str = ""  # Component value (e.g., "10k", "100nF")
    tolerance: str = ""  # Tolerance (e.g., "5%", "1%")
    voltage_rating: str = ""  # Voltage rating (e.g., "25V")
    power_rating: str = ""  # Power rating (e.g., "0.25W")
    temperature_coefficient: str = ""  # Temp coefficient
    package: str = ""  # Package type (e.g., "0603", "SOT-23")
    manufacturer: str = ""  # Manufacturer name
    part_number: str = ""  # Manufacturer part number
    datasheet_url: str = ""  # Link to datasheet
    custom_properties: dict[str, Any] | None = None

    def __post_init__(self):
        if self.custom_properties is None:
            self.custom_properties = {}


class PCBComponentInterface(ABC):
    """
    Abstract interface for PCB component operations.

    This interface handles component placement, footprint management,
    electrical properties, and component-specific operations.
    """

    def __init__(self):
        self.reference_designator: str = ""  # e.g., "R1", "C5", "U3"
        self.component_type: ComponentType = ComponentType.CUSTOM
        self.footprint: FootprintDefinition | None = None
        self.electrical_properties: ElectricalProperties = ElectricalProperties()
        self.position: tuple[float, float] = (0.0, 0.0)  # X, Y position (mm)
        self.rotation: float = 0.0  # Rotation in degrees
        self.layer: str = "top"  # "top" or "bottom"
        self.locked: bool = False
        self.nets: dict[str, str] = {}  # Pin number -> net name mapping

    @abstractmethod
    def set_footprint(self, footprint: FootprintDefinition) -> "PCBComponentInterface":
        """
        Set the component footprint.

        Args:
            footprint: Footprint definition

        Returns:
            PCBComponentInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_position(
        self, x: LengthType, y: LengthType, rotation: float = 0.0
    ) -> "PCBComponentInterface":
        """
        Set component position and rotation.

        Args:
            x: X coordinate
            y: Y coordinate
            rotation: Rotation in degrees (0-360)

        Returns:
            PCBComponentInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_layer(self, layer: str) -> "PCBComponentInterface":
        """
        Set which layer the component is on.

        Args:
            layer: "top" or "bottom"

        Returns:
            PCBComponentInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def connect_pin_to_net(
        self, pin_number: str, net_name: str
    ) -> "PCBComponentInterface":
        """
        Connect a component pin to a net.

        Args:
            pin_number: Pin number/name to connect
            net_name: Name of net to connect to

        Returns:
            PCBComponentInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_electrical_properties(
        self, properties: ElectricalProperties
    ) -> "PCBComponentInterface":
        """
        Set electrical properties of the component.

        Args:
            properties: Electrical properties

        Returns:
            PCBComponentInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def get_pin_position(self, pin_number: str) -> tuple[float, float] | None:
        """
        Get the absolute position of a pin.

        Args:
            pin_number: Pin number/name

        Returns:
            tuple[float, float] or None: (x, y) position in mm, or None if pin not found
        """
        ...

    @abstractmethod
    def get_bounding_box(self) -> tuple[float, float, float, float]:
        """
        Get component bounding box.

        Returns:
            tuple[float, float, float, float]: (x_min, y_min, x_max, y_max) in mm
        """
        ...

    @abstractmethod
    def flip_to_bottom(self) -> "PCBComponentInterface":
        """
        Flip component to bottom layer.

        Returns:
            PCBComponentInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def validate_footprint(self) -> list[str]:
        """
        Validate the component footprint.

        Returns:
            list[str]: List of validation errors (empty if valid)
        """
        ...
