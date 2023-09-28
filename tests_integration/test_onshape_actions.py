import os
from providers.onshape import *
from providers.onshape.onshapeProvider import *
from providers.onshape.onshapeProvider.OnshapeActions import *

from CodeToCAD import *
from CodeToCAD.utilities import Point

configPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../providers/onshape/.onshape_client_config.yaml',
)

# Note: you must create a "CodeToCAD-OnshapeActions" document to run tests that use it.
onshapeDocumentName = "CodeToCAD-OnshapeActions"


class TestOnshapeActions():

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

    def testCreatePartStudioTab(self) -> None:
        documentUrl = getFirstDocumentUrlByName(
            self.client, onshapeDocumentName)

        partStudioId = createTabPartStudios(
            self.client, documentUrl, Utilities.createUUIDLikeId())

        assert partStudioId != None

    def testCreatePoint(self) -> None:

        onshapeUrl = getFirstDocumentUrlByName(
            self.client, onshapeDocumentName)

        partStudioId = createTabPartStudios(
            self.client, onshapeUrl, Utilities.createUUIDLikeId())

        onshapeUrl.tabId = partStudioId

        pointLocation = Dimension(1.5, "m")

        createPoint(self.client, onshapeUrl, "Test Point", Point(
            pointLocation, pointLocation, pointLocation))
