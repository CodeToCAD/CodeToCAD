from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Tuple
from codetocad.core.dimension import Dimension


if TYPE_CHECKING:
    from codetocad.codetocad_types import PointOrListOfFloatOrItsStringValue


@dataclass
class Point:
    x: Dimension
    y: Dimension
    z: Dimension

    def to_list(self):
        return [self.x, self.y, self.z]

    def to_tuple(self) -> Tuple[Dimension, Dimension, Dimension]:
        return (self.x, self.y, self.z)

    @staticmethod
    def from_list(point_list: List[Dimension]) -> "Point":
        assert len(point_list) == 3, "Point list must contain three Dimensions."
        return Point(point_list[0], point_list[1], point_list[2])

    @staticmethod
    def from_list_of_float_or_string(
        point_representation: "PointOrListOfFloatOrItsStringValue",
    ) -> "Point":
        if isinstance(point_representation, list):
            assert (
                len(point_representation) == 3
            ), "Point list must contain three Dimensions."
            points = [
                Dimension.from_dimension_or_its_float_or_string_value(point, None)
                for point in point_representation
            ]
            return Point(points[0], points[1], points[2])
        elif isinstance(point_representation, str):
            from codetocad.utilities import get_dimension_list_from_string_list

            points = get_dimension_list_from_string_list(point_representation)
            return Point(points[0], points[1], points[2])
        elif isinstance(point_representation, Point):
            return point_representation

        raise ValueError(f"Cannot convert type {type(point_representation)} to Point.")

    def arithmetic_precheck_and_unit_conversion(self, other) -> "Point":
        assert other is not None, "Right-hand value cannot be None."

        if not isinstance(other, (int, float, str, Dimension, list, Point)):
            raise TypeError(
                "Only int/float, Dimension, or Dimension String, or a list of those types is allowed."
            )

        if isinstance(other, (int, float)):
            return Point(Dimension(other), Dimension(other), Dimension(other))

        x = Dimension(0)
        y = Dimension(0)
        z = Dimension(0)

        from codetocad.utilities import get_dimension_list_from_string_list

        if isinstance(other, list):
            [x, y, z] = get_dimension_list_from_string_list(other)

        if isinstance(other, str):
            if "," in other:
                [x, y, z] = get_dimension_list_from_string_list(other)
            else:
                other = Dimension.from_string(other)

        if isinstance(other, Dimension):
            x = other
            y = other
            z = other

        if isinstance(other, Point):
            x = other.x
            y = other.y
            z = other.z

        if x.unit is not None and self.x.unit is not None and x.unit != self.x.unit:
            x: Dimension = x.convert_to_unit(self.x.unit)
        if y.unit is not None and self.y.unit is not None and y.unit != self.y.unit:
            y: Dimension = y.convert_to_unit(self.y.unit)
        if z.unit is not None and self.z.unit is not None and z.unit != self.z.unit:
            z: Dimension = z.convert_to_unit(self.z.unit)
        return Point(x, y, z)

    def __eq__(self, other) -> bool:
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return self.x == other.x and self.y == other.y and self.z == other.z

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

    def __getitem__(self, key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z

    def __str__(self):
        return f"""x   y   z
{self.x}  {self.y}  {self.z}
"""

    def __repr__(self) -> str:
        return self.__str__()
