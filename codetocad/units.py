"""Unit types and unit-expression parsing.

Floats are interpreted as the base SI unit (meters, radians, kilograms, ...).
Strings may carry units ("2in", "10 deg") or whole expressions ("2in - 5mm"),
which are evaluated and converted to the base unit. Anything that cannot be
evaluated raises ``ValueError``.

The transient ``str | float | SomeUnit`` datatypes are denoted with a
``WithUnit`` suffix, e.g. ``LengthWithUnit`` or ``AngleWithUnit``.
"""

from __future__ import annotations

import math
import re
from typing import Union

_NUMBER_PATTERN = r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

# After unit substitution only plain arithmetic may remain.
_ALLOWED_EXPRESSION = re.compile(r"^[\d\s()+\-*/.eE]*$")


def _build_token_pattern(units: dict[str, float]) -> re.Pattern[str]:
    alternation = "|".join(
        re.escape(key) for key in sorted(units, key=len, reverse=True)
    )
    return re.compile(rf"({_NUMBER_PATTERN})\s*({alternation})?", re.IGNORECASE)


def evaluate_expression(
    expression: str, units: dict[str, float], quantity_name: str
) -> float:
    """Evaluate a unit-bearing arithmetic expression into the base unit."""
    token_pattern = _build_token_pattern(units)

    def _substitute(match: re.Match[str]) -> str:
        number, unit = match.group(1), match.group(2)
        factor = units[unit.lower()] if unit else 1.0
        return repr(float(number) * factor)

    substituted = token_pattern.sub(_substitute, expression)
    if not substituted.strip():
        raise ValueError(f"Empty {quantity_name} expression: {expression!r}")
    if not _ALLOWED_EXPRESSION.match(substituted):
        raise ValueError(
            f"Could not evaluate {quantity_name} expression: {expression!r}"
        )
    try:
        return float(eval(substituted, {"__builtins__": {}}, {}))
    except Exception as error:
        raise ValueError(
            f"Could not evaluate {quantity_name} expression: {expression!r}"
        ) from error


class SomeUnit:
    """A scalar value in a fixed base unit, supporting arithmetic with
    floats, unit strings and other instances of the same unit."""

    SYMBOL = ""

    def __init__(self, value: float):
        self.value = float(value)

    def _coerce(self, other) -> "SomeUnit":
        return type(self)(other)

    def __add__(self, other):
        return type(self)(self.value + self._coerce(other).value)

    __radd__ = __add__

    def __sub__(self, other):
        return type(self)(self.value - self._coerce(other).value)

    def __rsub__(self, other):
        return type(self)(self._coerce(other).value - self.value)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return type(self)(self.value * other)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return type(self)(self.value / other)
        if isinstance(other, (SomeUnit, str)):
            return self.value / self._coerce(other).value
        return NotImplemented

    def __neg__(self):
        return type(self)(-self.value)

    def __abs__(self):
        return type(self)(abs(self.value))

    def __float__(self):
        return self.value

    def __eq__(self, other):
        try:
            return self.value == self._coerce(other).value
        except (ValueError, TypeError):
            return NotImplemented

    def __lt__(self, other):
        return self.value < self._coerce(other).value

    def __le__(self, other):
        return self.value <= self._coerce(other).value

    def __gt__(self, other):
        return self.value > self._coerce(other).value

    def __ge__(self, other):
        return self.value >= self._coerce(other).value

    def __hash__(self):
        return hash((type(self).__name__, self.value))

    def __repr__(self):
        return f"{type(self).__name__}({self.value})"

    def __str__(self):
        return f"{self.value}{self.SYMBOL}"


LENGTH_UNITS: dict[str, float] = {
    "m": 1.0,
    "meter": 1.0,
    "meters": 1.0,
    "metre": 1.0,
    "metres": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "um": 1e-6,
    "micron": 1e-6,
    "microns": 1e-6,
    "in": 0.0254,
    "inch": 0.0254,
    "inches": 0.0254,
    '"': 0.0254,
    "ft": 0.3048,
    "foot": 0.3048,
    "feet": 0.3048,
    "'": 0.3048,
    "yd": 0.9144,
    "yard": 0.9144,
    "yards": 0.9144,
    "mi": 1609.344,
    "mile": 1609.344,
    "miles": 1609.344,
}

ANGLE_UNITS: dict[str, float] = {
    "rad": 1.0,
    "radian": 1.0,
    "radians": 1.0,
    "deg": math.pi / 180.0,
    "degree": math.pi / 180.0,
    "degrees": math.pi / 180.0,
    "°": math.pi / 180.0,
}

WEIGHT_UNITS: dict[str, float] = {
    "kg": 1.0,
    "kilogram": 1.0,
    "kilograms": 1.0,
    "g": 0.001,
    "gram": 0.001,
    "grams": 0.001,
    "mg": 1e-6,
    "lb": 0.45359237,
    "lbs": 0.45359237,
    "pound": 0.45359237,
    "pounds": 0.45359237,
    "oz": 0.028349523125,
    "ounce": 0.028349523125,
    "ounces": 0.028349523125,
}

