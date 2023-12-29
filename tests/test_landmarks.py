import unittest

from codetocad.enums.preset_landmark import PresetLandmark


class TestLandmarks(unittest.TestCase):
    def test_preset_landmarks(self):
        from codetocad.utilities import (
            min,
            max,
            center,
        )

        assert PresetLandmark.left.get_xyz() == (min, center, center)
        assert PresetLandmark.right.get_xyz() == (max, center, center)
        assert PresetLandmark.leftTop.get_xyz() == (min, center, max)
        assert PresetLandmark.backTop.get_xyz() == (center, max, max)
        assert PresetLandmark.rightBackBottom.get_xyz() == (max, max, min)
        assert PresetLandmark.leftBackTop.get_xyz() == (min, max, max)
        assert PresetLandmark.center.get_xyz() == (center, center, center)
