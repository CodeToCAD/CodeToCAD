"""
PCB Net interface for CodeToCAD.

This module defines the abstract interface for PCB net operations including
net management, connectivity, and electrical rules.
"""

from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
from dataclasses import dataclass


class NetClass(Enum):
    """Enumeration of net classes."""

    DEFAULT = "default"
    POWER = "power"
    GROUND = "ground"
    SIGNAL = "signal"
    CLOCK = "clock"
    DIFFERENTIAL = "differential"
    HIGH_SPEED = "high_speed"
    ANALOG = "analog"
    DIGITAL = "digital"


@dataclass
class NetConstraints:
    """Electrical constraints for a net."""

    min_trace_width: float = 0.1  # mm
    max_trace_width: float = 10.0  # mm
    min_via_size: float = 0.2  # mm
    max_via_size: float = 2.0  # mm
    min_clearance: float = 0.1  # mm
    max_length: float = 1000.0  # mm
    impedance_target: float | None = None  # ohms
    impedance_tolerance: float = 10.0  # %
    max_stub_length: float = 0.0  # mm (0 = no stubs allowed)
    differential_pair_spacing: float | None = None  # mm
    custom_constraints: dict[str, Any] = None

    def __post_init__(self):
        if self.custom_constraints is None:
            self.custom_constraints = {}


@dataclass
class NetConnection:
    """Represents a connection point on a net."""

    component_ref: str  # Component reference designator
    pin_number: str  # Pin number/name
    x: float  # X coordinate (mm)
    y: float  # Y coordinate (mm)
    layer: str  # Layer name


class PCBNetInterface(ABC):
    """
    Abstract interface for PCB net operations.

    This interface handles net management, connectivity tracking,
    and electrical rule checking for PCB designs.
    """

    def __init__(self, name: str):
        self.name: str = name
        self.net_class: NetClass = NetClass.DEFAULT
        self.constraints: NetConstraints = NetConstraints()
        self.connections: list[NetConnection] = []
        self.priority: int = 0  # Routing priority (higher = more important)
        self.locked: bool = False
        self.hidden: bool = False

    @abstractmethod
    def add_connection(
        self, component_ref: str, pin_number: str, x: float, y: float, layer: str
    ) -> "PCBNetInterface":
        """
        Add a connection point to the net.

        Args:
            component_ref: Component reference designator
            pin_number: Pin number/name
            x: X coordinate in mm
            y: Y coordinate in mm
            layer: Layer name

        Returns:
            PCBNetInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def remove_connection(
        self, component_ref: str, pin_number: str
    ) -> "PCBNetInterface":
        """
        Remove a connection from the net.

        Args:
            component_ref: Component reference designator
            pin_number: Pin number/name

        Returns:
            PCBNetInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_net_class(self, net_class: NetClass) -> "PCBNetInterface":
        """
        Set the net class.

        Args:
            net_class: Net class to assign

        Returns:
            PCBNetInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_constraints(self, constraints: NetConstraints) -> "PCBNetInterface":
        """
        Set electrical constraints for the net.

        Args:
            constraints: Net constraints

        Returns:
            PCBNetInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def set_priority(self, priority: int) -> "PCBNetInterface":
        """
        Set routing priority for the net.

        Args:
            priority: Priority level (higher = more important)

        Returns:
            PCBNetInterface: Self for method chaining
        """
        ...

    @abstractmethod
    def get_connection_count(self) -> int:
        """
        Get the number of connections on this net.

        Returns:
            int: Number of connections
        """
        ...

    @abstractmethod
    def get_total_length(self) -> float:
        """
        Calculate total routed length of the net.

        Returns:
            float: Total length in mm
        """
        ...

    @abstractmethod
    def is_fully_routed(self) -> bool:
        """
        Check if all connections are routed.

        Returns:
            bool: True if fully routed
        """
        ...

    @abstractmethod
    def get_unrouted_connections(self) -> list[tuple[NetConnection, NetConnection]]:
        """
        Get pairs of connections that need routing.

        Returns:
            list[tuple[NetConnection, NetConnection]]: Unrouted connection pairs
        """
        ...

    @abstractmethod
    def validate_constraints(self) -> list[str]:
        """
        Validate net against its constraints.

        Returns:
            list[str]: List of constraint violations (empty if valid)
        """
        ...

    @abstractmethod
    def clear_routing(self) -> "PCBNetInterface":
        """
        Clear all routing for this net (keep connections).

        Returns:
            PCBNetInterface: Self for method chaining
        """
        ...
