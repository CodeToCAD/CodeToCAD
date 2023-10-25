from enum import Enum


class ScalingMethods(Enum):
    toSpecificLength = 0
    scaleFactor = 1
    lockAspectRatio = 2  # scale one dimension, the others scale with it
