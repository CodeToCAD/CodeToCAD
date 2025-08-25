from dataclasses import dataclass
from functools import reduce
from typing import TYPE_CHECKING, Tuple


@dataclass
class Point:
    x: float
    y: float
    z: float

    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

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
    def from_list(point_list: list[float]) -> "Point":
        assert len(point_list) == 3, "Point list must contain three Dimensions."
        return Point(point_list[0], point_list[1], point_list[2])

    def arithmetic_precheck_and_unit_conversion(self, other) -> "Point":
        assert other is not None, "Right-hand value cannot be None."

        if isinstance(other, (int, float)):
            return Point(other, other, other)

        if isinstance(other, list):
            return Point.from_list(other)

        if isinstance(other, Point):
            return other

        raise TypeError("Only int/float/Point or a list of those types is allowed.")

    def __eq__(self, other) -> bool:
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __gt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x, y, z)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        return Point(x, y, z)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Point(x, y, z)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x // other.x
        y = self.y // other.y
        z = self.z // other.z
        return Point(x, y, z)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = self.x % other.x
        y = self.y % other.y
        z = self.z % other.z
        return Point(x, y, z)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     x = divmod(self.x, other.x)
    #     y = divmod(self.y, other.y)
    #     z = divmod(self.z, other.z)
    #     return Point(x, y, z)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        x = pow(self.x, other.x)
        y = pow(self.y, other.y)
        z = pow(self.z, other.z)
        return Point(x, y, z)

    def __abs__(self):
        x = abs(self.x)
        y = abs(self.y)
        z = abs(self.z)
        return Point(x, y, z)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Point(self.x, self.y, self.z)

    def copy(self):
        return self.__deepcopy__()

    def __getitem__(self, key) -> float:
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        raise IndexError("Index out of range.")

    def __str__(self):
        return f"""x   y   z
{self.x}  {self.y}  {self.z}
"""

    def __repr__(self) -> str:
        return self.__str__()
