from enum import Enum
from typing import Union


class Axis(str, Enum):
    X = "x"
    Y = "y"
    Z = "z"

    MAX = "max"
    MIN = "min"
    CENTER = "center"

    @staticmethod
    def _max_min_center():
        return [Axis.MIN, Axis.MAX, Axis.CENTER]

    def _arithmetic_check(self, other):

        if not isinstance(other, (str, Axis)):
            raise TypeError("Axis name can only be concatenated with a string or Axis.")

        if self not in Axis._max_min_center():
            raise TypeError(f"Only {Axis._max_min_center()} can be concatenated.")

    def __add__(self, other):
        self._arithmetic_check(other)

        return self.name + (other if isinstance(other, str) else other.name)

    @staticmethod
    def is_axis_name_in_string(string_to_check: str) -> bool:
        """
        Used to check if min, max or center are in a string, for example "min + 2mm" -> returns True.
        """
        for word in [axis.name.lower() for axis in Axis._max_min_center()]:
            if word in string_to_check.lower():
                return True
        return False

    @staticmethod
    def from_string(axis: Union[str, float, "Axis"]):
        if isinstance(axis, Axis):
            return axis
        axis = str(axis).lower()
        if axis == "x" or axis == "0":
            return Axis.X
        if axis == "y" or axis == "1":
            return Axis.Y
        if axis == "z" or axis == "2":
            return Axis.Z
        if axis == "max":
            return Axis.MAX
        if axis == "min":
            return Axis.MIN
        if axis == "center":
            return Axis.CENTER

        assert False, f"Invalid axis {axis}"
