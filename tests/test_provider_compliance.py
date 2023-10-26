import unittest


class TestProviderCompliance(unittest.TestCase):
    def test_blender_provider(self):
        # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
        from providers.blender.blender_provider import Part, Sketch, Landmark

        Part("")
        Sketch("")
        Landmark("", "")
