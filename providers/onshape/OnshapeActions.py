import CodeToCAD.utilities as Utilities
import OnshapeDefinitions
from onshape_client import OnshapeElement, Client


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
