import math
import re
from typing import TypeAlias


class Angle:
    """
    Takes a string expression of an angle and converts it to radians.
    This also supports basic arithmetic operations like addition, subtraction,
    multiplication, and division with scalars.

    ```
    theta = Angle("90deg + 0.5rad")
    assert math.isclose(theta, 2.0708, abs_tol=0.0001), f"Expected 2.0708rad but got {theta}rad"
    ```
    """

    def __init__(self, expr):
        if isinstance(expr, Angle):
            self.radians = expr.radians
        else:
            self.radians = self._eval(expr)

    def _eval(self, expr):
        expr = str(expr)

        unit_pattern = r"([\d.]+)\s*(deg|rad)"
        unit_convert = {"deg": lambda x: math.radians(x), "rad": lambda x: x}

        while re.search(unit_pattern, expr):
            expr = re.sub(
                unit_pattern,
                lambda m: str(unit_convert[m.group(2)](float(m.group(1)))),
                expr,
            )

        return eval(expr, {"__builtins__": None}, {})

    @property
    def value(self):
        return float(self.radians)

    def __add__(self, other):
        return Angle(self.radians + other.radians)

    def __sub__(self, other):
        return Angle(self.radians - other.radians)

    def __mul__(self, scalar):
        return Angle(self.radians * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Angle(self.radians / scalar)

    def __float__(self):
        return self.value

    def __str__(self):
        return str(self.radians)

    def __repr__(self):
        return f"Angle({self.radians} rad)"


AngleType: TypeAlias = "str | float | int | Angle"
