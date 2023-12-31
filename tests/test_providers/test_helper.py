from mock.modeling.mock_modeling_provider import (
    inject_mock_modeling_provider,
    reset_mock_modeling_provider,
)

from providers.blender.blender_provider import *
import unittest


def injectMockProvider():
    reset_mock_modeling_provider()
    inject_mock_modeling_provider(globals())


class TestProviderCase(unittest.TestCase):
    def setUp(self) -> None:
        injectMockProvider()
        super().setUp()
