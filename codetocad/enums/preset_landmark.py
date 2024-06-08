from enum import Enum
from typing import Optional

from codetocad.enums.axis import Axis


class PresetLandmark(Enum):
    left = 2
    right = 4
    top = 8
    bottom = 16
    front = 32
    back = 64
    center = 128
    start = 256
    end = 512
    leftTop = left | top
    leftBottom = left | bottom
    leftFront = left | front
    leftBack = left | back
    rightTop = right | top
    rightBottom = right | bottom
    rightFront = right | front
    rightBack = right | back
    frontTop = front | top
    backTop = back | top
    frontBottom = front | bottom
    backBottom = back | bottom
    leftFrontTop = left | front | top
    leftBackTop = left | back | top
    leftFrontBottom = left | front | bottom
    leftBackBottom = left | back | bottom
    rightFrontTop = right | front | top
    rightBackTop = right | back | top
    rightFrontBottom = right | front | bottom
    rightBackBottom = right | back | bottom

    def __ror__(self, other):
        return self.value | other.value

    def __and__(self, other):
        return self.value & other.value

    def contains(self, other):
        return self & other == other.value

    @staticmethod
    def from_string(landmark_name) -> Optional["PresetLandmark"]:
        for preset in PresetLandmark:
            if preset.name == landmark_name:
                return preset
        return None

    def get_xyz(self):

        x = (
            Axis.MIN
            if self.contains(PresetLandmark.left)
            else Axis.MAX if self.contains(PresetLandmark.right) else Axis.CENTER
        )
        y = (
            Axis.MIN
            if self.contains(PresetLandmark.front)
            else Axis.MAX if self.contains(PresetLandmark.back) else Axis.CENTER
        )
        z = (
            Axis.MIN
            if self.contains(PresetLandmark.bottom)
            else Axis.MAX if self.contains(PresetLandmark.top) else Axis.CENTER
        )
        return (x, y, z)
