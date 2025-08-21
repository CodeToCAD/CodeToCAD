"""
build123d-specific wire presets.
"""

from typing import TYPE_CHECKING
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.build123d_actions.geometry import (
    create_rectangle_wire,
    create_circle_wire,
    create_regular_polygon_wire,
    create_polyline_wire,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.sketch.sketch import Sketch
    from codetocad.adapters.build123d.cad.wire.wire import Wire


class Build123dWirePresets(WirePresetsInterface):
    """build123d-specific wire presets that use native build123d geometry creation."""

    def rectangle(self, x: LengthType, y: LengthType) -> "Wire":
        """Create a rectangular wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d rectangle
        native_rect = create_rectangle_wire(x, y)
        wire = Wire(self.sketch, native_instance=native_rect)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def circle(self, radius: LengthType) -> "Wire":
        """Create a circular wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d circle
        native_circle = create_circle_wire(radius)
        wire = Wire(self.sketch, native_instance=native_circle)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def regular_polygon(
        self, radius: LengthType, side_count: int, rotation: float = 0
    ) -> "Wire":
        """Create a regular polygon wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d regular polygon
        native_polygon = create_regular_polygon_wire(radius, side_count, rotation)
        wire = Wire(self.sketch, native_instance=native_polygon)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def polyline(self, points: list[tuple[float, float]]) -> "Wire":
        """Create a polyline wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d polyline
        native_polyline = create_polyline_wire(points)
        wire = Wire(self.sketch, native_instance=native_polyline)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
