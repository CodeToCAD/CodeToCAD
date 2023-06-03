import os
import unittest
from OnshapeActions import *

from CodeToCAD import *

configPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../providers/onshape/.onshape_client_config.yaml',
)

# Note: you must create a "CodeToCAD-OnshapeActions" document to run tests that use it.
onshapeDocumentName = "CodeToCAD-OnshapeActions"


class TestOnshapeActions(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = getOnshapeClientWithConfigFile(
            configFilepath=configPath)

        # from OnshapeProvider import injectOnshapeProvider
        # injectOnshapeProvider(globals())

    def setUp(self) -> None:
        pass

    def testReadDocumentUrlByName(self) -> None:
        documentUrl = getFirstDocumentUrlByName(
            self.client, onshapeDocumentName)

        assert documentUrl != None

        print("documentUrl", documentUrl)
