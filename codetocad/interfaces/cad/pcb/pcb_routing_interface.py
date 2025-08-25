"""
PCB Routing interface for CodeToCAD.

This module defines the abstract interface for PCB routing operations including
trace routing, via placement, and design rule checking.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from enum import Enum
from dataclasses import dataclass
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from .pcb_net_interface import PCBNetInterface
    from .pcb_board_interface import DrillSpecs


class TraceShape(Enum):
    """Enumeration of trace shapes."""

    STRAIGHT = "straight"
    ARC = "arc"
    CURVED = "curved"


class ViaType(Enum):
    """Enumeration of via types."""

    THROUGH = "through"  # Through-hole via
    BLIND = "blind"  # Blind via (outer to inner layer)
    BURIED = "buried"  # Buried via (inner to inner layer)
    MICRO = "micro"  # Micro via
    TENTED = "tented"  # Tented via (covered by soldermask)


@dataclass
class TraceSegment:
    """Definition of a trace segment."""

    start_x: float
    start_y: float
    end_x: float
    end_y: float
    width: float
    layer: str
    net_name: str
    shape: TraceShape = TraceShape.STRAIGHT
    arc_center_x: float | None = None  # For arc traces
    arc_center_y: float | None = None  # For arc traces


@dataclass
class ViaDefinition:
    """Definition of a via."""

    x: float
    y: float
    via_type: ViaType
    drill_diameter: float
    pad_diameter: float
    start_layer: str
    end_layer: str
    net_name: str
    tented_top: bool = False
    tented_bottom: bool = False


@dataclass
class RoutingConstraints:
    """Constraints for routing operations."""

    min_trace_width: float = 0.1  # mm
    max_trace_width: float = 10.0  # mm
    min_via_size: float = 0.2  # mm
    min_spacing: float = 0.1  # mm
    min_annular_ring: float = 0.05  # mm
    max_via_aspect_ratio: float = 10.0  # drill_diameter / board_thickness
    preferred_directions: dict[str, float] = None  # layer -> angle in degrees
    avoid_areas: list[tuple[float, float, float, float]] = None  # (x1,y1,x2,y2)

    def __post_init__(self):
        if self.preferred_directions is None:
            self.preferred_directions = {}
        if self.avoid_areas is None:
            self.avoid_areas = []


class PCBRoutingInterface(ABC):
    """
    Abstract interface for PCB routing operations.

    This interface handles trace routing, via placement, design rule checking,
    and routing optimization for PCB designs.
    """

    def __init__(self):
        self.traces: list[TraceSegment] = []
        self.vias: list[ViaDefinition] = []
        self.routing_constraints: RoutingConstraints = RoutingConstraints()

    @abstractmethod
    def add_trace(
        self,
        start_x: LengthType,
        start_y: LengthType,
        end_x: LengthType,
        end_y: LengthType,
        width: LengthType,
        layer: str,
        net_name: str,
    ) -> "PCBRoutingInterface":
        """
        Add a straight trace segment.

        Args:
            start_x: Start X coordinate
            start_y: Start Y coordinate
            end_x: End X coordinate
            end_y: End Y coordinate
            width: Trace width
            layer: Layer name
            net_name: Net name

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def add_arc_trace(
        self,
        start_x: LengthType,
        start_y: LengthType,
        end_x: LengthType,
        end_y: LengthType,
        center_x: LengthType,
        center_y: LengthType,
        width: LengthType,
        layer: str,
        net_name: str,
    ) -> "PCBRoutingInterface":
        """
        Add an arc trace segment.

        Args:
            start_x: Start X coordinate
            start_y: Start Y coordinate
            end_x: End X coordinate
            end_y: End Y coordinate
            center_x: Arc center X coordinate
            center_y: Arc center Y coordinate
            width: Trace width
            layer: Layer name
            net_name: Net name

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def add_via(
        self,
        x: LengthType,
        y: LengthType,
        via_type: ViaType,
        drill_diameter: LengthType,
        pad_diameter: LengthType,
        start_layer: str,
        end_layer: str,
        net_name: str,
    ) -> "PCBRoutingInterface":
        """
        Add a via.

        Args:
            x: X coordinate
            y: Y coordinate
            via_type: Type of via
            drill_diameter: Drill diameter
            pad_diameter: Pad diameter
            start_layer: Starting layer
            end_layer: Ending layer
            net_name: Net name

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def route_net(
        self, net: "PCBNetInterface", algorithm: str = "auto"
    ) -> "PCBRoutingInterface":
        """
        Automatically route a net.

        Args:
            net: Net to route
            algorithm: Routing algorithm ("auto", "shortest", "avoid_vias")

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def route_differential_pair(
        self,
        net_positive: "PCBNetInterface",
        net_negative: "PCBNetInterface",
        spacing: LengthType,
        trace_width: LengthType,
    ) -> "PCBRoutingInterface":
        """
        Route a differential pair.

        Args:
            net_positive: Positive net
            net_negative: Negative net
            spacing: Spacing between traces
            trace_width: Width of each trace

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_routing_constraints(
        self, constraints: RoutingConstraints
    ) -> "PCBRoutingInterface":
        """
        Set routing constraints.

        Args:
            constraints: Routing constraints

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def optimize_routing(
        self, net_names: list[str] | None = None
    ) -> "PCBRoutingInterface":
        """
        Optimize routing for specified nets or all nets.

        Args:
            net_names: List of net names to optimize (None for all)

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def check_design_rules(self) -> list[str]:
        """
        Check routing against design rules.

        Returns:
            list[str]: List of design rule violations (empty if valid)
        """
        ...

    @abstractmethod
    def get_trace_length(self, net_name: str) -> float:
        """
        Calculate total trace length for a net.

        Args:
            net_name: Net name

        Returns:
            float: Total trace length in mm
        """
        ...

    @abstractmethod
    def remove_routing(self, net_name: str) -> "PCBRoutingInterface":
        """
        Remove all routing for a specific net.

        Args:
            net_name: Net name

        Returns:
            PCBRoutingInterface: Self for method chaining
        """
        ...
