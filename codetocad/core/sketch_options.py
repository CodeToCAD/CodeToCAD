from dataclasses import dataclass

from codetocad.core.angle import Angle


@dataclass
class SketchOptions:
    rotation_x: str | float | Angle | None = None
    rotation_y: str | float | Angle | None = None
    rotation_z: str | float | Angle | None = None
