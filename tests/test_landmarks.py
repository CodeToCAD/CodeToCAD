import unittest

from codetocad.enums.axis import Axis
from codetocad.enums.preset_landmark import PresetLandmark


class TestLandmarks(unittest.TestCase):
    def test_preset_landmarks(self):

        assert PresetLandmark.left.get_xyz() == (Axis.MIN, Axis.CENTER, Axis.CENTER)
        assert PresetLandmark.right.get_xyz() == (Axis.MAX, Axis.CENTER, Axis.CENTER)
        assert PresetLandmark.leftTop.get_xyz() == (Axis.MIN, Axis.CENTER, Axis.MAX)
        assert PresetLandmark.backTop.get_xyz() == (Axis.CENTER, Axis.MAX, Axis.MAX)
        assert PresetLandmark.rightBackBottom.get_xyz() == (
            Axis.MAX,
            Axis.MAX,
            Axis.MIN,
        )
        assert PresetLandmark.leftBackTop.get_xyz() == (Axis.MIN, Axis.MAX, Axis.MAX)
        assert PresetLandmark.center.get_xyz() == (
            Axis.CENTER,
            Axis.CENTER,
            Axis.CENTER,
        )
