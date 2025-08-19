import bpy
from typing import List
from uuid import uuid4

from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.adapters.blender.cad.sketch.sketch_get import SketchGet
from codetocad.adapters.blender.blender_actions.objects import create_object


class Sketch(SketchInterface):
    """Blender implementation of SketchInterface."""

    def __init__(self, name: str | None = None):
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.wire.wire import Wire
        from codetocad.adapters.blender.cad.wire.wire_add import WireAdd

        # Blender-specific properties
        self.name = name or f"sketch_{str(uuid4())[:8]}"
        self._blender_object: bpy.types.Object | None = None

        # Initialize parent interface properties
        self.wires: List[Wire] = []
        self.preset = WirePresetsInterface(Wire, self)
        self.get = SketchGet(self)

        # Create Blender representation
        self._create_blender_sketch()

    def _create_blender_sketch(self):
        """Create a Blender collection to represent this sketch."""
        # Create a collection for organizing sketch objects
        if self.name not in bpy.data.collections:
            collection = bpy.data.collections.new(self.name)
            bpy.context.scene.collection.children.link(collection)

        # Create an empty object to represent the sketch
        empty_data = None  # Empty objects don't need data
        self._blender_object = create_object(f"{self.name}_origin", empty_data)
        self._blender_object.empty_display_type = "PLAIN_AXES"
        self._blender_object.empty_display_size = 0.1

        # Add to the sketch collection
        sketch_collection = bpy.data.collections[self.name]
        sketch_collection.objects.link(self._blender_object)

        # Remove from scene collection to avoid duplication
        if self._blender_object.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(self._blender_object)

    def add(self, wire):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

        # Add wire's Blender object to sketch collection
        if wire.get_blender_object() and self.name in bpy.data.collections:
            sketch_collection = bpy.data.collections[self.name]
            wire_obj = wire.get_blender_object()

            # Add to sketch collection if not already there
            if wire_obj.name not in sketch_collection.objects:
                sketch_collection.objects.link(wire_obj)

                # Remove from scene collection to avoid duplication
                if wire_obj.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(wire_obj)

    @property
    def draw(self):
        """Draw on the last wire in the sketch. If no wire exists, create a new one."""
        from codetocad.adapters.blender.cad.wire.wire import Wire
        from codetocad.adapters.blender.cad.wire.wire_add import WireAdd

        wire = self.wires[-1] if self.wires else None

        if not wire:
            wire = Wire(self)
            self.add(wire)

        return WireAdd(wire)

    def get_blender_object(self) -> "bpy.types.Object | None":
        """Get the Blender object representing this sketch."""
        return self._blender_object

    def get_collection(self) -> "bpy.types.Collection | None":
        """Get the Blender collection containing sketch objects."""
        return bpy.data.collections.get(self.name)

    def get_all_vertices(self) -> List:
        """Get all vertices from all wires in the sketch."""
        vertices = []
        for wire in self.wires:
            vertices.extend(wire.get_vertices())
        return vertices

    def get_all_edges(self) -> List:
        """Get all edges from all wires in the sketch."""
        edges = []
        for wire in self.wires:
            edges.extend(wire.edges)
        return edges

    def get_bounding_box(self) -> tuple:
        """Get the bounding box of all objects in the sketch."""
        if not self.wires:
            return ((0, 0, 0), (0, 0, 0))

        all_vertices = self.get_all_vertices()
        if not all_vertices:
            return ((0, 0, 0), (0, 0, 0))

        positions = [v.position for v in all_vertices]
        min_pos = [min(pos[i] for pos in positions) for i in range(3)]
        max_pos = [max(pos[i] for pos in positions) for i in range(3)]

        return (tuple(min_pos), tuple(max_pos))

    def clear(self):
        """Remove all wires from the sketch."""
        # Remove Blender objects
        if self.name in bpy.data.collections:
            collection = bpy.data.collections[self.name]
            for obj in list(collection.objects):
                if obj != self._blender_object:  # Keep the sketch origin
                    collection.objects.unlink(obj)
                    if obj.data:
                        bpy.data.meshes.remove(obj.data)
                    bpy.data.objects.remove(obj)

        # Clear wires list
        self.wires.clear()

    def hide(self):
        """Hide the sketch in Blender."""
        if self.name in bpy.data.collections:
            collection = bpy.data.collections[self.name]
            collection.hide_viewport = True

    def show(self):
        """Show the sketch in Blender."""
        if self.name in bpy.data.collections:
            collection = bpy.data.collections[self.name]
            collection.hide_viewport = False

    def __repr__(self):
        return f"<Sketch(name='{self.name}'): {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
