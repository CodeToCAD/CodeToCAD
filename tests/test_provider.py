from mock.blender.MockBlender import injectMockBpy
from CodeToCAD import *
import unittest


def runProviderTests():
    import tests.testcases_test_provider
    unittest.main(tests.testcases_test_provider)

    pass


if __name__ == "__main__":
    print("Started test_provider")

    # We don't have a mock provider yet, so we'll use the BlenderProvider temporarily.
    from BlenderProvider import injectBlenderProvider
    injectBlenderProvider()
    injectMockBpy()

    runProviderTests()

    print("Completed test_provider")
