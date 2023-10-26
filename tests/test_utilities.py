from codetocad.enums.preset_landmark import PresetLandmark
from codetocad.utilities import (
    Dimension,
    LengthUnit,
    AngleUnit,
    get_angles_from_string_list,
    get_dimension_list_from_string_list,
    BoundaryAxis,
    BoundaryBox,
    min,
    max,
    center,
)

import unittest


class TestUtilities(unittest.TestCase):
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

    def test_angles(self):
        angles = get_angles_from_string_list("10,1")
        assert angles[0].value == 10 and angles[1].value == 1
        assert (
            angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES
        )
        angles = get_angles_from_string_list("1,2,deg")
        assert angles[0].value == 1 and angles[1].value == 2
        assert (
            angles[0].unit == AngleUnit.DEGREES and angles[1].unit == AngleUnit.DEGREES
        )
        angles = get_angles_from_string_list("1,2,3,deg")
        assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
        assert (
            angles[0].unit == AngleUnit.DEGREES
            and angles[1].unit == AngleUnit.DEGREES
            and angles[2].unit == AngleUnit.DEGREES
        )
        angles = get_angles_from_string_list("1deg,2rad,3deg")
        assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
        assert (
            angles[0].unit == AngleUnit.DEGREES
            and angles[1].unit == AngleUnit.RADIANS
            and angles[2].unit == AngleUnit.DEGREES
        )
        angles = get_angles_from_string_list("1,2,3deg,rad")
        assert angles[0].value == 1 and angles[1].value == 2 and angles[2].value == 3
        assert (
            angles[0].unit == AngleUnit.RADIANS
            and angles[1].unit == AngleUnit.RADIANS
            and angles[2].unit == AngleUnit.DEGREES
        )
        angles = get_angles_from_string_list("21,1/8,1/8, degrees")
        assert (
            angles[0].value == 21
            and angles[1].value == 0.125
            and angles[2].value == 0.125
        )
        assert (
            angles[0].unit == AngleUnit.DEGREES
            and angles[1].unit == AngleUnit.DEGREES
            and angles[2].unit == AngleUnit.DEGREES
        )

        print("test_angles done")

    def test_preset_landmarks(self):
        assert PresetLandmark.left.get_xyz() == (min, center, center)
        assert PresetLandmark.right.get_xyz() == (max, center, center)
        assert PresetLandmark.leftTop.get_xyz() == (min, center, max)
        assert PresetLandmark.backTop.get_xyz() == (center, max, max)
        assert PresetLandmark.rightBackBottom.get_xyz() == (max, max, min)
        assert PresetLandmark.leftBackTop.get_xyz() == (min, max, max)
        assert PresetLandmark.center.get_xyz() == (center, center, center)
