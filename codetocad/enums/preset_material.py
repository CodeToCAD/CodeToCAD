from enum import Enum
from typing import Tuple


class MaterialProperty:
    r: float
    g: float
    b: float
    a: float
    reflectivity: float
    roughness: float

    def __init__(
        self,
        color: Tuple[float, float, float, float],
        reflectivity: float,
        roughness: float,
    ):
        self.r, self.g, self.b, self.a = color
        self.reflectivity = reflectivity
        self.roughness = roughness


class PresetMaterial(Enum):
    black = MaterialProperty((0, 0, 0, 1.0), 0.0, 1.0)
    white = MaterialProperty((255, 255, 255, 1.0), 0.0, 1.0)
    red = MaterialProperty((255, 0, 0, 1.0), 0.0, 1.0)
    green = MaterialProperty((0, 255, 0, 1.0), 0.0, 1.0)
    blue = MaterialProperty((0, 0, 255, 1.0), 0.0, 1.0)
    yellow = MaterialProperty((255, 255, 0, 1.0), 0.0, 1.0)
    cyan = MaterialProperty((0, 255, 255, 1.0), 0.0, 1.0)
    magenta = MaterialProperty((255, 0, 255, 1.0), 0.0, 1.0)
    silver = MaterialProperty((192, 192, 192, 1.0), 0.0, 1.0)
    gray = MaterialProperty((128, 128, 128, 1.0), 0.0, 1.0)
    maroon = MaterialProperty((128, 0, 0, 1.0), 0.0, 1.0)
    olive = MaterialProperty((128, 128, 0, 1.0), 0.0, 1.0)
    green2 = MaterialProperty((0, 128, 0, 1.0), 0.0, 1.0)
    purple = MaterialProperty((128, 0, 128, 1.0), 0.0, 1.0)
    teal = MaterialProperty((0, 128, 128, 1.0), 0.0, 1.0)
    navy = MaterialProperty((0, 0, 128, 1.0), 0.0, 1.0)

    @property
    def color(self):
        r = self.value.r
        g = self.value.g
        b = self.value.b
        a = self.value.a
        return (r, g, b, a)

    @property
    def reflectivity(self):
        return self.value.reflectivity

    @property
    def roughness(self):
        return self.value.roughness
