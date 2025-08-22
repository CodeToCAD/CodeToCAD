"""
PCB Board interface for CodeToCAD.

This module defines the abstract interface for PCB board operations including
board creation, layer management, stackup configuration, and dimension handling.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.pcb.pcb_layer_interface import PCBLayerInterface
    from codetocad.interfaces.cad.pcb.pcb_component_interface import (
        PCBComponentInterface,
    )
    from codetocad.interfaces.cad.pcb.pcb_net_interface import PCBNetInterface


class BoardShape(Enum):
    """Enumeration of supported board shapes."""

    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    CUSTOM = "custom"


@dataclass
class BoardDimensions:
    """Board dimension specifications."""

    width: float  # mm
    height: float  # mm
    thickness: float = 1.6  # mm, standard PCB thickness
    shape: BoardShape = BoardShape.RECTANGLE
    corner_radius: float = 0.0  # mm, for rounded corners


@dataclass
class DrillSpecs:
    """Drill specifications for vias and holes."""

    drill_diameter: float  # mm
    finished_hole_diameter: float  # mm
    plated: bool = True


class PCBBoardInterface(ABC):
    """
    Abstract interface for PCB board operations.

    This interface handles board-level operations including creation,
    layer management, stackup configuration, and overall board properties.
    """

    def __init__(self):
        self.name: str = "untitled_board"
        self.dimensions: BoardDimensions = BoardDimensions(100.0, 80.0)
        self.layers: list["PCBLayerInterface"] = []
        self.components: list["PCBComponentInterface"] = []
        self.nets: list["PCBNetInterface"] = []
        self.design_rules: dict[str, float] = {}

    @abstractmethod
    def create_board(
        self, name: str, dimensions: BoardDimensions, layer_count: int = 2
    ) -> "PCBBoardInterface":
        """
        Create a new PCB board.

        Args:
            name: Board name
            dimensions: Board dimensions and shape
            layer_count: Number of copper layers (2, 4, 6, 8, etc.)

        Returns:
            PCBBoardInterface: The created board
        """
        ...

    @abstractmethod
    def set_board_outline(
        self, outline_points: list[tuple[float, float]]
    ) -> "PCBBoardInterface":
        """
        Set custom board outline from points.

        Args:
            outline_points: List of (x, y) coordinates defining the board edge

        Returns:
            PCBBoardInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def add_layer(self, layer: "PCBLayerInterface") -> "PCBBoardInterface":
        """
        Add a layer to the board stackup.

        Args:
            layer: Layer to add

        Returns:
            PCBBoardInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def remove_layer(self, layer_name: str) -> "PCBBoardInterface":
        """
        Remove a layer from the board stackup.

        Args:
            layer_name: Name of layer to remove

        Returns:
            PCBBoardInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def get_layer(self, layer_name: str) -> "PCBLayerInterface | None":
        """
        Get a layer by name.

        Args:
            layer_name: Name of layer to retrieve

        Returns:
            PCBLayerInterface or None: The layer if found
        """
        ...

    @abstractmethod
    def set_design_rules(self, rules: dict[str, float]) -> "PCBBoardInterface":
        """
        Set design rules for the board.

        Args:
            rules: Dictionary of rule names to values (in mm)
                  Common rules: 'min_trace_width', 'min_via_size',
                  'min_drill_size', 'min_spacing'

        Returns:
            PCBBoardInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def add_mounting_hole(
        self, x: LengthType, y: LengthType, drill_specs: DrillSpecs
    ) -> "PCBBoardInterface":
        """
        Add a mounting hole to the board.

        Args:
            x: X coordinate
            y: Y coordinate
            drill_specs: Drill specifications

        Returns:
            PCBBoardInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def get_board_area(self) -> float:
        """
        Calculate the board area.

        Returns:
            float: Board area in mm²
        """
        ...

    @abstractmethod
    def validate_design_rules(self) -> list[str]:
        """
        Validate the board against design rules.

        Returns:
            list[str]: List of design rule violations (empty if valid)
        """
        ...
