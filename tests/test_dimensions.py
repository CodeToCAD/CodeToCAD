import unittest

from codetocad.core.dimension import Dimension
from codetocad.utilities import (
    LengthUnit,
    get_dimension_list_from_string_list,
    BoundaryAxis,
    BoundaryBox,
)


class TestDimensions(unittest.TestCase):
    def test_math(self):
        assert min(Dimension(5), Dimension(3)) == Dimension(
            3
        ), "Unexpected builtin min result"
        assert max(Dimension(5), Dimension(3)) == Dimension(
            5
        ), "Unexpected builtin max result"

    def test_dimensions(self):
        try:
            dimension = Dimension.from_string("")
            assert False
        except Exception as e:
            assert str(e) == "Dimension value cannot be empty."

        try:
            dimension = Dimension.from_string("50NotAUnit")
            assert False
        except Exception as e:
            assert "Could not parse unit" in str(e)

        dimension = Dimension.from_string("50")
        assert dimension.value == 50
        assert dimension.unit is None
        dimension = Dimension.from_string("100")
        assert dimension.value == 100
        assert dimension.unit is None
        dimension = Dimension.from_string("100", LengthUnit.m)
        assert dimension.value == 100
        assert dimension.unit == LengthUnit.m
        dimension = Dimension(99, LengthUnit.m)
        assert dimension.value == 99
        assert dimension.unit == LengthUnit.m

        dimension = Dimension.from_string("100mm")
        assert dimension.value == 100
        assert dimension.unit == LengthUnit.mm
        dimension = Dimension.from_string("1m")
        assert dimension.value == 1
        assert dimension.unit == LengthUnit.m

        dimension = Dimension.from_string("1/4mm")
        assert dimension.value == 0.25
        assert dimension.unit == LengthUnit.mm
        dimension = Dimension.from_string("1-(3/4)")
        assert dimension.value == 0.25
        assert dimension.unit is None
        dimension = Dimension.from_string("1-(3/4)", LengthUnit.ft)
        assert dimension.value == 0.25
        assert dimension.unit == LengthUnit.ft

        dimensions = get_dimension_list_from_string_list("10,1")
        assert dimensions[0].value == 10 and dimensions[1].value == 1
        assert dimensions[0].unit is None and dimensions[1].unit is None
        dimensions = get_dimension_list_from_string_list("1,2,m")
        assert dimensions[0].value == 1 and dimensions[1].value == 2
        assert dimensions[0].unit == LengthUnit.m and dimensions[1].unit == LengthUnit.m
        dimensions = get_dimension_list_from_string_list("1,2,3,m")
        assert (
            dimensions[0].value == 1
            and dimensions[1].value == 2
            and dimensions[2].value == 3
        )
        assert (
            dimensions[0].unit == LengthUnit.m
            and dimensions[1].unit == LengthUnit.m
            and dimensions[2].unit == LengthUnit.m
        )
        dimensions = get_dimension_list_from_string_list("1m,2m,3m")
        assert (
            dimensions[0].value == 1
            and dimensions[1].value == 2
            and dimensions[2].value == 3
        )
        assert (
            dimensions[0].unit == LengthUnit.m
            and dimensions[1].unit == LengthUnit.m
            and dimensions[2].unit == LengthUnit.m
        )
        dimensions = get_dimension_list_from_string_list("1m,2in,3m")
        assert (
            dimensions[0].value == 1
            and dimensions[1].value == 2
            and dimensions[2].value == 3
        )
        assert (
            dimensions[0].unit == LengthUnit.m
            and dimensions[1].unit == LengthUnit.inch
            and dimensions[2].unit == LengthUnit.m
        )
        dimensions = get_dimension_list_from_string_list("1,2,3mm,m")
        assert (
            dimensions[0].value == 1
            and dimensions[1].value == 2
            and dimensions[2].value == 3
        )
        assert (
            dimensions[0].unit == LengthUnit.m
            and dimensions[1].unit == LengthUnit.m
            and dimensions[2].unit == LengthUnit.mm
        )
        dimensions = get_dimension_list_from_string_list("21,1/8,1/8, in")
        assert (
            dimensions[0].value == 21
            and dimensions[1].value == 0.125
            and dimensions[2].value == 0.125
        )
        assert (
            dimensions[0].unit == LengthUnit.inch
            and dimensions[1].unit == LengthUnit.inch
            and dimensions[2].unit == LengthUnit.inch
        )
        dimensions = get_dimension_list_from_string_list("3in,1mm")
        assert dimensions[0].value == 3 and dimensions[1].value == 1
        assert (
            dimensions[0].unit == LengthUnit.inch
            and dimensions[1].unit == LengthUnit.mm
        )

        assert Dimension(1, LengthUnit.m).convert_to_unit(LengthUnit.mm).value == 1000
        assert Dimension(1000, LengthUnit.mm).convert_to_unit(LengthUnit.m).value == 1

        print("test_dimensions done.")

    def test_minMaxCenter(self):
        boundingBox = BoundaryBox(
            BoundaryAxis(-1, 1, LengthUnit.m),
            BoundaryAxis(-1, 1, LengthUnit.m),
            BoundaryAxis(-1, 1, LengthUnit.m),
        )

        dimensions = get_dimension_list_from_string_list("min", boundingBox)
        assert dimensions[0].value == -1
        assert dimensions[0].unit == LengthUnit.m
        dimensions = get_dimension_list_from_string_list("max", boundingBox)
        assert dimensions[0].value == 1
        assert dimensions[0].unit == LengthUnit.m
        dimensions = get_dimension_list_from_string_list("center", boundingBox)
        assert dimensions[0].value == 0
        assert dimensions[0].unit == LengthUnit.m
        dimensions = get_dimension_list_from_string_list("min-2", boundingBox)
        assert dimensions[0].value == -3
        assert dimensions[0].unit == LengthUnit.m
        dimensions = get_dimension_list_from_string_list("min-2cm", boundingBox)
        assert dimensions[0].value == -102
        assert dimensions[0].unit == LengthUnit.cm

        print("test_minMaxCenter() done.")
