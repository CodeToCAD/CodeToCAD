import unittest

from mock.modeling.mock_modeling_provider import (
    reset_mock_modeling_provider,
    inject_mock_modeling_provider,
)


class TestBlenderActions(unittest.TestCase):
    def setUp(self) -> None:
        # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
        reset_mock_modeling_provider()
        inject_mock_modeling_provider(globals())
        super().setUp()

    def test_todo(self):
        pass
