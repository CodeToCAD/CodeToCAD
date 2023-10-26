from onshape_client import Client
from onshape_client.oas import (
    BTFeatureDefinitionCall1406,
    BTMIndividualQuery138, BTModelElementParams,
    BTMParameterQueryList148,
    BTMSketch151, BTMSketchPoint158)
from codetocad.core.point import Point

import codetocad.utilities as Utilities

from . import onshape_definitions


def get_onshape_client(config: dict) -> Client:
    return Client(configuration=config).get_client()


def get_onshape_client_with_config_file(config_filepath: str) -> Client:
    configAbsolutePath = Utilities.get_absolute_filepath(config_filepath)
    return Client(keys_file=configAbsolutePath).get_client()


def get_document_by_name(client: Client, name: str) -> dict:
    return client.documents_api.get_documents(q=name)["items"][0]


def get_document_workspaces_by_id(client: Client, document_id: str) -> list[dict]:
    return client.documents_api.get_document_workspaces(did=document_id)


def get_first_document_workspace_by_id(client: Client, document_id: str) -> dict:
    return get_document_workspaces_by_id(client, document_id)[0]


def get_document_tabs_by_id(client: Client, document_id: str, workspace_id: str) -> list[dict]:
    return client.documents_api.get_elements_in_document(did=document_id, wvmid=workspace_id, wvm="w")


def get_first_document_tabs_by_id(client: Client, document_id: str, workspace_id: str) -> dict:
    return get_document_tabs_by_id(client, document_id, workspace_id)[0]


def get_first_document_url_by_id(client: Client, document_id: str) -> onshape_definitions.OnshapeUrl:
    workspace_id: str = get_first_document_workspace_by_id(client, document_id)[
        "id"]
    tab_id: str = get_first_document_tabs_by_id(
        client, document_id, workspace_id)["id"]
    return onshape_definitions.OnshapeUrl(document_id=document_id, workspace_id=workspace_id, tab_id=tab_id)


def get_first_document_url_by_name(client: Client, document_name: str) -> onshape_definitions.OnshapeUrl:
    document_id = get_document_by_name(client, document_name)["id"]
    return get_first_document_url_by_id(client, document_id)


def create_tab_part_studios(client: Client, onshape_url: onshape_definitions.OnshapeUrl, tab_name: str) -> str:
    '''
    Create a Part Studio tab and return the newly created tab id
    '''

    partStudio = client.part_studios_api.create_part_studio(
        **onshape_url.dict_document_and_workspace, bt_model_element_params=BTModelElementParams(name=tab_name))
    return partStudio["id"]


def create_sketch(client: Client, onshape_url: onshape_definitions.OnshapeUrl, sketch_name: str, btm_entities: list):
    # References https://github.com/onshape-public/onshape-clients/blob/master/python/test/test_part_studios_api.py
    PLANE_ID = "JDC"  # The plane deterministic ID for the sketch
    plane_query = BTMParameterQueryList148(
        parameter_id="sketchPlane",
        queries=[BTMIndividualQuery138(deterministic_ids=[PLANE_ID])],
    )
    sketch = BTMSketch151(
        entities=btm_entities, name=sketch_name, parameters=[plane_query]
    )
    feature_definition = BTFeatureDefinitionCall1406(
        feature=sketch, bt_type="BTFeatureDefinitionCall-1406"
    )
    return client.part_studios_api.add_part_studio_feature(
        **onshape_url.dict_document_and_workspaceAndModelAndTab,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )


def create_point(client: Client, onshape_url: onshape_definitions.OnshapeUrl, sketch_name: str,  point: Point):
    btmPoint = BTMSketchPoint158(
        y=point.y.value, x=point.x.value, is_user_point=True, is_construction=False, parameters=[]
    )

    return create_sketch(client, onshape_url, sketch_name=sketch_name, btm_entities=[btmPoint])
