import unittest

from CodeToCAD import *
from providers.blender.blenderProvider import injectBlenderProvider


class TestProviderCompliance(unittest.TestCase):

    def test_injectBlenderProvider(self):
        # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
        injectBlenderProvider(globals())
        Part("")
        Sketch("")
        Landmark("", "")


if __name__ == "__main__":
    print("Started test_provider_compliance")
    import tests.test_provider_compliance
    unittest.main(tests.test_provider_compliance)
    print("Completed test_provider_compliance")
