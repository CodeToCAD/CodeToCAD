import re
from typing import Optional, Union
from codetocad.core.boundary_axis import BoundaryAxis

from codetocad.enums.length_unit import LengthUnit


class Dimension:
    def __init__(self, value: float, unit: Optional[Union[str, LengthUnit]] = None):
        assert isinstance(value, (int, float)), "Dimension value must be a number."

        unit = (
            LengthUnit.from_string(unit.replace(" ", "").lower())
            if isinstance(unit, str)
            else unit
        )
        assert unit is None or isinstance(
            unit, LengthUnit
        ), "Dimension unit must be of type LengthUnit or None."

        self.value = value
        self.unit = unit

    @staticmethod
    def from_dimension_or_its_float_or_string_value(
        mystery_dimension: Union[str, float, "Dimension"],
        boundary_axis: Optional[BoundaryAxis],
    ) -> "Dimension":
        if isinstance(mystery_dimension, Dimension):
            return mystery_dimension
        if isinstance(mystery_dimension, (int, float)):
            return Dimension(mystery_dimension)
        return Dimension.from_string(mystery_dimension, None, boundary_axis)

    def __str__(self) -> str:
        return f"{self.value}{' '+self.unit.name if self.unit else ''}"

    def __repr__(self) -> str:
        return self.__str__()

    def convert_to_unit(self, target_unit: Union[str, LengthUnit]) -> "Dimension":
        assert self.unit is not None, "Current dimension does not have a unit."
        target_unit = (
            LengthUnit.from_string(target_unit)
            if not isinstance(target_unit, LengthUnit)
            else target_unit
        )
        assert isinstance(
            target_unit, LengthUnit
        ), f"Could not convert to unit {target_unit}"

        newDimension = Dimension(
            self.value * (self.unit.value / target_unit.value), target_unit
        )
        return newDimension

    def arithmetic_precheck_and_unit_conversion(self, other) -> "Dimension":
        assert other is not None, "Right-hand value cannot be None."
        if not isinstance(other, Dimension):
            other = Dimension.from_string(other)
        if other.unit is not None and self.unit is not None and other.unit != self.unit:
            other = other.convert_to_unit(self.unit)
        return other

    def __add__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value + other.value, self.unit or other.unit)

    def __sub__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value - other.value, self.unit or other.unit)

    def __mul__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value * other.value, self.unit or other.unit)

    def __truediv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value / other.value, self.unit or other.unit)

    def __floordiv__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value // other.value, self.unit or other.unit)

    def __mod__(self, other):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(self.value % other.value, self.unit or other.unit)

    # def __divmod__(self, other):
    #     other = self.arithmetic_precheck_and_unit_conversion(other)
    #     return Dimension(divmod(self.value, other.value), self.unit)

    def __pow__(self, other, mod=None):
        other = self.arithmetic_precheck_and_unit_conversion(other)
        return Dimension(pow(self.value, other.value, mod), self.unit or other.unit)

    def __abs__(self):
        return Dimension(abs(self.value), self.unit)

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
        return Dimension(self.value, self.unit)

    def copy(self):
        return self.__deepcopy__()

    # from_string: takes a string with a math operation and an optional unit of measurement
    # Default unit is None (scale factor) if it's not passed in
    # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm"
    # boundary_axis is required if min,center,max are used

    @staticmethod
    def from_string(
        from_string: Union[str, float, "Dimension"],
        default_unit: Optional[LengthUnit] = None,
        boundary_axis: Optional[BoundaryAxis] = None,
    ):
        if isinstance(from_string, Dimension):
            return from_string.copy()

        unit = (
            LengthUnit.from_string(default_unit.replace(" ", "").lower())
            if isinstance(default_unit, str)
            else default_unit
        )
        assert (unit is None and default_unit is None) or isinstance(
            unit, LengthUnit
        ), "Could not parse default unit."

        if isinstance(from_string, (int, float)):
            return Dimension(from_string, unit)

        assert isinstance(from_string, str), "from_string must be a string."

        from_string = from_string.replace(" ", "").lower()

        value = from_string

        from codetocad.utilities import (
            get_unit_in_string,
            is_reserved_word_in_string,
            replace_min_max_center_with_respective_value,
        )

        # check if a unit is passed into from_string, e.g. "1-(3/4)cm" -> cm
        unitInString = get_unit_in_string(from_string)
        if unitInString:
            value = from_string[0 : -1 * len(unitInString)]
            unitInString = LengthUnit.from_string(unitInString)
            unit = unitInString or unit

        # if min,max,center is used, try to parse those words into their respective values.
        if is_reserved_word_in_string(value):
            assert (
                boundary_axis is not None
            ), "min,max,center keywords used, but boundary_axis is not known."
            if unit is None:
                unit = boundary_axis.unit

            assert unit, "Could not determine the unit to convert the boundary axis."

            value = replace_min_max_center_with_respective_value(
                value, boundary_axis, unit
            )

        assert len(value) > 0, "Dimension value cannot be empty."

        # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
        assert re.match(
            "[+\-*\/%\d\(\)]+", value
        ), f"Value {value} contains characters that are not allowed."

        value = eval(value)

        return Dimension(value, unit)
