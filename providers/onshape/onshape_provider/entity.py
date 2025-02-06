from typing import Optional
from typing import Self
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Entity(EntityInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_exists(self) -> "bool":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete(self, remove_children: "bool" = True) -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_visible(self) -> "bool":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_visible(self, is_visible: "bool") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ) -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_native_instance(self) -> "Any":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location_world(self) -> "Point":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location_local(self) -> "Point":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def select(self) -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_x(self, amount: "str|float|Dimension") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_y(self, amount: "str|float|Dimension") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_z(self, amount: "str|float|Dimension") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ) -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_x(self, rotation: "str|float|Angle") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_y(self, rotation: "str|float|Angle") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_z(self, rotation: "str|float|Angle") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(self) -> "BoundaryBox":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(self) -> "Dimensions":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_name(
        self, new_name: "str", rename_linked_entities_and_landmarks: "bool" = True
    ) -> "Self":
        print(
            "set_name called", f": {new_name}, {rename_linked_entities_and_landmarks}"
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_name(self) -> "str":
        print("get_name called")
        return "String"
