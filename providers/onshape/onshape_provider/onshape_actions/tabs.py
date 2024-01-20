from onshape_client import Client

from providers.onshape.onshape_provider import onshape_definitions
from providers.onshape.onshape_provider.onshape_actions.documents import (
    get_document_by_name_or_none,
)

from providers.onshape.onshape_provider.onshape_actions.workspaces import get_workspaces

from onshape_client.oas import BTModelElementParams


def get_tabs(client: Client, document_id: str, workspace_id: str) -> list[dict]:
    return client.documents_api.get_elements_in_document(
        did=document_id, wvmid=workspace_id, wvm="w"
    )


def get_tab_by_name_or_none(
    client: Client, document_id: str, workspace_id: str, tab_name: str
) -> dict | None:
    for tab in get_tabs(client, document_id, workspace_id):
        if tab["name"] == tab_name:
            return tab
    return None


def get_tab_url_by_name(
    client: Client, document_name: str, tab_name: str, workspace_id: str | None = None
) -> onshape_definitions.OnshapeUrl:
    """
    Given a document_name and tab_name, return the onshape_definitions.OnshapeUrl with this document and tab.
    """
    document = get_document_by_name_or_none(client, document_name)
    if document is None:
        raise Exception(f"Document {document_name} does not exist")
    document_id = document["id"]

    workspace_id = workspace_id or get_workspaces(client, document_id)[0]["id"]

    tab = get_tab_by_name_or_none(client, document_id, workspace_id, tab_name)
    if tab is None:
        raise Exception(
            f"Tab {tab_name} does not exist in document {document_name} and workspace {workspace_id}"
        )
    tab_id = tab["id"]

    return onshape_definitions.OnshapeUrl(
        document_id=document_id, workspace_id=workspace_id, tab_id=tab_id
    )


def create_tab_part_studios(
    client: Client, document_id: str, workspace_id: str, tab_name: str
) -> str:
    """
    Create a Part Studio tab and return the newly created tab id
    """

    tab = client.part_studios_api.create_part_studio(
        **onshape_definitions.OnshapeUrl(
            document_id, workspace_id
        ).dict_document_and_workspace,
        bt_model_element_params=BTModelElementParams(name=tab_name),
    )
    return tab["id"]


def get_features(client: Client, onshape_url: onshape_definitions.OnshapeUrl):
    """
    Get the features in a tab (aka element).
    """
    return client.part_studios_api.get_part_studio_features(
        **onshape_url.dict_document_and_workspaceAndModelAndTab
    ).to_dict()
