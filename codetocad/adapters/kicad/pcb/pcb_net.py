"""
KiCad PCB Net implementation for CodeToCAD.

This module provides KiCad-specific implementation of PCB net operations.
"""

from typing import Optional, TYPE_CHECKING
from codetocad.interfaces.cad.pcb.pcb_net_interface import (
    PCBNetInterface,
    NetClass,
    NetConstraints,
    NetConnection,
)


from kipy import KiCad
from kipy.board_types import Net, Track, Via

if TYPE_CHECKING:
    from .pcb_board import PCBBoard


class PCBNet(PCBNetInterface):
    """
    KiCad-specific implementation of PCB net operations.

    This class provides KiCad-specific implementations for net management,
    connectivity tracking, and electrical rule checking using KiCad's pcbnew API.
    """

    def __init__(self, name: str, board: Optional["PCBBoard"] = None):
        super().__init__(name)
        self._board = board
        self._kicad_net: Optional["pcbnew.NETINFO_ITEM"] = None

    @property
    def kicad_net(self) -> "pcbnew.NETINFO_ITEM":
        """Get the underlying KiCad net object."""
        if self._kicad_net is None:
            raise RuntimeError("Net not created in KiCad board")
        return self._kicad_net

    def add_connection(
        self, component_ref: str, pin_number: str, x: float, y: float, layer: str
    ) -> "PCBNetInterface":
        """Add a connection point to the net."""
        connection = NetConnection(
            component_ref=component_ref, pin_number=pin_number, x=x, y=y, layer=layer
        )

        self.connections.append(connection)

        # If we have a KiCad board, update the actual net connection
        if self._board is not None:
            try:
                self._update_kicad_connection(connection)
            except Exception as e:
                # Remove the connection if KiCad update failed
                self.connections.remove(connection)
                raise RuntimeError(f"Failed to add connection to KiCad: {str(e)}")

        return self

    def remove_connection(
        self, component_ref: str, pin_number: str
    ) -> "PCBNetInterface":
        """Remove a connection from the net."""
        # Find and remove the connection
        self.connections = [
            conn
            for conn in self.connections
            if not (
                conn.component_ref == component_ref and conn.pin_number == pin_number
            )
        ]

        # Update KiCad if available
        if self._board is not None:
            try:
                self._remove_kicad_connection(component_ref, pin_number)
            except Exception as e:
                raise RuntimeError(f"Failed to remove connection from KiCad: {str(e)}")

        return self

    def set_net_class(self, net_class: NetClass) -> "PCBNetInterface":
        """Set the net class."""
        self.net_class = net_class

        # Update KiCad net class if available
        if self._kicad_net is not None:
            try:
                # KiCad net class management would go here
                # This is a simplified implementation
                pass
            except Exception as e:
                raise RuntimeError(f"Failed to set net class in KiCad: {str(e)}")

        return self

    def set_constraints(self, constraints: NetConstraints) -> "PCBNetInterface":
        """Set electrical constraints for the net."""
        self.constraints = constraints
        return self

    def set_priority(self, priority: int) -> "PCBNetInterface":
        """Set routing priority for the net."""
        self.priority = priority
        return self

    def get_connection_count(self) -> int:
        """Get the number of connections on this net."""
        return len(self.connections)

    def get_total_length(self) -> float:
        """Calculate total routed length of the net."""

        try:
            if self._board is None or self._kicad_net is None:
                return 0.0

            from ..kicad_actions.routing_operations import get_net_info

            net_info = get_net_info(self._board.kicad_board, self.name)
            return net_info.get("total_length_mm", 0.0)

        except Exception:
            return 0.0

    def is_fully_routed(self) -> bool:
        """Check if all connections are routed."""

        try:
            if self._board is None or self._kicad_net is None:
                return False

            from ..kicad_actions.routing_operations import get_net_info

            net_info = get_net_info(self._board.kicad_board, self.name)
            return net_info.get("is_routed", False)

        except Exception:
            return False

    def get_unrouted_connections(self) -> list[tuple[NetConnection, NetConnection]]:
        """Get pairs of connections that need routing."""
        # This would require analyzing the KiCad board to find
        # unconnected pins on the same net
        # This is a simplified implementation

        unrouted_pairs = []

        # Create pairs from all connections (simplified)
        for i in range(len(self.connections)):
            for j in range(i + 1, len(self.connections)):
                # In a real implementation, we'd check if these are actually connected
                unrouted_pairs.append((self.connections[i], self.connections[j]))

        return unrouted_pairs

    def validate_constraints(self) -> list[str]:
        """Validate net against its constraints."""
        violations = []

        # Check connection count
        if len(self.connections) < 2:
            violations.append(f"Net '{self.name}' has fewer than 2 connections")

        # Check trace length constraint
        if self.constraints.max_length > 0:
            total_length = self.get_total_length()
            if total_length > self.constraints.max_length:
                violations.append(
                    f"Net '{self.name}' length {total_length:.3f}mm exceeds maximum {self.constraints.max_length:.3f}mm"
                )

        # Additional constraint checks would go here

        return violations

    def clear_routing(self) -> "PCBNetInterface":
        """Clear all routing for this net (keep connections)."""

        try:
            if self._board is not None:
                # Remove all tracks and vias for this net
                board = self._board.kicad_board

                tracks_to_remove = []
                for track in board.GetTracks():
                    if track.GetNet() == self._kicad_net:
                        tracks_to_remove.append(track)

                for track in tracks_to_remove:
                    board.Remove(track)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to clear routing: {str(e)}")

    def _update_kicad_connection(self, connection: NetConnection) -> None:
        """Update KiCad with the new connection (internal method)."""

        if self._board is None:
            return

        # Find the component and pad
        board = self._board.kicad_board

        for footprint in board.GetFootprints():
            if footprint.GetReference() == connection.component_ref:
                for pad in footprint.Pads():
                    if pad.GetNumber() == connection.pin_number:
                        # Get or create the net
                        if self._kicad_net is None:
                            netlist = board.GetNetInfo()
                            net = netlist.GetNetItem(self.name)
                            if net is None:
                                net = pcbnew.NETINFO_ITEM(board, self.name)
                                board.Add(net)
                            self._kicad_net = net

                        # Connect pad to net
                        pad.SetNet(self._kicad_net)
                        return

        raise RuntimeError(
            f"Component {connection.component_ref} pin {connection.pin_number} not found"
        )

    def _remove_kicad_connection(self, component_ref: str, pin_number: str) -> None:
        """Remove KiCad connection (internal method)."""

        if self._board is None:
            return

        # Find the component and pad, disconnect from net
        board = self._board.kicad_board

        for footprint in board.GetFootprints():
            if footprint.GetReference() == component_ref:
                for pad in footprint.Pads():
                    if pad.GetNumber() == pin_number:
                        # Disconnect pad from net (set to no net)
                        no_net = board.GetNetInfo().GetNetItem("")
                        pad.SetNet(no_net)
                        return

    def set_board(self, board: "PCBBoard") -> None:
        """Set the parent board (internal method)."""
        self._board = board
