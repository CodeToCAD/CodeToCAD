from codetocad.interfaces.landmark_interface import LandmarkInterface
from typing import Self
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.base import (
    get_body,
    get_component,
    get_sketch,
)
from providers.fusion360.fusion360_provider.fusion_actions.fusion_landmark import (
    FusionLandmark,
)
from .fusion_actions.fusion_body import FusionBody
from .fusion_actions.fusion_sketch import FusionSketch


class Entity(EntityInterface):

    def __init__(
        self,
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @property
    def _center(self):
        if isinstance(self, PartInterface):
            return FusionBody(self.name).center
        if isinstance(self, SketchInterface):
            return FusionSketch(self.name).center

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def is_exists(self) -> bool:
        try:
            component = get_component(self.name)
            if isinstance(self, PartInterface):
                return get_body(component, self.name) != None
            elif isinstance(self, SketchInterface):
                return get_sketch(component, self.name) != None
            raise NotImplementedError()
        except:
            return False

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def delete(self, remove_children: "bool" = True):
        if isinstance(self, PartInterface):
            FusionBody(self.name).delete()
        if isinstance(self, SketchInterface):
            FusionSketch(self.name).delete()
        if isinstance(self, LandmarkInterface):
            FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).delete()
        return self

    @supported(SupportLevel.PLANNED)
    def is_visible(self) -> bool:
        raise NotImplementedError()
        return True

    @supported(SupportLevel.PLANNED)
    def set_visible(self, is_visible: "bool"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def get_native_instance(self) -> object:
        if isinstance(self, PartInterface):
            return FusionBody(self.name)
        if isinstance(self, SketchInterface):
            return FusionSketch(self.name)
        if isinstance(self, LandmarkInterface):
            return FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            )
        raise NotImplementedError()

    @supported(SupportLevel.PLANNED)
    def get_location_world(self) -> "Point":
        raise NotImplementedError()
        return Point.from_list_of_float_or_string([0, 0, 0])

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def get_location_local(self) -> "Point":
        if isinstance(self, PartInterface):
            pos = FusionBody(self.name).center
        elif isinstance(self, SketchInterface):
            pos = FusionSketch(self.name).center
        elif isinstance(self, LandmarkInterface):
            pos = FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).get_point()
        return Point(pos.x, pos.y, pos.z)

    @supported(SupportLevel.PLANNED)
    def select(self):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        if isinstance(self, PartInterface):
            FusionBody(self.name).translate(x, y, z)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).translate(x, y, z)
        elif isinstance(self, LandmarkInterface):
            FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).translate(x, y, z)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_x(self, amount: "str|float|Dimension"):
        if isinstance(self, PartInterface):
            FusionBody(self.name).translate(amount, 0, 0)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).translate(amount, 0, 0)
        elif isinstance(self, LandmarkInterface):
            FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).translate(amount, 0, 0)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_y(self, amount: "str|float|Dimension"):
        if isinstance(self, PartInterface):
            FusionBody(self.name).translate(0, amount, 0)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).translate(0, amount, 0)
        elif isinstance(self, LandmarkInterface):
            FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).translate(0, amount, 0)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part, Sketch and Landmark entities.")
    def translate_z(self, amount: "str|float|Dimension"):
        if isinstance(self, PartInterface):
            FusionBody(self.name).translate(0, 0, amount)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).translate(0, 0, amount)
        elif isinstance(self, LandmarkInterface):
            FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).translate(0, 0, amount)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ):
        self.rotate_x(x)
        self.rotate_y(y)
        self.rotate_z(z)
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_x(self, rotation: "str|float|Angle"):
        if isinstance(self, PartInterface):
            FusionBody(self.name).rotate("x", rotation)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).rotate("x", rotation)
        else:
            raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_y(self, rotation: "str|float|Angle"):
        if isinstance(self, PartInterface):
            FusionBody(self.name).rotate("y", rotation)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).rotate("y", rotation)
        else:
            raise NotImplementedError()
        return self

    @supported(SupportLevel.PARTIAL, "Supports Part and Sketch entities.")
    def rotate_z(self, rotation: "str|float|Angle"):
        if isinstance(self, PartInterface):
            FusionBody(self.name).rotate("z", rotation)
        elif isinstance(self, SketchInterface):
            FusionSketch(self.name).rotate("z", rotation)
        else:
            raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def get_bounding_box(self) -> "BoundaryBox":
        if isinstance(self, PartInterface):
            boundaryBox = FusionBody(self.name).get_bounding_box()
        elif isinstance(self, SketchInterface):
            boundaryBox = FusionSketch(self.name).get_bounding_box()
        else:
            raise NotImplementedError()
        return boundaryBox

    @supported(SupportLevel.SUPPORTED)
    def get_dimensions(self) -> "Dimensions":
        if isinstance(self, PartInterface):
            dimensions = FusionBody(self.name).get_dimensions()
        elif isinstance(self, SketchInterface):
            dimensions = FusionSketch(self.name).get_dimensions()
        else:
            raise NotImplementedError()
        return dimensions

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_name(
        self, new_name: "str", rename_linked_entities_and_landmarks: "bool" = True
    ) -> Self:
        if isinstance(self, PartInterface):
            FusionBody(self.name).rename(new_name)
        if isinstance(self, SketchInterface):
            FusionSketch(self.name).rename(new_name)
        if isinstance(self, LandmarkInterface):
            FusionLandmark(
                self.name, self.get_parent_entity().get_native_instance()
            ).rename(new_name)
        self.name = new_name
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_name(self) -> "str":
        print("get_name called")
        return "String"

    @supported(SupportLevel.SUPPORTED, notes="")
    def update_native_instance(self) -> "object":
        print("update_native_instance called")
        return self
