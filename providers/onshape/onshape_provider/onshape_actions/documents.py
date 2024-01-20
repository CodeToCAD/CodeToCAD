from onshape_client import Client

from providers.onshape.onshape_provider import onshape_definitions
from providers.onshape.onshape_provider.onshape_actions.tabs import (
    get_first_tab_url_by_id,
)


def get_document_by_name(client: Client, name: str) -> dict:
    return client.documents_api.get_documents(q=name)["items"][0]


def get_document_url_by_name(
    client: Client, document_name: str
) -> onshape_definitions.OnshapeUrl:
    """
    Given a document_name, return the onshape_definitions.OnshapeUrl with this document and the first tab.
    """
    document_id = get_document_by_name(client, document_name)["id"]
    return get_first_tab_url_by_id(client, document_id)
