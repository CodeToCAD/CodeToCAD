import unittest
import BlenderActions

from CodeToCAD import *

from mock.modeling.MockModelingProvider import resetMockModelingProvider, injectMockModelingProvider
from providers.blender.BlenderActions import *


class TestBlenderActions(unittest.TestCase):

    def setUp(self) -> None:
        # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
        resetMockModelingProvider()
        injectMockModelingProvider(globals())
        super().setUp()

    def test_getTranslationOfObjectAOntoObjectBOffsetByObjectC(self):
        objectA = Part("A").createCube(1, 1, 1)
        objectB = Part("B").createCube(1, 1, 1)
        objectC = objectB.createLandmark("top", min, center, center)

        objectB.translateZ(5)

        translation = BlenderActions.getTranslationOfObjectAOntoObjectBOffsetByObjectC(
            objectA.name, objectB.name, objectC.getLandmarkEntityName())

        assert translation.x.value == 0.5
        assert translation.y.value == 0
        assert translation.z.value == -5.0


if __name__ == "__main__":
    print("Started test_blender_actions")
    import tests.test_blender_actions
    unittest.main(tests.test_blender_actions)
    print("Completed test_blender_actions")
