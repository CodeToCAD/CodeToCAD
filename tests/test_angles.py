from codetocad.utilities import (
    AngleUnit,
    get_angles_from_string_list,
)

import unittest


class TestAngles(unittest.TestCase):
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
