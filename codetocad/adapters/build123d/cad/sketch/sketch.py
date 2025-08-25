"""
build123d implementation of SketchInterface.
"""

from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.adapters.build123d.cad.sketch.sketch_get import SketchGet
from codetocad.adapters.build123d.cad.wire.wire_presets import Build123dWirePresets
from codetocad.adapters.build123d.build123d_actions.sketch_operations import (
    create_sketch_context,
    get_sketch_wires,
    get_sketch_faces,
    make_face_from_sketch,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.wire.wire import Wire
    import build123d as bd


class Sketch(SketchInterface):
    """build123d implementation of SketchInterface."""

    def __init__(
        self, name: str | None = None, native_instance: "bd.BuildSketch | None" = None
    ):
        # Initialize parent interface first
        super().__init__()

        # build123d-specific properties
        self.name = name or f"sketch_{str(uuid4())[:8]}"
        self.native_instance = native_instance

        # Initialize parent interface properties
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        self.wires: list[Wire] = []  # type: ignore
        self.preset = Build123dWirePresets(Wire, self)
        self.get = SketchGet(self)

        # Override operations with build123d-specific implementation
        from codetocad.adapters.build123d.cad.sketch.sketch_operations import (
            SketchOperations,
        )

        self.operations = SketchOperations(self)

        # Create build123d sketch context if not provided
        if self.native_instance is None:
            self.native_instance = create_sketch_context()

    def add(self, wire: "Wire"):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

        # Add the wire to the member sketches
        if self not in wire.member_sketches:
            wire.member_sketches.append(self)

    @property
    def draw(self):
        """Draw on the last wire in the sketch. If no wire exists, create a new one."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire
        from codetocad.adapters.build123d.cad.wire.wire_add import WireAdd

        wire = self.wires[-1] if self.wires else None

        if not wire:
            wire = Wire(self)
            self.add(wire)

        return WireAdd(wire)

    def __repr__(self):
        return f"<Sketch: {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
