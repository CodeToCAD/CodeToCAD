from typing import Optional

from codetocad.interfaces import WireInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

from . import blender_actions
from . import blender_definitions

if TYPE_CHECKING:
    from . import Edge
    from . import Part


class Wire(Entity, WireInterface):
    edges: "list[Edge]"
    parent_sketch: Optional[SketchOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        edges: "list[Edge]",
        name: str,
        parent_sketch: Optional[SketchOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.edges = edges
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def is_closed(self) -> bool:
        raise NotImplementedError()

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        raise NotImplementedError()
        return self

    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        raise NotImplementedError()
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        raise NotImplementedError()
        return self

    def loft(self, other: "Wire", new_part_name: Optional[str] = None) -> "Part":

        blender_mesh = blender_actions.loft(self, other)

        from . import Part
        part = Part(blender_mesh.name)

        if new_part_name:
            part.rename(new_part_name)
        else:
            if self.parent_sketch:
                parent_name = self.parent_sketch.name if not isinstance(
                    self.parent_sketch, str) else self.parent_sketch

                if type(blender_actions.get_object(parent_name)) == blender_definitions.BlenderTypes.MESH.value:
                    part.union(
                        parent_name,
                        delete_after_union=True,
                        is_transfer_landmarks=True
                    )
                else:
                    Entity(parent_name).delete()

                part.rename(parent_name)
            if other.parent_sketch:
                parent_name = other.parent_sketch.name if not isinstance(
                    other.parent_sketch, str) else other.parent_sketch

                if type(blender_actions.get_object(parent_name)) == blender_definitions.BlenderTypes.MESH.value:
                    part.union(
                        parent_name,
                        delete_after_union=True,
                        is_transfer_landmarks=True
                    )
                else:
                    Entity(parent_name).delete()

        return part
