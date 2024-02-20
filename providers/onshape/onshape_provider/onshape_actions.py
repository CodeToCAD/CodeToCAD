from typing import Optional
from onshape_client import Client
from onshape_client.oas import (
    BTFeatureDefinitionCall1406,
    BTMIndividualQuery138,
    BTMParameterBoolean144,
    BTModelElementParams,
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
    BTMSketchTextEntity1761,
    BTMParameterString149,
    BTCurveGeometryEllipse1189,
    BTFeatureScriptEvalCall2377,
)
from codetocad.core.dimension import Dimension


from codetocad.core.point import Point

import codetocad.utilities as Utilities

from . import onshape_definitions
from . import utils


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


def get_document_tabs_by_id(
    client: Client, document_id: str, workspace_id: str
) -> list[dict]:
    return client.documents_api.get_elements_in_document(
        did=document_id, wvmid=workspace_id, wvm="w"
    )


def get_first_document_tabs_by_id(
    client: Client, document_id: str, workspace_id: str
) -> dict:
    return get_document_tabs_by_id(client, document_id, workspace_id)[0]


def get_first_document_url_by_id(
    client: Client, document_id: str
) -> onshape_definitions.OnshapeUrl:
    workspace_id: str = get_first_document_workspace_by_id(client, document_id)["id"]
    tab_id: str = get_first_document_tabs_by_id(client, document_id, workspace_id)["id"]
    return onshape_definitions.OnshapeUrl(
        document_id=document_id, workspace_id=workspace_id, tab_id=tab_id
    )


def get_first_document_url_by_name(
    client: Client, document_name: str
) -> onshape_definitions.OnshapeUrl:
    document_id = get_document_by_name(client, document_name)["id"]
    return get_first_document_url_by_id(client, document_id)


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


