from onshape_client import Client

from providers.onshape.onshape_provider import onshape_definitions
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


def get_first_tab_url_by_id(
    client: Client, document_id: str
) -> onshape_definitions.OnshapeUrl:
    workspace_id: str = get_workspaces(client, document_id)[0]["id"]
    tab_id: str = get_tabs(client, document_id, workspace_id)[0]["id"]
    return onshape_definitions.OnshapeUrl(
        document_id=document_id, workspace_id=workspace_id, tab_id=tab_id
    )


def create_tab_part_studios(
    client: Client, onshape_url: onshape_definitions.OnshapeUrl, tab_name: str
) -> str:
    """
    Create a Part Studio tab and return the newly created tab id
    """

    partStudio = client.part_studios_api.create_part_studio(
        **onshape_url.dict_document_and_workspace,
        bt_model_element_params=BTModelElementParams(name=tab_name),
    )
    return partStudio["id"]


def get_features(client: Client, onshape_url: onshape_definitions.OnshapeUrl):
    """
    Get the features in a tab (aka element).
    """
    return client.part_studios_api.get_part_studio_features(
        **onshape_url.dict_document_and_workspaceAndModelAndTab
    ).to_dict()
