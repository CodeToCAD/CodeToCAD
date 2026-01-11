import math
import re

class LengthExp:
    """
    Takes a string|int|float expression of a length and converts it to meters. 

    If it's int or float, it's assumed it's in meters.

    This also supports basic arithmetic operations like addition, subtraction,
    multiplication, and division with scalars.

    ```
    x = LengthExp("2mm + 1m")
    x = LengthExp("6in + 2ft")
    x = LengthExp("6m / 2")
    ```
    """

    def __init__(self, expr):
        if isinstance(expr, LengthExp):
            self._meters = expr._meters
        else:
            self._meters = self._eval(expr)

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
        return float(self._meters)

    def __add__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(self.value + other.value)

    def __sub__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(self.value - other.value)

    def __mul__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(self.value * other.value)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(self.value / other.value)
    
    def __lt__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return self.value <= other.value
    
    def __gt__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return self.value > other.value
    
    def __ge__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return self.value >= other.value
    
    def __eq__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return self.value == other.value
    
    def __ne__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return self.value != other.value
    
    def __floordiv__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(self.value // other.value)
    
    def __mod__(self, other):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(self.value % other.value)
    
    def __pow__(self, other, mod=None):
        if not isinstance(other, LengthExp):
            other = LengthExp(other)
        return LengthExp(pow(self.value, other, mod))
    
    def __abs__(self):
        return LengthExp(abs(self.value))
    
    def __round__(self, ndigits=None):
        return LengthExp(round(self.value, ndigits))
    
    def __floor__(self):
        return LengthExp(math.floor(self.value))
    
    def __ceil__(self):
        return LengthExp(math.ceil(self.value))
    
    def __trunc__(self):
        return LengthExp(math.trunc(self.value))
    
    def __copy__(self):
        return self.__deepcopy__()
    
    def __deepcopy__(self):
        return LengthExp(self.value)
    
    def copy(self):
        return self.__deepcopy__()
    
    def __float__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Length({self.value} m)"

type LengthType = "str | float | int | LengthExp"

if __name__ == "__main__":

    x = LengthExp("2mm + 1m")
    assert math.isclose(x, 1.002), f"Expected 1.002m but got {x}m"

    x = LengthExp("5in")
    assert math.isclose(x, 0.127), f"Expected 0.127m but got {x}m"

    y = LengthExp("1in")
    x = LengthExp("1mm")
    val = x * y
    assert math.isclose(val ,2.54e-5), f"Expected 0.000254m but got {val}m"