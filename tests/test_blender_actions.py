import unittest

from CodeToCAD import *

from mock.modeling.MockModelingProvider import resetMockModelingProvider, injectMockModelingProvider
from providers.blender.BlenderActions import *


class TestBlenderActions(unittest.TestCase):

    def setUp(self) -> None:
        # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
        resetMockModelingProvider()
        injectMockModelingProvider(globals())
        super().setUp()

    def test_todo(self):
        pass


if __name__ == "__main__":
    print("Started test_blender_actions")
    import tests.test_blender_actions
    unittest.main(tests.test_blender_actions)
    print("Completed test_blender_actions")
