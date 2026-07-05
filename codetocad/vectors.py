"""Small vector value types used across CodeToCAD, backed by numpy."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> "Vec3":
        return cls(float(array[0]), float(array[1]), float(array[2]))

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z], dtype=np.float64)

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3.from_numpy(self.to_numpy() + other.to_numpy())

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3.from_numpy(self.to_numpy() - other.to_numpy())

    def __mul__(self, scalar: float) -> "Vec3":
        return Vec3.from_numpy(self.to_numpy() * scalar)

    __rmul__ = __mul__

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class Vec4:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> "Vec4":
        return cls(float(array[0]), float(array[1]), float(array[2]), float(array[3]))

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z, self.w], dtype=np.float64)

    def to_tuple(self) -> tuple[float, float, float, float]:
        return (self.x, self.y, self.z, self.w)
