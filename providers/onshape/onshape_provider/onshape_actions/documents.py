from onshape_client import Client


def get_document_by_name_or_none(client: Client, name: str) -> dict | None:
    clients = client.documents_api.get_documents(q=name)["items"]

    if len(clients) == 0:
        return None

    return clients[0]


def create_document(client: Client, name: str):
    return client.documents_api.create_document(name=name)
