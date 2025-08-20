import re
from typing import TypeAlias


class LengthExpression:
    """
    Takes a string expression of a length and converts it to meters.
    This also supports basic arithmetic operations like addition, subtraction,
    multiplication, and division with scalars.

    ```
    x = Length("2mm + 1m")
    assert math.isclose(x, 1.002), f"Expected 1.002m but got {x}m"

    x = Length("5in")
    assert math.isclose(x, 0.127), f"Expected 0.127m but got {x}m"

    x = Length(f"2mm * {x}")
    assert math.isclose(x ,0.000254), f"Expected 0.000254m but got {x}m"
    ```
    """

    def __init__(self, expr):
        if isinstance(expr, LengthExpression):
            self.meters = expr.meters
        else:
            self.meters = self._eval(expr)

    def _eval(self, expr):
        expr = str(expr)

        unit_pattern = r"([\d.]+)\s*(mm|cm|m|in|ft)"
        unit_convert = {
            "mm": lambda x: x / 1000,
            "cm": lambda x: x / 100,
            "m": lambda x: x,
            "in": lambda x: x * 0.0254,
            "ft": lambda x: x * 0.3048,
        }

        while re.search(unit_pattern, expr):
            expr = re.sub(
                unit_pattern,
                lambda m: str(unit_convert[m.group(2)](float(m.group(1)))),
                expr,
            )

        return eval(expr, {"__builtins__": None}, {})

    @property
    def value(self) -> float:
        return float(self.meters)

    def __add__(self, other):
        return LengthExpression(self.meters + other.meters)

    def __sub__(self, other):
        return LengthExpression(self.meters - other.meters)

    def __mul__(self, scalar):
        return LengthExpression(self.meters * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return LengthExpression(self.meters / scalar)

    def __float__(self):
        return self.value

    def __str__(self):
        return str(self.meters)

    def __repr__(self):
        return f"Length({self.meters} m)"


LengthType: TypeAlias = str | float | int | LengthExpression
