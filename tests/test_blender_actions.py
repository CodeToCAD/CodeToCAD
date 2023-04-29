import unittest

from CodeToCAD import *

from mock.modeling.MockModelingProvider import resetMockModelingProvider, injectMockModelingProvider
from providers.blender.BlenderActions import *


class TestBlenderActions(unittest.TestCase):

    def test_translationProjectionFromBtoA(self):
        # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
        resetMockModelingProvider()
        injectMockModelingProvider(globals())

        a = Part("A").createCube(1, 1, 1)
        b = Part("B").createCube(1, 1, 1).translateX(10)
        b_landmark = b.createLandmark("right", max, center, center)

        print(translationProjectionFromBtoA(
            a.name, b_landmark.getLandmarkEntityName(), b.name))

        b.rotateX(90)

        print("2", translationProjectionFromBtoA(
            a.name, b_landmark.getLandmarkEntityName(), b.name))


if __name__ == "__main__":
    print("Started test_blender_actions")
    import tests.test_blender_actions
    unittest.main(tests.test_blender_actions)
    print("Completed test_blender_actions")
