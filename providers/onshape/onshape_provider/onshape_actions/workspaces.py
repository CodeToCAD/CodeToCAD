from onshape_client import Client


def get_workspaces(client: Client, document_id: str) -> list[dict]:
    return client.documents_api.get_document_workspaces(did=document_id)
