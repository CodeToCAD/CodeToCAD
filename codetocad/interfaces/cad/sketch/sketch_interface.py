from codetocad.interfaces.cad.sketch.sketch_get import SketchGetInterface
from codetocad.interfaces.cad.wire.wire_interface import WireInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface


class SketchInterface:
    def __init__(self):
        self.wires: list[WireInterface] = []
        self.preset = WirePresetsInterface(WireInterface, self)
        self.get = SketchGetInterface(self)

    def add(self, wire: WireInterface):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

    @property
    def draw(self):
        """Draw on the last wire in the sketch. If no wire exists, create a new one."""
        wire = self.wires[-1] if self.wires else None

        if not wire:
            wire = WireInterface(self)

            self.add(wire)

        return WireAddInterface(wire)

    def __repr__(self):
        return f"<Sketch: {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
