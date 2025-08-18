import math
import pytest

from codetocad.adapters.blender import *


def test_length():
    x = Length("2mm + 1m")
    assert math.isclose(x, 1.002), f"Expected 1.002m but got {x}m"

    x = Length("5in")
    assert math.isclose(x, 0.127), f"Expected 0.127m but got {x}m"

    x = Length(f"2mm * {x}")
    assert math.isclose(x, 0.000254), f"Expected 0.000254m but got {x}m"


def test_angle():
    theta = Angle("90deg + 0.5rad")
    assert math.isclose(
        theta, 2.0708, abs_tol=0.0001
    ), f"Expected 2.0708rad but got {theta}rad"
