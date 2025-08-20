from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.adapters.blender.cad.sketch.sketch_get import SketchGet
from codetocad.adapters.blender.blender_actions.objects import create_object
from codetocad.adapters.blender.blender_actions.collections import (
    create_collection,
    get_collection,
    get_collection_or_none,
    get_scene_collection,
    link_object_to_collection,
    unlink_object_from_collection,
)
from codetocad.adapters.blender.blender_actions.mesh import remove_mesh

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.wire.wire import Wire
    import bpy


class Sketch(SketchInterface):
    """Blender implementation of SketchInterface."""

    def __init__(self, name: str | None = None):
        # Initialize parent interface first
        super().__init__()

        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.wire.wire import Wire
        from codetocad.adapters.blender.cad.wire.wire_add import WireAdd

        # Blender-specific properties
        self.name = name or f"sketch_{str(uuid4())[:8]}"
        self._blender_object: bpy.types.Object | None = None

        # Initialize parent interface properties
        self.wires: list[Wire] = []  # type: ignore
        self.preset = WirePresetsInterface(Wire, self)
        self.get = SketchGet(self)

        # Override operations with Blender-specific implementation
        from codetocad.adapters.blender.cad.sketch.sketch_operations import (
            SketchOperations,
        )

        self.operations = SketchOperations(self)

        # Create Blender representation
        self._create_blender_sketch()

    def _create_blender_sketch(self):
        """Create a Blender collection to represent this sketch."""
        # Create a collection for organizing sketch objects
        if not get_collection_or_none(self.name):
            create_collection(self.name)

        # Create an empty object to represent the sketch
        empty_data = None  # Empty objects don't need data
        self._blender_object = create_object(f"{self.name}_origin", empty_data)
        self._blender_object.empty_display_type = "PLAIN_AXES"
        self._blender_object.empty_display_size = 0.1

        # Add to the sketch collection
        sketch_collection = get_collection(self.name)
        if sketch_collection:
            link_object_to_collection(self._blender_object, sketch_collection)

        # Remove from scene collection to avoid duplication
        scene_collection = get_scene_collection()
        if self._blender_object.name in scene_collection.objects:
            unlink_object_from_collection(self._blender_object, scene_collection)

    def add(self, wire: "Wire"):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

        # Add wire's Blender object to sketch collection
        wire_obj = wire.get_blender_object()
        if wire_obj:
            sketch_collection = get_collection_or_none(self.name)
            if sketch_collection:
                # Add to sketch collection if not already there
                if wire_obj.name not in sketch_collection.objects:
                    link_object_to_collection(wire_obj, sketch_collection)

                    # Remove from scene collection to avoid duplication
                    scene_collection = get_scene_collection()
                    if wire_obj.name in scene_collection.objects:
                        unlink_object_from_collection(wire_obj, scene_collection)

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
        return get_collection_or_none(self.name)

    def get_all_vertices(self) -> list:
        """Get all vertices from all wires in the sketch."""
        vertices = []
        for wire in self.wires:
            vertices.extend(wire.get_vertices())
        return vertices

    def get_all_edges(self) -> list:
        """Get all edges from all wires in the sketch."""
        edges = []
        for wire in self.wires:
            edges.extend(wire.edges)
        return edges

    def hide(self):
        """Hide the sketch in Blender."""
        collection = get_collection_or_none(self.name)
        if collection:
            collection.hide_viewport = True

    def show(self):
        """Show the sketch in Blender."""
        collection = get_collection_or_none(self.name)
        if collection:
            collection.hide_viewport = False

    def __repr__(self):
        return f"<Sketch(name='{self.name}'): {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
