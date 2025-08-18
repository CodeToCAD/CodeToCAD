from codetocad.interfaces.cad.sketch.sketch_get import SketchGet
from codetocad.interfaces.cad.wire.wire import Wire
from codetocad.interfaces.cad.wire.wire_add import WireAdd
from codetocad.interfaces.cad.wire.wire_presets import WirePresets


class Sketch:
    def __init__(self):
        self.wires: list[Wire] = []
        self.preset = WirePresets(Wire, self)
        self.get = SketchGet(self)

    def add(self, wire: Wire):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

    @property
    def draw(self):
        """Draw on the last wire in the sketch. If no wire exists, create a new one."""
        wire = self.wires[-1] if self.wires else None

        if not wire:
            wire = Wire(self)

            self.add(wire)

        return WireAdd(wire)

    def __repr__(self):
        return f"<Sketch: {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
