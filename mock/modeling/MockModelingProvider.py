from typing import Optional
from mock.modeling.MockBlender import injectMockBpy, resetMockBpy


def injectMockModelingProvider(globalContext: Optional[dict]):

    # We don't have a mock provider yet, so we'll use the BlenderProvider temporarily.
    from BlenderProvider import injectBlenderProvider
    injectBlenderProvider(globalContext)

    injectMockBpy()


def resetMockModelingProvider():
    resetMockBpy()
