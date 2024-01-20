from onshape_client import Client
from onshape_client.oas import (
    BTFeatureDefinitionCall1406,
    BTMIndividualQuery138,
    BTMParameterQueryList148,
    BTMSketch151,
    BTMFeature134,
    BTMSketchPoint158,
    BTMParameterEnum145,
    BTMParameterQuantity147,
    BTCurveGeometryLine117,
    BTCurveGeometryCircle115,
    BTMSketchCurve4,
    BTMSketchCurveSegment155,
    BTMIndividualSketchRegionQuery140,
)
from codetocad.core.dimension import Dimension


from codetocad.core.point import Point
from providers.onshape.onshape_provider import onshape_definitions
from providers.onshape.onshape_provider.onshape_actions.tabs import get_features


def create_or_update_sketch(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    btm_entities: list,
):
    # References https://github.com/onshape-public/onshape-clients/blob/master/python/test/test_part_studios_api.py and https://onshape-public.github.io/docs/api-adv/featureaccess/#sketches
    features = get_features(client, onshape_url)
    PLANE_ID = "JDC"  # The plane deterministic ID for the sketch
    plane_query = BTMParameterQueryList148(
        parameter_id="sketchPlane",
        queries=[BTMIndividualQuery138(deterministic_ids=[PLANE_ID])],
    )
    sketch = BTMSketch151(
        entities=btm_entities,
        name=sketch_name,
        parameters=[plane_query],
    )
    feature_definition = BTFeatureDefinitionCall1406(
        feature=sketch, bt_type="BTFeatureDefinitionCall-1406"
    )

    return client.part_studios_api.add_part_studio_feature(
        **onshape_url.dict_document_and_workspace_and_model_and_tab,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )


def update_sketch(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    sketch_feature_id: str,
    btm_entities: list,
):
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

    feature_url = onshape_url.dict_document_and_workspace_and_model_and_tab
    feature_url["fid"] = sketch_feature_id

    return client.part_studios_api.update_part_studio_feature(
        **feature_url,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )


def create_point(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    point: Point,
):
    btmPoint = BTMSketchPoint158(
        y=point.y.value,
        x=point.x.value,
        is_user_point=True,
        is_construction=False,
        parameters=[],
    )

    return create_or_update_sketch(
        client, onshape_url, sketch_name=sketch_name, btm_entities=[btmPoint]
    )


def create_line(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    start_point: Point,
    end_point: Point,
):
    line_geometry1 = BTCurveGeometryLine117(
        pnt_x=start_point.x.value,
        pnt_y=start_point.y.value,
        dir_x=end_point.x.value - start_point.x.value,
        dir_y=end_point.y.value - start_point.y.value,
        bt_type="BTCurveGeometryLine-117",
    )
    line = BTMSketchCurveSegment155(
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry1,
        bt_type="BTMSketchCurveSegment-155",
    )
    return create_or_update_sketch(
        client,
        onshape_url,
        sketch_name=sketch_name,
        btm_entities=[line],
    )


def create_rect(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    corner1: Point,
    corner2: Point,
):
    # Define the sketch entities for the rectangle

    LINE_ID = "myLine"
    START = "start"
    END = "end"
    dist_x = corner2.x.value - corner1.x.value
    dist_y = corner2.y.value - corner1.y.value
    line_geometry1 = BTCurveGeometryLine117(
        pnt_x=corner1.x.value,
        pnt_y=corner1.y.value,
        dir_x=0.0,
        dir_y=dist_y,
        bt_type="BTCurveGeometryLine-117",
    )
    line1 = BTMSketchCurveSegment155(
        start_point_id=f"{LINE_ID}.{START}",
        end_point_id=f"{LINE_ID}.{END}",
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry1,
        entity_id=LINE_ID + "1",
        bt_type="BTMSketchCurveSegment-155",
    )
    line_geometry2 = BTCurveGeometryLine117(
        pnt_x=corner1.x.value,
        pnt_y=corner2.y.value,
        dir_x=dist_x,
        dir_y=0.0,
        bt_type="BTCurveGeometryLine-117",
    )
    line2 = BTMSketchCurveSegment155(
        start_point_id=f"{LINE_ID}.{START}",
        end_point_id=f"{LINE_ID}.{END}",
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry2,
        entity_id=LINE_ID + "2",
        bt_type="BTMSketchCurveSegment-155",
    )
    line_geometry3 = BTCurveGeometryLine117(
        pnt_x=corner2.x.value,
        pnt_y=corner2.y.value,
        dir_x=0.0,
        dir_y=-dist_y,
        bt_type="BTCurveGeometryLine-117",
    )
    line3 = BTMSketchCurveSegment155(
        start_point_id=f"{LINE_ID}.{START}",
        end_point_id=f"{LINE_ID}.{END}",
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry3,
        entity_id=LINE_ID + "3",
        bt_type="BTMSketchCurveSegment-155",
    )
    line_geometry4 = BTCurveGeometryLine117(
        pnt_x=corner2.x.value,
        pnt_y=corner1.y.value,
        dir_x=-dist_x,
        dir_y=0.0,
        bt_type="BTCurveGeometryLine-117",
    )
    line4 = BTMSketchCurveSegment155(
        start_point_id=f"{LINE_ID}.{START}",
        end_point_id=f"{LINE_ID}.{END}",
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry4,
        entity_id=LINE_ID + "4",
        bt_type="BTMSketchCurveSegment-155",
    )
    return create_or_update_sketch(
        client,
        onshape_url,
        sketch_name=sketch_name,
        btm_entities=[line1, line2, line3, line4],
    )


def create_circle(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    radius: float,
    center: Point = Point(Dimension(0), Dimension(0), Dimension(0)),
    clockwise: bool = False,
):
    CIRCLE_ID = "my_circle"
    circle_geometry = BTCurveGeometryCircle115(
        radius=radius,
        clockwise=clockwise,
        xcenter=center.x.value,
        ycenter=center.y.value,
        xdir=0.1,
        ydir=0.0,
    )
    circle = BTMSketchCurve4(geometry=circle_geometry, entity_id=CIRCLE_ID)

    return create_or_update_sketch(
        client, onshape_url, sketch_name, btm_entities=[circle]
    )


def create_extrude(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    feature_id: str,
    length_expression: str,
):
    # tool_body_type = BTMParameterEnum145(
    #     value="SOLID", enum_name="ToolBodyType", parameter_id="bodyType"
    # )
    operation_type = BTMParameterEnum145(
        value="NEW",
        enum_name="NewSurfaceOperationType",
        parameter_id="surfaceOperationType",
    )

    line_query = BTMParameterQueryList148(
        parameter_id="entities",
        queries=[BTMIndividualSketchRegionQuery140(feature_id=feature_id)],
    )
    length = BTMParameterQuantity147(expression=length_expression, parameter_id="depth")
    extrude_feature = BTMFeature134(
        bt_type="BTMFeature-134",
        name="My extrude",
        feature_type="extrude",
        parameters=[operation_type, line_query, length],
    )
    feature_definition = BTFeatureDefinitionCall1406(feature=extrude_feature)
    return client.part_studios_api.add_part_studio_feature(
        **onshape_url.dict_document_and_workspace_and_model_and_tab,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )
