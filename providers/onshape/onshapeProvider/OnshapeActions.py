import codetocad.utilities as Utilities
from . import OnshapeDefinitions
from onshape_client import Client
from onshape_client.oas import (
    BTMParameterString149,
    BTMSketch151,
    BTMSketchConstraint2,
    BTMSketchCurveSegment155,
    BTMIndividualQuery138,
    BTMParameterQueryList148,
    BTMSketchPoint158,
    BTCurveGeometryLine117,
    BTMSketchCurve4,
    BTCurveGeometryCircle115,
    BTModelElementParams,
    BTFeatureDefinitionCall1406,
    BTMParameterQuantity147
)


def getOnshapeClient(config: dict) -> Client:
    return Client(configuration=config).get_client()


def getOnshapeClientWithConfigFile(configFilepath: str) -> Client:
    configAbsolutePath = Utilities.getAbsoluteFilepath(configFilepath)
    return Client(keys_file=configAbsolutePath).get_client()


def getDocumentByName(client: Client, name: str) -> dict:
    return client.documents_api.get_documents(q=name)["items"][0]


def getDocumentWorkspacesById(client: Client, documentId: str) -> list[dict]:
    return client.documents_api.get_document_workspaces(did=documentId)


def getFirstDocumentWorkspaceById(client: Client, documentId: str) -> dict:
    return getDocumentWorkspacesById(client, documentId)[0]


def getDocumentTabsById(client: Client, documentId: str, workspaceId: str) -> list[dict]:
    return client.documents_api.get_elements_in_document(did=documentId, wvmid=workspaceId, wvm="w")


def getFirstDocumentTabsById(client: Client, documentId: str, workspaceId: str) -> dict:
    return getDocumentTabsById(client, documentId, workspaceId)[0]


def getFirstDocumentUrlById(client: Client, documentId: str) -> OnshapeDefinitions.OnshapeUrl:
    workspaceId: str = getFirstDocumentWorkspaceById(client, documentId)["id"]
    tabId: str = getFirstDocumentTabsById(
        client, documentId, workspaceId)["id"]
    return OnshapeDefinitions.OnshapeUrl(documentId=documentId, workspaceId=workspaceId, tabId=tabId)


def getFirstDocumentUrlByName(client: Client, documentName: str) -> OnshapeDefinitions.OnshapeUrl:
    documentId = getDocumentByName(client, documentName)["id"]
    return getFirstDocumentUrlById(client, documentId)


def createTabPartStudios(client: Client, onshapeUrl: OnshapeDefinitions.OnshapeUrl, tabName: str) -> str:
    '''
    Create a Part Studio tab and return the newly created tab id
    '''

    partStudio = client.part_studios_api.create_part_studio(
        **onshapeUrl.dictDocumentAndWorkspace, bt_model_element_params=BTModelElementParams(name=tabName))
    return partStudio["id"]


def createSketch(client: Client, onshapeUrl: OnshapeDefinitions.OnshapeUrl, sketchName: str, btmEntities: list):
    # References https://github.com/onshape-public/onshape-clients/blob/master/python/test/test_part_studios_api.py
    PLANE_ID = "JDC"  # The plane deterministic ID for the sketch
    plane_query = BTMParameterQueryList148(
        parameter_id="sketchPlane",
        queries=[BTMIndividualQuery138(deterministic_ids=[PLANE_ID])],
    )
    sketch = BTMSketch151(
        entities=btmEntities, name=sketchName, parameters=[plane_query]
    )
    feature_definition = BTFeatureDefinitionCall1406(
        feature=sketch, bt_type="BTFeatureDefinitionCall-1406"
    )
    return client.part_studios_api.add_part_studio_feature(
        **onshapeUrl.dictDocumentAndWorkspaceAndModelAndTab,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )


def createPoint(client: Client, onshapeUrl: OnshapeDefinitions.OnshapeUrl, sketchName: str,  point: Utilities.Point):
    btmPoint = BTMSketchPoint158(
        y=point.y.value, x=point.x.value, is_user_point=True, is_construction=False, parameters=[]
    )

    return createSketch(client, onshapeUrl, sketchName=sketchName, btmEntities=[btmPoint])