def create_sketch(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
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

    # client.part_studios_api.update_features(**onshape_url.dict_document_and_workspaceAndModelAndTab,_preload_content=False)
    return client.part_studios_api.add_part_studio_feature(
        **onshape_url.dict_document_and_workspaceAndModelAndTab,
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

    return create_sketch(
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
        entity_id="line",
        bt_type="BTMSketchCurveSegment-155",
    )
    return create_sketch(
        client,
        onshape_url,
        sketch_name=sketch_name,
        btm_entities=[line],
    )


def create_polygon(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    point_list: list[Point],
):
    btm_entities = []
    import itertools

    point_iterator = itertools.cycle(point_list)
    point = next(point_iterator)
    next_point = next(point_iterator)
    for i in range(len(point_list)):
        line_geometry = BTCurveGeometryLine117(
            pnt_x=point.x.value,
            pnt_y=point.y.value,
            dir_x=next_point.x.value - point.x.value,
            dir_y=next_point.y.value - point.y.value,
            bt_type="BTCurveGeometryLine-117",
        )
        line = BTMSketchCurveSegment155(
            start_param=0.0,
            end_param=1.0,
            geometry=line_geometry,
            entity_id="polygon-line-" + str(i + 1),
            bt_type="BTMSketchCurveSegment-155",
        )
        btm_entities.append(line)
        point, next_point = next_point, next(point_iterator)
    return create_sketch(
        client,
        onshape_url,
        sketch_name=sketch_name,
        btm_entities=btm_entities,
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
    return create_sketch(
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
    return create_sketch(client, onshape_url, sketch_name, btm_entities=[circle])


def create_ellipse(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    minor_radius: float,
    radius: float,
    center: Point = Point(Dimension(0), Dimension(0), Dimension(0)),
    clockwise: bool = False,
):
    ellipse_geometry = BTCurveGeometryEllipse1189(
        minor_radius=minor_radius,
        radius=radius,
        clockwise=clockwise,
        xcenter=center.x.value,
        ycenter=center.y.value,
        xdir=0.1,
        ydir=0.0,
    )
    ellipse_entity = BTMSketchCurve4(geometry=ellipse_geometry, entity_id="ellipse-1")
    return create_sketch(
        client, onshape_url, sketch_name, btm_entities=[ellipse_entity]
    )


def create_arc(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    radius: float,
    start_at: Point = Point(Dimension(0), Dimension(0), Dimension(0)),
    end_at: Point = Point(Dimension(0), Dimension(0), Dimension(0)),
    flip: bool = False,
):
    center, start_angle, end_angle = utils.get_center_start_end_angle(
        (start_at.x.value, start_at.y.value), (end_at.x.value, end_at.y.value), radius
    )
    circle_geometry = BTCurveGeometryCircle115(
        radius=radius,
        clockwise=False,
        xcenter=center[0],
        ycenter=center[1],
        xdir=0.1,
        ydir=0.0,
    )
    if flip:
        start_angle, end_angle = end_angle, start_angle
    arc_entity = BTMSketchCurveSegment155(
        geometry=circle_geometry,
        start_param=start_angle,
        end_param=end_angle,
        entity_id="arc-1",
    )

    return create_sketch(client, onshape_url, sketch_name, btm_entities=[arc_entity])


def create_trapezoid(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    length_upper: float,
    length_lower: float,
    height: float,
):
    center_x = 0.0
    center_y = 0.0
    # bottom line
    line_geometry1 = BTCurveGeometryLine117(
        pnt_x=center_x - length_lower / 2,
        pnt_y=center_y,
        dir_x=length_lower,
        dir_y=0.0,
        bt_type="BTCurveGeometryLine-117",
    )
    line1 = BTMSketchCurveSegment155(
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry1,
        bt_type="BTMSketchCurveSegment-155",
        entity_id="trape_bottom",
    )
    # left side line
    line_geometry2 = BTCurveGeometryLine117(
        pnt_x=center_x - length_lower / 2,
        pnt_y=center_y,
        dir_x=length_lower / 2 - length_upper / 2,
        dir_y=height,
        bt_type="BTCurveGeometryLine-117",
    )
    line2 = BTMSketchCurveSegment155(
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry2,
        bt_type="BTMSketchCurveSegment-155",
        entity_id="trape_left",
    )
    # right side line
    line_geometry3 = BTCurveGeometryLine117(
        pnt_x=center_x + length_lower / 2,
        pnt_y=center_y,
        dir_x=length_upper / 2 - length_lower / 2,
        dir_y=height,
        bt_type="BTCurveGeometryLine-117",
    )
    line3 = BTMSketchCurveSegment155(
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry3,
        bt_type="BTMSketchCurveSegment-155",
        entity_id="trape_right",
    )
    # top line
    line_geometry4 = BTCurveGeometryLine117(
        pnt_x=center_x - length_upper / 2,
        pnt_y=center_y + height,
        dir_x=length_upper,
        dir_y=0.0,
        bt_type="BTCurveGeometryLine-117",
    )
    line4 = BTMSketchCurveSegment155(
        start_param=0.0,
        end_param=1.0,
        geometry=line_geometry4,
        bt_type="BTMSketchCurveSegment-155",
        entity_id="trape_top",
    )
    return create_sketch(
        client,
        onshape_url,
        sketch_name=sketch_name,
        btm_entities=[line1, line2, line3, line4],
    )


def create_extrude(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    feature_id: str,
    length_expression: str = "10.03*in",
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
    length = BTMParameterQuantity147(expression="10.03*in", parameter_id="depth")
    extrude_feature = BTMFeature134(
        bt_type="BTMFeature-134",
        name="My extrude",
        feature_type="extrude",
        parameters=[operation_type, line_query, length],
    )
    feature_definition = BTFeatureDefinitionCall1406(feature=extrude_feature)
    return client.part_studios_api.add_part_studio_feature(
        **onshape_url.dict_document_and_workspaceAndModelAndTab,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )


def create_spiral(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    number_of_turns: "int",
    height: Dimension,
    radius: Dimension,
    is_clockwise: bool = True,
    radius_end: Optional[Dimension] = None,
):
    import json

    # Draw Axis of Spiral
    start_point = Point(
        Dimension(0.0, "meter"), Dimension(0.0, "meter"), Dimension(0.0, "meter")
    )
    end_point = Point(
        Dimension(0.0, "inch"), Dimension(0.05, "meter"), Dimension(0.0, "inch")
    )
    sketch_info = create_line(client, onshape_url, sketch_name, start_point, end_point)
    feature_id = json.loads(sketch_info.data)["feature"]["featureId"]
    # Draw Spiral
    # Get the Axis Line from created sketch
    print("=========== Feature Id ==============", feature_id)
    bt_feature_script_eval_call_2377 = BTFeatureScriptEvalCall2377(
        script='function(context is Context, queries){{return transientQueriesToStrings(evaluateQuery(context, qGeometry(qCreatedBy(makeId("{}")), GeometryType.LINE)));}}'.format(
            feature_id
        )
    )
    feature_script_resp = client.part_studios_api.eval_feature_script(
        **onshape_url.dict_document_and_workspaceAndModelAndTab,
        bt_feature_script_eval_call_2377=bt_feature_script_eval_call_2377,
        _preload_content=False,
    )
    print(json.loads(feature_script_resp.data))
    geometry_id = json.loads(feature_script_resp.data)["result"]["message"]["value"][0][
        "message"
    ]["value"]

    axis = BTMParameterQueryList148(
        parameter_id="axis",
        queries=[BTMIndividualQuery138(deterministic_ids=[geometry_id])],
    )
    # deteremine rest parameters
    axis_type = BTMParameterEnum145(
        parameter_id="axisType", value="AXIS", enum_name="AxisType"
    )
    path_type = BTMParameterEnum145(
        parameter_id="pathType", value="TURNS", enum_name="PathType"
    )
    start_type = BTMParameterEnum145(
        parameter_id="startType", value="START_ANGLE", enum_name="StartType"
    )
    start_angle = BTMParameterQuantity147(parameter_id="startAngle", expression="0 deg")
    start_radius = BTMParameterQuantity147(
        parameter_id="startRadius", expression=str(radius)
    )
    end_type = BTMParameterEnum145(
        parameter_id="endType", value="HEIGHT", enum_name="EndType"
    )
    end_height = BTMParameterQuantity147(parameter_id="height", expression=str(height))
    end_rad_toggle = BTMParameterBoolean144(
        parameter_id="endRadToggle", value=radius_end is not None
    )
    end_radius = BTMParameterQuantity147(
        parameter_id="endRadius", expression=str(radius_end)
    )
    revolutions = BTMParameterQuantity147(
        parameter_id="revolutions", value=float(number_of_turns)
    )
    handedness = BTMParameterEnum145(
        parameter_id="handedness",
        value="CW" if is_clockwise else "CCW",
        enum_name="Direction",
    )

    spiral_feature = BTMFeature134(
        bt_type="BTMFeature-134",
        name="Helix",
        feature_type="helix",
        parameters=[
            axis,
            axis_type,
            path_type,
            start_type,
            start_angle,
            start_radius,
            end_type,
            end_height,
            *([end_rad_toggle, end_radius] if radius_end is not None else []),
            revolutions,
            handedness,
        ],
    )
    feature_definition = BTFeatureDefinitionCall1406(feature=spiral_feature)
    return client.part_studios_api.add_part_studio_feature(
        **onshape_url.dict_document_and_workspaceAndModelAndTab,
        bt_feature_definition_call_1406=feature_definition,
        _preload_content=False,
    )


def create_text(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
    text: str,
    corner1: Point,
    corner2: Point,
    font_name: str = "OpenSans-Regular.ttf",
    ascent: float = 0.2,
    bold: bool = False,
    italic: bool = False,
):
    baseline_start_x: float = corner1.x.value
    baseline_start_y: float = corner1.y.value
    baseline_direction_x: float = corner2.x.value - corner1.x.value
    baseline_direction_y: float = corner2.y.value - corner1.y.value
    if bold and italic:
        font_name.replace("Regular", "BoldItalic")
    elif bold:
        font_name.replace("Regular", "Bold")
    elif italic:
        font_name.replace("Regular", "Italic")
    font_name_param = BTMParameterString149(parameter_id="fontName", value=font_name)
    text_param = BTMParameterString149(parameter_id="text", value=text)
    text_entity = BTMSketchTextEntity1761(
        ascent=ascent,
        text=text,
        font_name=font_name,
        baseline_start_x=baseline_start_x,
        baseline_start_y=baseline_start_y,
        baseline_direction_x=baseline_direction_x,
        baseline_direction_y=baseline_direction_y,
        entity_id="text-entity",
        parameters=[font_name_param, text_param],
    )

    return create_sketch(
        client, onshape_url, sketch_name=sketch_name, btm_entities=[text_entity]
    )
