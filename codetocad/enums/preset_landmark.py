from enum import Enum
from typing import Optional


class PresetLandmark(Enum):
    left = 2
    right = 4
    top = 8
    bottom = 16
    front = 32
    back = 64
    center = 128
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
        from codetocad.utilities import center, min, max

        x = (
            min
            if self.contains(PresetLandmark.left)
            else max
            if self.contains(PresetLandmark.right)
            else center
        )
        y = (
            min
            if self.contains(PresetLandmark.front)
            else max
            if self.contains(PresetLandmark.back)
            else center
        )
        z = (
            min
            if self.contains(PresetLandmark.bottom)
            else max
            if self.contains(PresetLandmark.top)
            else center
        )
        return (x, y, z)
