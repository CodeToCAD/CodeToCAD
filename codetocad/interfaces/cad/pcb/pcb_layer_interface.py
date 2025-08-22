"""
PCB Layer interface for CodeToCAD.

This module defines the abstract interface for PCB layer operations including
layer types, stackup management, and layer-specific properties.
"""

from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum
from dataclasses import dataclass


class LayerType(Enum):
    """Enumeration of PCB layer types."""

    SIGNAL = "signal"  # Copper signal layer
    POWER = "power"  # Power plane
    GROUND = "ground"  # Ground plane
    MIXED = "mixed"  # Mixed signal/power layer
    MECHANICAL = "mechanical"  # Mechanical/outline layer
    SOLDERMASK = "soldermask"  # Solder mask layer
    SILKSCREEN = "silkscreen"  # Silkscreen layer
    PASTE = "paste"  # Solder paste layer
    DRILL = "drill"  # Drill layer
    KEEPOUT = "keepout"  # Keepout area layer


class LayerSide(Enum):
    """Enumeration of layer sides."""

    TOP = "top"
    BOTTOM = "bottom"
    INNER = "inner"


@dataclass
class LayerProperties:
    """Properties for a PCB layer."""

    name: str
    layer_type: LayerType
    side: LayerSide
    thickness: float = 0.035  # mm, standard copper thickness
    color: tuple[int, int, int] = (255, 0, 0)  # RGB color
    visible: bool = True
    locked: bool = False
    copper_pour: bool = False  # Whether layer has copper pour
    pour_clearance: float = 0.2  # mm, clearance around copper pour


class PCBLayerInterface(ABC):
    """
    Abstract interface for PCB layer operations.

    This interface handles individual layer properties, stackup management,
    and layer-specific operations like copper pours and keepout areas.
    """

    def __init__(self, properties: LayerProperties):
        self.properties = properties
        self.objects: list = []  # Layer-specific objects (traces, pads, etc.)

    @abstractmethod
    def set_layer_properties(self, properties: LayerProperties) -> "PCBLayerInterface":
        """
        Set layer properties.

        Args:
            properties: Layer properties to set

        Returns:
            PCBLayerInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def add_copper_pour(
        self,
        net_name: str,
        outline_points: list[tuple[float, float]],
        clearance: float = 0.2,
    ) -> "PCBLayerInterface":
        """
        Add a copper pour to the layer.

        Args:
            net_name: Name of net to connect pour to
            outline_points: Points defining pour boundary
            clearance: Clearance around objects in mm

        Returns:
            PCBLayerInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def add_keepout_area(
        self,
        outline_points: list[tuple[float, float]],
        keepout_type: str = "all",  # "all", "via", "track", "pad"
    ) -> "PCBLayerInterface":
        """
        Add a keepout area to the layer.

        Args:
            outline_points: Points defining keepout boundary
            keepout_type: Type of objects to keep out

        Returns:
            PCBLayerInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_visibility(self, visible: bool) -> "PCBLayerInterface":
        """
        Set layer visibility.

        Args:
            visible: Whether layer should be visible

        Returns:
            PCBLayerInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_color(self, color: tuple[int, int, int]) -> "PCBLayerInterface":
        """
        Set layer display color.

        Args:
            color: RGB color tuple (0-255 each)

        Returns:
            PCBLayerInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def get_layer_thickness(self) -> float:
        """
        Get the layer thickness.

        Returns:
            float: Layer thickness in mm
        """
        ...

    @abstractmethod
    def is_copper_layer(self) -> bool:
        """
        Check if this is a copper layer.

        Returns:
            bool: True if copper layer
        """
        ...

    @abstractmethod
    def get_objects_in_area(self, x1: float, y1: float, x2: float, y2: float) -> list:
        """
        Get all objects in a rectangular area.

        Args:
            x1, y1: Bottom-left corner coordinates
            x2, y2: Top-right corner coordinates

        Returns:
            list: Objects in the specified area
        """
        ...

    @abstractmethod
    def clear_layer(self) -> "PCBLayerInterface":
        """
        Clear all objects from the layer.

        Returns:
            PCBLayerInterface: Self for method chaining
        """
        ...
