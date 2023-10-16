import unittest
from CodeToCAD.providersSample import *

from mock.modeling.MockModelingProvider import injectMockModelingProvider, resetMockModelingProvider


def injectMockProvider():
    resetMockModelingProvider()
    injectMockModelingProvider(globals())


class TestProviderCase(unittest.TestCase):

    def setUp(self) -> None:
        injectMockProvider()
        super().setUp()
