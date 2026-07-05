import math

import pytest

from codetocad import (
    AngleRadians,
    DensityKilogramsPerCubicMeter,
    LengthMeters,
    WeightKilograms,
)


def test_float_is_meters():
    assert LengthMeters(2.5).value == 2.5


def test_unit_strings():
    assert LengthMeters("2in").value == pytest.approx(0.0508)
    assert LengthMeters("5mm").value == pytest.approx(0.005)
    assert LengthMeters("2 meters").value == pytest.approx(2.0)
    assert AngleRadians("10 deg").value == pytest.approx(math.radians(10))
    assert AngleRadians("1.5").value == pytest.approx(1.5)


def test_expressions():
    assert LengthMeters("2in - 5mm").value == pytest.approx(0.0508 - 0.005)
    assert LengthMeters("(1m + 50cm) * 2").value == pytest.approx(3.0)
    assert AngleRadians("90 deg / 2").value == pytest.approx(math.pi / 4)


def test_invalid_expression_raises():
    with pytest.raises(ValueError):
        LengthMeters("2 flags")
    with pytest.raises(ValueError):
        LengthMeters("__import__('os')")
    with pytest.raises(ValueError):
        LengthMeters("")


def test_arithmetic_with_strings_and_floats():
    assert ("2mm" + LengthMeters(0.001)).value == pytest.approx(0.003)
    assert (LengthMeters("1cm") + "1cm").value == pytest.approx(0.02)
    assert (LengthMeters(2) * 0.5).value == pytest.approx(1.0)
    assert (0.5 * LengthMeters(2)).value == pytest.approx(1.0)
    assert (LengthMeters(1) - "50cm").value == pytest.approx(0.5)
    assert LengthMeters(1) / LengthMeters(2) == pytest.approx(0.5)
    assert (-LengthMeters(1)).value == -1.0


def test_comparisons():
    assert LengthMeters("1cm") == "10mm"
    assert LengthMeters("1cm") < "2cm"
    assert LengthMeters("3cm") >= "2cm"


def test_weight_and_density():
    assert WeightKilograms("500 g").value == pytest.approx(0.5)
    assert WeightKilograms("1 lb").value == pytest.approx(0.45359237)
    assert DensityKilogramsPerCubicMeter("2700 kg/m3").value == pytest.approx(2700)
    assert DensityKilogramsPerCubicMeter("1 g/cm3").value == pytest.approx(1000)