ANGULAR_SPEED_UNITS: dict[str, float] = {
    "rad/s": 1.0,
    "rad/sec": 1.0,
    "deg/s": math.pi / 180.0,
    "deg/sec": math.pi / 180.0,
    "rpm": 2.0 * math.pi / 60.0,
    "rps": 2.0 * math.pi,
    "rev/s": 2.0 * math.pi,
    "rev/min": 2.0 * math.pi / 60.0,
}

LINEAR_SPEED_UNITS: dict[str, float] = {
    "m/s": 1.0,
    "mps": 1.0,
    "cm/s": 0.01,
    "mm/s": 0.001,
    "km/h": 1000.0 / 3600.0,
    "kph": 1000.0 / 3600.0,
    "mph": 1609.344 / 3600.0,
    "ft/s": 0.3048,
    "in/s": 0.0254,
}

DENSITY_UNITS: dict[str, float] = {
    "kg/m3": 1.0,
    "kg/m^3": 1.0,
    "g/cm3": 1000.0,
    "g/cm^3": 1000.0,
    "g/mm3": 1e6,
    "g/mm^3": 1e6,
    "lb/in3": 27679.904710203125,
    "lb/in^3": 27679.904710203125,
    "lb/ft3": 16.018463373960142,
    "lb/ft^3": 16.018463373960142,
}


class LengthMeters(SomeUnit):
    SYMBOL = "m"

    def __init__(self, value: Union[str, float, "LengthMeters"]):
        super().__init__(self.value_to_meters(value))

    @staticmethod
    def value_to_meters(value) -> float:
        if isinstance(value, SomeUnit):
            return value.value
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return evaluate_expression(value, LENGTH_UNITS, "length")
        raise ValueError(f"Cannot interpret {value!r} as a length")

    def to_millimeters(self) -> float:
        return self.value * 1000.0

    def to_inches(self) -> float:
        return self.value / 0.0254


class AngleRadians(SomeUnit):
    SYMBOL = "rad"

    def __init__(self, value: Union[str, float, "AngleRadians"]):
        super().__init__(self.value_to_radians(value))

    @staticmethod
    def value_to_radians(value) -> float:
        if isinstance(value, SomeUnit):
            return value.value
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return evaluate_expression(value, ANGLE_UNITS, "angle")
        raise ValueError(f"Cannot interpret {value!r} as an angle")

    def to_degrees(self) -> float:
        return math.degrees(self.value)


class WeightKilograms(SomeUnit):
    SYMBOL = "kg"

    def __init__(self, value: Union[str, float, "WeightKilograms"]):
        super().__init__(self.value_to_kilograms(value))

    @staticmethod
    def value_to_kilograms(value) -> float:
        if isinstance(value, SomeUnit):
            return value.value
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return evaluate_expression(value, WEIGHT_UNITS, "weight")
        raise ValueError(f"Cannot interpret {value!r} as a weight")


class DensityKilogramsPerCubicMeter(SomeUnit):
    SYMBOL = "kg/m^3"

    def __init__(self, value: Union[str, float, "DensityKilogramsPerCubicMeter"]):
        super().__init__(self.value_to_kilograms_per_cubic_meter(value))

    @staticmethod
    def value_to_kilograms_per_cubic_meter(value) -> float:
        if isinstance(value, SomeUnit):
            return value.value
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return evaluate_expression(value, DENSITY_UNITS, "density")
        raise ValueError(f"Cannot interpret {value!r} as a density")


class AngularSpeedRadiansPerSecond(SomeUnit):
    SYMBOL = "rad/s"

    def __init__(self, value: Union[str, float, "AngularSpeedRadiansPerSecond"]):
        super().__init__(self.value_to_radians_per_second(value))

    @staticmethod
    def value_to_radians_per_second(value) -> float:
        if isinstance(value, SomeUnit):
            return value.value
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return evaluate_expression(value, ANGULAR_SPEED_UNITS, "angular speed")
        raise ValueError(f"Cannot interpret {value!r} as an angular speed")

    def to_rpm(self) -> float:
        return self.value * 60.0 / (2.0 * math.pi)


class LinearSpeedMetersPerSecond(SomeUnit):
    SYMBOL = "m/s"

    def __init__(self, value: Union[str, float, "LinearSpeedMetersPerSecond"]):
        super().__init__(self.value_to_meters_per_second(value))

    @staticmethod
    def value_to_meters_per_second(value) -> float:
        if isinstance(value, SomeUnit):
            return value.value
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return evaluate_expression(value, LINEAR_SPEED_UNITS, "linear speed")
        raise ValueError(f"Cannot interpret {value!r} as a linear speed")

    def to_kilometers_per_hour(self) -> float:
        return self.value * 3600.0 / 1000.0


LengthWithUnit = Union[str, float, LengthMeters]
AngleWithUnit = Union[str, float, AngleRadians]
WeightWithUnit = Union[str, float, WeightKilograms]
DensityWithUnit = Union[str, float, DensityKilogramsPerCubicMeter]
AngularSpeedWithUnit = Union[str, float, AngularSpeedRadiansPerSecond]
LinearSpeedWithUnit = Union[str, float, LinearSpeedMetersPerSecond]
