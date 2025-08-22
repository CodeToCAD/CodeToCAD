"""
KiCad PCB Routing implementation for CodeToCAD.

This module provides KiCad-specific implementation of PCB routing operations.
"""

from typing import TYPE_CHECKING
from codetocad.interfaces.cad.pcb.pcb_routing_interface import (
    PCBRoutingInterface,
    ViaType,
    RoutingConstraints,
)
from codetocad.core.dimensions.length_expression import LengthType


try:
    from kipy import KiCad

    KIPY_AVAILABLE = True
except ImportError:
    try:
        from kicad import KiCad

        KIPY_AVAILABLE = True
    except ImportError:
        KiCad = None
        KIPY_AVAILABLE = False

if TYPE_CHECKING:
    from .pcb_board import PCBBoard
    from codetocad.interfaces.cad.pcb.pcb_net_interface import PCBNetInterface


class PCBRouting(PCBRoutingInterface):
    """
    KiCad-specific implementation of PCB routing operations.

    This class provides KiCad-specific implementations for trace routing,
    via placement, and design rule checking using KiCad's pcbnew API.
    """

    def __init__(self, board: "PCBBoard | None" = None):
        super().__init__()
        self._board = board

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
        """Add a straight trace segment."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with routing")

            from ..kicad_actions.routing_operations import create_trace

            # Create trace in KiCad
            track = create_trace(
                self._board.kicad_board,
                float(start_x),
                float(start_y),
                float(end_x),
                float(end_y),
                float(width),
                layer,
                net_name,
            )

            # Add to our trace list
            from codetocad.interfaces.cad.pcb.pcb_routing_interface import (
                TraceSegment,
                TraceShape,
            )

            trace_segment = TraceSegment(
                start_x=float(start_x),
                start_y=float(start_y),
                end_x=float(end_x),
                end_y=float(end_y),
                width=float(width),
                layer=layer,
                net_name=net_name,
                shape=TraceShape.STRAIGHT,
            )
            self.traces.append(trace_segment)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to add trace: {str(e)}")

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
        """Add an arc trace segment."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with routing")

            from ..kicad_actions.routing_operations import create_arc_trace

            # Create arc trace in KiCad
            arc = create_arc_trace(
                self._board.kicad_board,
                float(start_x),
                float(start_y),
                float(end_x),
                float(end_y),
                float(center_x),
                float(center_y),
                float(width),
                layer,
                net_name,
            )

            # Add to our trace list
            from codetocad.interfaces.cad.pcb.pcb_routing_interface import (
                TraceSegment,
                TraceShape,
            )

            trace_segment = TraceSegment(
                start_x=float(start_x),
                start_y=float(start_y),
                end_x=float(end_x),
                end_y=float(end_y),
                width=float(width),
                layer=layer,
                net_name=net_name,
                shape=TraceShape.ARC,
                arc_center_x=float(center_x),
                arc_center_y=float(center_y),
            )
            self.traces.append(trace_segment)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to add arc trace: {str(e)}")

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
        """Add a via."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with routing")

            from ..kicad_actions.routing_operations import create_via

            # Create via in KiCad
            via = create_via(
                self._board.kicad_board,
                float(x),
                float(y),
                float(drill_diameter),
                float(pad_diameter),
                start_layer,
                end_layer,
                net_name,
            )

            # Add to our via list
            from codetocad.interfaces.cad.pcb.pcb_routing_interface import ViaDefinition

            via_def = ViaDefinition(
                x=float(x),
                y=float(y),
                via_type=via_type,
                drill_diameter=float(drill_diameter),
                pad_diameter=float(pad_diameter),
                start_layer=start_layer,
                end_layer=end_layer,
                net_name=net_name,
            )
            self.vias.append(via_def)

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to add via: {str(e)}")

    def route_net(
        self, net: "PCBNetInterface", algorithm: str = "auto"
    ) -> "PCBRoutingInterface":
        """Automatically route a net."""

        try:
            if self._board is None:
                raise RuntimeError("No board associated with routing")

            from ..kicad_actions.routing_operations import route_net_auto

            # Auto-route the net in KiCad
            routed_items = route_net_auto(self._board.kicad_board, net.name, algorithm)

            # Update our routing data based on created items
            # This is a simplified implementation

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to route net: {str(e)}")

    def route_differential_pair(
        self,
        net_positive: "PCBNetInterface",
        net_negative: "PCBNetInterface",
        spacing: LengthType,
        trace_width: LengthType,
    ) -> "PCBRoutingInterface":
        """Route a differential pair."""
        # Differential pair routing is complex and would require
        # specialized KiCad routing algorithms
        # This is a placeholder implementation

        # Route each net individually with constraints
        self.route_net(net_positive, "shortest")
        self.route_net(net_negative, "shortest")

        return self

    def set_routing_constraints(
        self, constraints: RoutingConstraints
    ) -> "PCBRoutingInterface":
        """Set routing constraints."""
        self.routing_constraints = constraints

        if self._board is not None:
            # Update KiCad design rules based on constraints
            rules = {
                "min_trace_width": constraints.min_trace_width,
                "min_via_size": constraints.min_via_size,
                "min_spacing": constraints.min_spacing,
            }
            self._board.set_design_rules(rules)

        return self

    def optimize_routing(
        self, net_names: list[str] | None = None
    ) -> "PCBRoutingInterface":
        """Optimize routing for specified nets or all nets."""
        # Routing optimization would require advanced algorithms
        # This is a placeholder implementation
        return self

    def check_design_rules(self) -> list[str]:
        """Check routing against design rules."""

        try:
            if self._board is None:
                return ["No board associated with routing"]

            from ..kicad_actions.routing_operations import check_design_rules

            violations = check_design_rules(self._board.kicad_board)
            return violations

        except Exception as e:
            return [f"Design rule check failed: {str(e)}"]

    def get_trace_length(self, net_name: str) -> float:
        """Calculate total trace length for a net."""

        try:
            if self._board is None:
                return 0.0

            from ..kicad_actions.routing_operations import get_net_info

            net_info = get_net_info(self._board.kicad_board, net_name)
            return net_info.get("total_length_mm", 0.0)

        except Exception:
            return 0.0

    def remove_routing(self, net_name: str) -> "PCBRoutingInterface":
        """Remove all routing for a specific net."""

        try:
            if self._board is None:
                return self

            # Remove traces and vias for the specified net
            board = self._board.kicad_board

            # Remove tracks
            tracks_to_remove = []
            for track in board.GetTracks():
                if track.GetNet().GetNetname() == net_name:
                    tracks_to_remove.append(track)

            for track in tracks_to_remove:
                board.Remove(track)

            # Update our internal lists
            self.traces = [t for t in self.traces if t.net_name != net_name]
            self.vias = [v for v in self.vias if v.net_name != net_name]

            return self

        except Exception as e:
            raise RuntimeError(f"Failed to remove routing: {str(e)}")

    def set_board(self, board: "PCBBoard") -> None:
        """Set the parent board (internal method)."""
        self._board = board
