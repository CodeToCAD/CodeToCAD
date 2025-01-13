from typing import Optional
from onpy import Client
import onpy.entities
import onpy.entities.protocols
import onpy.features
from onshape_client.oas import (
    BTFeatureDefinitionCall1406,
    BTMIndividualQuery138,
    BTMParameterBoolean144,
    BTMParameterQueryList148,
    BTMFeature134,
    BTMSketchPoint158,
    BTMParameterEnum145,
    BTMParameterQuantity147,
    BTCurveGeometryLine117,
    BTCurveGeometryCircle115,
    BTMSketchCurve4,
    BTMSketchCurveSegment155,
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

import onpy
from onpy import Client, Document
from onpy.api import schema
from onpy.elements.partstudio import PartStudio

# def get_onshape_client(config: dict) -> Client:
#     return Client(configuration=config).get_client()


def get_onshape_client_with_config_file(config_filepath: str) -> Client:
    configAbsolutePath = Utilities.get_absolute_filepath(config_filepath)
    import yaml

    with open(configAbsolutePath, "r") as f:
        config = yaml.safe_load(f)
        base_url = config["prod_api_keys"]["base_url"]
        secret_key = config["prod_api_keys"]["secret_key"]
        access_key = config["prod_api_keys"]["access_key"]
        default_stack = config["default_stack"]
    return Client(onshape_access_token=access_key, onshape_secret_token=secret_key)


def get_document_by_name(client: Client, name: str) -> Document:
    # return client.documents_api.get_documents(q=name)["items"][0]
    return client.get_document(name=name)


def get_document_by_id(client: Client, id: str) -> Document:
    return client.get_document(id)


# def get_document_workspaces_by_id(client: Client, document_id: str) -> schema.Workspace:
#     return client.get_document(document_id).default_workspace


def get_first_document_workspace_by_id(
    client: Client, document_id: str
) -> schema.Workspace:
    return client.get_document(document_id).default_workspace


def get_document_tabs_by_id(
    client: Client, document_id: str, workspace_id: str
) -> list[PartStudio]:
    return client.get_document(document_id).list_partstudios()


def get_first_document_tabs_by_id(
    client: Client, document_id: str, workspace_id: str
) -> PartStudio:
    return client.get_document(document_id).list_partstudios()[0]


def get_first_document_url_by_id(
    client: Client, document_id: str
) -> onshape_definitions.OnshapeUrl:
    workspace_id: str = client.get_document(document_id).default_workspace.id
    tab_id: str = client.get_document(document_id).list_partstudios()[0].id
    return onshape_definitions.OnshapeUrl(
        document_id=document_id, workspace_id=workspace_id, tab_id=tab_id
    )


def get_first_document_url_by_name(
    client: Client, document_name: str
) -> onshape_definitions.OnshapeUrl:
    document_id = client.get_document(name=document_name).id
    workspace_id: str = client.get_document(document_id).default_workspace.id
    tab_id: str = client.get_document(document_id).list_partstudios()[0].id
    return onshape_definitions.OnshapeUrl(
        document_id=document_id, workspace_id=workspace_id, tab_id=tab_id
    )


# def create_tab_part_studios(
#     client: Client, onshape_url: onshape_definitions.OnshapeUrl, tab_name: str
# ) -> str:
#     """
#     Create a Part Studio tab and return the newly created tab id
#     """


#     partStudio = client.get_document(onshape_url.document_id).add_partstudio(
#         name=tab_name,
#         workspace_id=onshape_url.workspace_id,
#         tab_id=onshape_url.tab_id,
#     )
#     return partStudio["id"]
def get_partstudio_by_name(client: Client, document_id: str, name: str):
    document = client.get_document(document_id)
    partstudio = document.get_partstudio(name=name)
    return partstudio


def get_partstudio_by_id(client: Client, document_id: str, element_id: str):
    document = client.get_document(document_id)
    partstudio = document.get_partstudio(element_id=element_id)
    return partstudio


def create_sketch(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str,
):
    document = client.get_document(onshape_url.document_id)
    partstudio = document.get_partstudio(element_id=onshape_url.tab_id)
    # now, we'll define a sketch
    sketch = partstudio.add_sketch(
        plane=partstudio.features.top_plane,  # we define the plane to draw on
        name=sketch_name,  # and we name the sketch
    )
    return sketch


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
    document = client.get_document(onshape_url.document_id)
    partstudio = document.get_partstudio(element_id=onshape_url.tab_id)
    # now, we'll define a sketch
    sketch = partstudio.add_sketch(
        plane=partstudio.features.top_plane,  # we define the plane to draw on
        name=sketch_name,  # and we name the sketch
    )
    sketch.add_corner_rectangle(
        (corner1.x.value, corner1.y.value), (corner2.x.value, corner2.y.value)
    )
    return sketch


def create_circle(
    client: Client,
    onshape_url: onshape_definitions.OnshapeUrl,
    sketch_name: str = "New Cirdle",
    radius: float = 1.0,
    center: Point = Point(Dimension(0), Dimension(0), Dimension(0)),
    clockwise: bool = False,
):
    document = client.get_document(onshape_url.document_id)
    partstudio = document.get_partstudio(element_id=onshape_url.tab_id)
    # now, we'll define a sketch
    sketch = partstudio.add_sketch(
        plane=partstudio.features.top_plane,  # we define the plane to draw on
        name=sketch_name,  # and we name the sketch
    )

    sketch.add_circle(center=(0, 0), radius=0.5)
    return sketch


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
    partstudio: PartStudio,
    sketch: onpy.features.Sketch,
    distance: float,
):
    extrude = partstudio.add_extrude(faces=sketch, distance=distance)
    return extrude


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
