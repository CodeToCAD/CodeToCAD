from dataclasses import dataclass
from functools import reduce
from typing import TYPE_CHECKING, Tuple

from codetocad.core.dimensions.length_expression import LengthExp, LengthType


@dataclass
class Point:
    x: LengthType
    y: LengthType
    z: LengthType

    @property
    def _x(self):
        return LengthExp(self.x)
    @property
    def _y(self):
        return LengthExp(self.y)
    @property
    def _z(self):
        return LengthExp(self.z)

    def to_list(self) -> list[float]:
        return [self._x.value, self._y.value, self._z.value]

    def to_tuple(self) -> tuple[float, float, float]:
        return (self._x.value, self._y.value, self._z.value)

    def magnitude(self) -> float:
        return pow(
            reduce(
                lambda acc, value: pow(value, 2) + acc,
                self.to_list(),
                0,
            ),
            1 / 2,
        )

    def distance_to(self, other: "Point") -> float:
        return (other - self).magnitude()

    def is_touching(
        self,
        other: "Point",
        tolerance: float = 0.001,
    ) -> bool:
        return self.distance_to(other) < tolerance

    @staticmethod
    def from_list(point_list: list[LengthType]|tuple[LengthType, LengthType, LengthType]) -> "Point":
        assert len(point_list) == 3, "Point list must contain three Dimensions."
        return Point(point_list[0], point_list[1], point_list[2])

    def arithmetic_precheck_and_unit_conversion(self, other) -> "Point":
        assert other is not None, "Right-hand value cannot be None."

        if isinstance(other, (int, float)):
            return Point(other, other, other)

        if isinstance(other, (list, tuple)):
            return Point.from_list(other)

        if isinstance(other, Point):
            return other

        raise TypeError("Only int/float/Point or a list of those types is allowed.")

    def __eq__(self, other) -> bool:
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self._x == other._x and self._y == other._y and self._z == other._z

    def __lt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self._x < other._x and self._y < other._y and self._z < other._z

    def __le__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self._x <= other._x and self._y <= other._y and self._z <= other._z

    def __gt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self._x > other._x and self._y > other._y and self._z > other._z

    def __ge__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self._x >= other._x and self._y >= other._y and self._z >= other._z

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self._x + other._x
        y = self._y + other._y
        z = self._z + other._z
        return Point(x, y, z)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self._x - other._x
        y = self._y - other._y
        z = self._z - other._z
        return Point(x, y, z)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self._x * other._x
        y = self._y * other._y
        z = self._z * other._z
        return Point(x, y, z)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self._x / other._x
        y = self._y / other._y
        z = self._z / other._z
        return Point(x, y, z)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self._x // other._x
        y = self._y // other._y
        z = self._z // other._z
        return Point(x, y, z)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self._x % other._x
        y = self._y % other._y
        z = self._z % other._z
        return Point(x, y, z)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     x = divmod(self._x, other._x)
    #     y = divmod(self._y, other._y)
    #     z = divmod(self._z, other._z)
    #     return Point(x, y, z)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = pow(self._x, other._x)
        y = pow(self._y, other._y)
        z = pow(self._z, other._z)
        return Point(x, y, z)

    def __abs__(self):
        x = abs(self._x)
        y = abs(self._y)
        z = abs(self._z)
        return Point(x, y, z)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Point(self._x, self._y, self._z)

    def copy(self):
        return self.__deepcopy__()

    def __getitem__(self, key) -> float:
        if key == 0:
            return self._x._meters
        if key == 1:
            return self._x._meters
        if key == 2:
            return self._x._meters
        raise IndexError("Index out of range.")

    def __str__(self):
        return f"""x   y   z
{self._x}  {self._y}  {self._z}
"""

    def __repr__(self) -> str:
        return self.__str__()
