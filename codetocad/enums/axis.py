from enum import Enum
from typing import Union


class Axis(Enum):
    X = 0
    Y = 1
    Z = 2

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

        assert False, f"Cannot parse axis {axis}"
