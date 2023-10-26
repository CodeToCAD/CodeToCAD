import math
import re
from typing import Union

from codetocad.enums.angle_unit import AngleUnit


class Angle:
    def to_radians(self) -> "Angle":
        return Angle(
            math.radians(self.value) if self.unit == AngleUnit.DEGREES else self.value,
            AngleUnit.RADIANS,
        )

    def to_degrees(self) -> "Angle":
        return Angle(
            math.degrees(self.value) if self.unit == AngleUnit.RADIANS else self.value,
            AngleUnit.DEGREES,
        )

    # Default unit is degrees if unit not passed
    def __init__(
        self, value: float, default_unit: AngleUnit = AngleUnit.DEGREES
    ) -> None:
        unit = (
            AngleUnit.from_string(default_unit.replace(" ", "").lower())
            if isinstance(default_unit, str)
            else default_unit
        )
        assert (unit is None and default_unit is None) or isinstance(
            unit, AngleUnit
        ), "Could not parse default unit."

        self.value = value
        self.unit = unit or AngleUnit.DEGREES

    @staticmethod
    def from_angle_or_its_float_or_string_value(
        mystery_angle: Union[str, float, "Angle"]
    ) -> "Angle":
        if isinstance(mystery_angle, Angle):
            return mystery_angle
        if isinstance(mystery_angle, (int, float)):
            return Angle(mystery_angle)
        return Angle.from_string(mystery_angle)

    def __str__(self) -> str:
        return f"{self.value}{' '+self.unit.name.lower() if self.unit else ''}"

    def __repr__(self) -> str:
        return self.__str__()

    def arithmetic_precheck_and_unit_conversion(self, other):
        if not isinstance(other, Angle):
            other = Angle.from_string(other)
        if other.unit != self.unit:
            if self.unit == AngleUnit.DEGREES:
                other.to_degrees()
            else:
                other.to_radians()
        return other

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value + other.value, self.unit)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value - other.value, self.unit)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value * other.value, self.unit)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value / other.value, self.unit)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value // other.value, self.unit)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(self.value % other.value, self.unit)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     return Angle(divmod(self.value, other.value), self.unit)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Angle(pow(self.value, other.value, mod), self.unit)

    def __abs__(self):
        return Angle(abs(self.value), self.unit)

    def __lt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value < other.value

    def __le__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value <= other.value

    def __gt__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value > other.value

    def __ge__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value >= other.value

    def __eq__(self, other):
        if other is None:
            return False
        other = self.arithmetic_precheck_and_unit_conversion(other)
        assert self.unit == other.unit, "Units are not matching for comparison."
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self):
        return Angle(self.value, self.unit)

    def copy(self):
        return self.__deepcopy__()

    # from_string: takes a string with a math operation and an optional unit of measurement
    # Default unit is degrees if unit not passed
    @staticmethod
    def from_string(
        from_string: Union[str, float, "Angle"],
        default_unit: Union[str, AngleUnit] = AngleUnit.DEGREES,
    ):
        if isinstance(from_string, Angle):
            return from_string.copy()

        unit = (
            AngleUnit.from_string(default_unit.replace(" ", "").lower())
            if isinstance(default_unit, str)
            else default_unit
        )
        assert (unit is None and default_unit is None) or isinstance(
            unit, AngleUnit
        ), "Could not parse default unit."

        if isinstance(from_string, (int, float)):
            return Angle(from_string, unit)

        assert isinstance(from_string, str), "from_string must be a string."

        from_string = from_string.replace(" ", "").lower()

        value = from_string

        assert len(value) > 0, "Angle value cannot be empty."

        # check if a unit is passed into from_string, e.g. "1rad" -> radians
        unitInString = re.search("[A-Za-z]+$", from_string)
        if unitInString:
            value = from_string[0 : -1 * len(unitInString[0])]
            unitInString = AngleUnit.from_string(unitInString[0])
            unit = unitInString or unit or AngleUnit.DEGREES

        # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
        assert re.match(
            r"[+\-*\/%\d\(\)]+", value
        ), f"Value {value} contains characters that are not allowed."

        value = eval(value)

        return Angle(value, unit)
