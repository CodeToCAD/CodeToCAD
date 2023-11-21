from typing import List, Tuple, Optional, Union, TYPE_CHECKING
import bpy
import mathutils

from codetocad.codetocad_types import (
    DimensionOrItsFloatOrStringValue,
    PointOrListOfFloatOrItsStringValue,
)
from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from codetocad.utilities import create_uuid_like_id

from .. import blender_definitions

from . import (
    get_object,
    get_object_or_none,
    create_object,
    convert_object_using_ops,
    assign_object_to_collection,
    enable_curve_extra_objects_addon,
)


if TYPE_CHECKING:
    from .. import Vertex, Edge, Wire


def get_curve(curve_name: str) -> bpy.types.Curve:
    """
    Get a curve in Blender. Throws if the curve does not exist.
    """
    curve = bpy.data.curves.get(curve_name)

    assert curve is not None, f"Curve {curve_name} does not exists"

    return curve


def get_curve_or_none(curve_name: str) -> Optional[bpy.types.Curve]:
    """
    Get a curve in Blender. Returns non if the curve does not exist.
    """
    return bpy.data.curves.get(curve_name, None)


def set_curve_extrude_property(curve_name: str, length: Dimension):
    """
    Changes a curve's Geometry -> Extrude property.
    """
    curve = get_curve(curve_name)

    length = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
        length)

    curve.extrude = length.value


def set_curve_offset_geometry(curve_name: str, offset: Dimension):
    """
    Changes a curve's Geometry -> Offset property.
    """
    curve = get_curve(curve_name)

    length = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
        offset)

    curve.offset = length.value


def set_curve_use_path(curve_name: str, is_use_path: bool):
    curveObject = get_object(curve_name)

    curve: bpy.types.Curve = curveObject.data

    curve.use_path = is_use_path


def set_curve_resolution_u(curve_name: str, resolution: int):
    curve = get_curve(curve_name)

    curve.resolution_u = resolution


def set_curve_resolution_v(curve_name: str, resolution: int):
    curve = get_curve(curve_name)

    curve.resolution_v = resolution


def create_text(
    curve_name: str,
    text: str,
    size=Dimension(1),
    bold=False,
    italic=False,
    underlined=False,
    character_spacing=1,
    word_spacing=1,
    line_spacing=1,
    font_file_path: Optional[str] = None,
):
    curveData = bpy.data.curves.new(type="FONT", name=curve_name)

    setattr(curveData, "body", text)
    setattr(
        curveData,
        "size",
        blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            size).value,
    )
    setattr(curveData, "space_character", character_spacing)
    setattr(curveData, "space_word", word_spacing)
    setattr(curveData, "space_line", line_spacing)

    if font_file_path:
        fontData = bpy.data.fonts.load(font_file_path.replace("\\", "/"))
        setattr(curveData, "font", fontData)

    if bold or italic or underlined:
        curveDataBodyFormat = curveData.body_format
        for index in range(len(text)):
            curveDataBodyFormat[index].use_underline = underlined
            curveDataBodyFormat[index].use_bold = bold
            curveDataBodyFormat[index].use_italic = italic

        # setattr(curveData, "body_format", curveDataBodyFormat)

    create_object(curve_name, curveData)

    assign_object_to_collection(curve_name)

    # issue-160: scaling doesn't work well for TextCurves, so we'll convert it to a normal Curve.
    convert_object_using_ops(
        curve_name, blender_definitions.BlenderTypes.CURVE)

    curveData.use_path = False


def get_vertex_from_blender_point(
    spline_point: Union[
        bpy.types.BezierSplinePoint, bpy.types.SplinePoint, bpy.types.MeshVertex
    ]
) -> "Vertex":
    from .. import Vertex

    point = spline_point.co

    point = point[0:3]

    point_dimension: List[Dimension] = [
        Dimension(p, blender_definitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)
        for p in point
    ]

    return Vertex(
        location=Point.from_list(point_dimension),
        name=create_uuid_like_id(),
        native_instance=spline_point,
    )


def get_edge_from_blender_edge(
    entity: Union[bpy.types.Curve, bpy.types.Mesh],
    edge: Union[
        bpy.types.Spline,
        bpy.types.MeshEdge,
        Tuple[
            bpy.types.SplinePoint | bpy.types.BezierSplinePoint,
            bpy.types.SplinePoint | bpy.types.BezierSplinePoint,
        ],
    ],
) -> "Edge":
    from .. import Vertex, Edge

    v1: Vertex
    v2: Vertex
    if isinstance(edge, bpy.types.Spline):
        points = edge.bezier_points if edge.type == "BEZIER" else edge.points

        if len(points) > 2:
            raise Exception(
                "Edge contains more than two vertices. Did you mean to create a Wire instead of an Edge?"
            )

        v1 = get_vertex_from_blender_point(points[0])
        v2 = get_vertex_from_blender_point(points[1])
    elif isinstance(edge, tuple):
        v1 = get_vertex_from_blender_point(edge[0])
        v2 = get_vertex_from_blender_point(edge[1])
    elif isinstance(edge, bpy.types.MeshEdge) and isinstance(entity, bpy.types.Mesh):
        points = [entity.vertices[index] for index in edge.vertices]

        v1 = get_vertex_from_blender_point(points[0])
        v2 = get_vertex_from_blender_point(points[1])
    else:
        raise Exception(f"Edge type {type(edge)} is not supported.")

    return Edge(
        v1=v1,
        v2=v2,
        name=create_uuid_like_id(),
        parent_sketch=entity.name,
        native_instance=edge,
    )


def get_wire_from_blender_wire(
    entity: Union[bpy.types.Curve, bpy.types.Mesh],
    wire: Union[bpy.types.Spline, bpy.types.MeshPolygon],
) -> "Wire":
    from .. import Edge, Wire

    edges: List[Edge]
    if isinstance(wire, bpy.types.Spline):
        points = wire.bezier_points if wire.type == "BEZIER" else wire.points

        edges = [
            get_edge_from_blender_edge(
                entity=entity, edge=(points[index], points[index + 1])
            )
            for index in range(0, len(points) - 1)
        ]
    elif isinstance(wire, bpy.types.MeshPolygon) and isinstance(entity, bpy.types.Mesh):
        # references https://blender.stackexchange.com/a/6729
        all_edge_keys: List = entity.edge_keys
        wire_edge_keys: List = wire.edge_keys
        mesh_edges = entity.edges
        face_edge_map = {ek: mesh_edges[i]
                         for i, ek in enumerate(all_edge_keys)}

        edges = [
            get_edge_from_blender_edge(
                entity=entity, edge=face_edge_map[edge_key])
            for edge_key in wire_edge_keys
        ]
    else:
        raise Exception(f"Wire type {type(wire)} is not supported.")

    return Wire(
        edges=edges,
        name=create_uuid_like_id(),
        parent_sketch=entity.name,
        native_instance=wire,
    )


def get_wires_from_blender_entity(
    entity: Union[bpy.types.Curve, bpy.types.Mesh]
) -> "List[Wire]":
    from .. import Wire

    wires: List[Wire]

    if isinstance(entity, bpy.types.Curve):
        wires = [
            get_wire_from_blender_wire(entity=entity, wire=wire)
            for wire in entity.splines
        ]
    elif isinstance(entity, bpy.types.Mesh):
        wires = [
            get_wire_from_blender_wire(entity=entity, wire=wire)
            for wire in entity.polygons
        ]
    else:
        raise Exception(f"Entity type {type(entity)} is not supported.")

    return wires


def create_curve(
    curve_name: str,
    curve_type: blender_definitions.BlenderCurveTypes,
    points: List[PointOrListOfFloatOrItsStringValue],
    interpolation=64,
    is_3d=False,
    order_u: int = 2,
) -> Tuple[bpy.types.Spline, List[bpy.types.SplinePoint | bpy.types.BezierSplinePoint]]:
    curve_data = get_curve_or_none(curve_name) or bpy.data.curves.new(
        curve_name, type="CURVE"
    )
    curve_data.dimensions = "3D" if is_3d else "2D"
    curve_data.resolution_u = interpolation
    curve_data.use_path = False
    curve_data.fill_mode = "FULL" if is_3d else "BOTH"
    points_parsed: List[Point] = [
        Point.from_list_of_float_or_string(point) for point in points
    ]

    points_expanded: List[List[float]] = [
        [
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                dimension
            ).value
            for dimension in point.to_list()
        ]
        for point in points_parsed
    ]

    if get_object_or_none(curve_name) is None:
        create_object(curve_name, curve_data)

        assign_object_to_collection(curve_name)

        reference_spline = create_spline(
            blender_curve=curve_data,
            curve_type=curve_type,
            order_u=order_u,
        )

        added_points = add_points_to_spline(
            spline=reference_spline, points=points_expanded, overwrite_first_point=True
        )

        return reference_spline, added_points

    reference_spline = curve_data.splines[0]

    spline, added_points = add_points_to_curve(
        reference_spline=reference_spline,
        points=points_expanded,
    )

    merge_touching_splines(curve=curve_data)

    return spline, added_points


def clone_spline(spline_to_clone: bpy.types.Spline):
    return create_spline(
        blender_curve=spline_to_clone.id_data,
        curve_type=blender_definitions.BlenderCurveTypes[spline_to_clone.type],
        order_u=spline_to_clone.order_u,
    )


def create_spline(
    blender_curve: bpy.types.Curve,
    curve_type: blender_definitions.BlenderCurveTypes,
    order_u: int,
):
    """
    Creates a new Splines instance in the bpy.types.curves object passed in as blender_curveb then assigns the points to them.
    references https://blender.stackexchange.com/a/6751/138679
    """

    spline = blender_curve.splines.new(curve_type.name)
    spline.order_u = order_u
    # spline.use_cyclic_u = is_closed
    spline.use_endpoint_u = True

    return spline


def point_exists_in_spline(
    spline_points: bpy.types.SplinePoints | bpy.types.SplineBezierPoints,
    target_point: Point,
    tolerance=0.001,
) -> bpy.types.SplinePoint | bpy.types.BezierSplinePoint | None:
    """
    Check if a point already exists in the spline within a given tolerance.
    """
    target_vector = mathutils.Vector(target_point.to_list())
    for point in spline_points:
        if points_touching(point.co.xyz, target_vector, tolerance):
            return point
    return None


def points_touching(
    point1: mathutils.Vector, point2: mathutils.Vector, tolerance: float = 0.001
) -> bool:
    """
    Check if two points are touching within a given tolerance.
    """
    return (point1 - point2).length < tolerance


def merge_touching_splines(curve: bpy.types.Curve, tolerance: float = 0.001):
    for spline in curve.splines[1:]:
        reference_spline = curve.splines[0]

        reference_spline_points = get_spline_points(reference_spline)
        reference_first_point: mathutils.Vector = reference_spline_points[0].co
        reference_last_point: mathutils.Vector = reference_spline_points[-1].co

        spline_points = get_spline_points(spline)
        points_first_point: mathutils.Vector = spline_points[0].co
        points_last_point: mathutils.Vector = spline_points[0].co

        first_point_touching = points_touching(
            points_first_point, reference_first_point
        ) or points_touching(points_first_point, reference_last_point)
        last_point_touching = points_touching(
            points_last_point, reference_first_point
        ) or points_touching(points_last_point, reference_last_point)

        if first_point_touching or last_point_touching:
            print(f"Merging spline {spline}")
            last_reference_spline_index = len(reference_spline.points) - 1

            reference_spline_points.add(len(spline_points) - 1)
            for i, co in enumerate(spline_points):
                reference_spline_points[last_reference_spline_index + i].co = co

            curve.splines.remove(spline)


def get_spline_points(
    spline: bpy.types.Spline,
) -> bpy.types.SplineBezierPoints | bpy.types.SplinePoints:
    return spline.bezier_points if spline.type == blender_definitions.BlenderCurveTypes.BEZIER.name else spline.points


def set_spline_point(spline_points: bpy.types.SplineBezierPoints | bpy.types.SplinePoints, new_coord: List[float], index: int, curve_type: blender_definitions.BlenderCurveTypes):
    if curve_type == blender_definitions.BlenderCurveTypes.BEZIER:
        spline_points[index].co = new_coord
        spline_points[index].handle_left = new_coord
        spline_points[index].handle_right = new_coord
        spline_points[index].handle_left_type = "FREE"
        spline_points[index].handle_right_type = "FREE"
    else:
        x, y, z = new_coord
        spline_points[index].co = (x, y, z, 1)


def add_points_to_spline(
    spline: bpy.types.Spline, points: List[List[float]], overwrite_first_point: bool = False
) -> list[bpy.types.SplinePoint | bpy.types.BezierSplinePoint]:
    added_points: List[bpy.types.SplinePoint |
                       bpy.types.BezierSplinePoint] = []

    spline_points = get_spline_points(spline)

    if overwrite_first_point:
        set_spline_point(
            spline_points=spline_points,
            new_coord=points[0],
            index=0,
            curve_type=blender_definitions.BlenderCurveTypes[spline.type]
        )
        points = points[1:]
        added_points.append(spline_points[0])

    last_spline_index = len(spline_points) - 1

    for coord in points:
        last_spline_index = last_spline_index + 1
        new_point_index = last_spline_index

        spline_points.add(1)

        set_spline_point(
            spline_points=spline_points,
            new_coord=coord,
            index=new_point_index,
            curve_type=blender_definitions.BlenderCurveTypes[spline.type]
        )

        added_points.append(spline_points[new_point_index])

    return added_points


def add_points_to_curve(
    reference_spline: bpy.types.Spline,
    points: List[List[float]],
) -> Tuple[bpy.types.Spline, List[bpy.types.SplinePoint | bpy.types.BezierSplinePoint]]:
    reference_first_point = get_spline_points(reference_spline)[0]
    reference_last_point = get_spline_points(reference_spline)[-1]

    points_first_point = mathutils.Vector(points[0])
    points_last_point = mathutils.Vector(points[-1])

    first_point_touching_spline_start = points_touching(
        points_first_point, reference_first_point.co
    )
    last_point_touching_spline_start = points_touching(
        points_last_point, reference_first_point.co)
    first_point_touching_spline_end = points_touching(
        points_first_point, reference_last_point.co
    )
    last_point_touching_spline_end = points_touching(
        points_last_point, reference_last_point.co)

    spline_to_add_points_to = reference_spline

    added_points = []

    overwrite_first_point = False

    if not (first_point_touching_spline_start or last_point_touching_spline_start or first_point_touching_spline_end or last_point_touching_spline_end):
        # Create a new spline
        spline_to_add_points_to = clone_spline(reference_spline)
        overwrite_first_point = True
    else:
        if first_point_touching_spline_start or first_point_touching_spline_end:
            points = points[1:]
            added_points.append(reference_first_point)
        if last_point_touching_spline_start or last_point_touching_spline_end:
            points = points[:-1]
            added_points.append(reference_last_point)

    added_points = added_points + \
        add_points_to_spline(spline_to_add_points_to,
                             points, overwrite_first_point=overwrite_first_point)

    if first_point_touching_spline_start or last_point_touching_spline_start:
        spline_to_add_points_to.use_cyclic_u = True

    return spline_to_add_points_to, added_points


def add_bevel_object_to_curve(
    path_curve_object_name: str, profile_curve_object_name: str, fill_cap=False
):
    """
    Effectively sweeps an object along a path
    """
    pathCurveObject = get_object(path_curve_object_name)

    profileCurveObject = get_object(profile_curve_object_name)

    assert isinstance(
        profileCurveObject.data, bpy.types.Curve
    ), f"Profile Object {profile_curve_object_name} is not a Curve object. Please use a Curve object."

    curve: bpy.types.Curve = pathCurveObject.data

    curve.bevel_mode = "OBJECT"
    curve.bevel_object = profileCurveObject
    curve.use_fill_caps = fill_cap


def get_blender_curve_primitive_function(
    curve_primitive: blender_definitions.BlenderCurvePrimitiveTypes,
):
    if curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Point:
        return BlenderCurvePrimitives.create_point
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.LineTo:
        return BlenderCurvePrimitives.create_line_to
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Distance:
        return BlenderCurvePrimitives.create_line
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Angle:
        return BlenderCurvePrimitives.create_angle
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Circle:
        return BlenderCurvePrimitives.create_circle
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Ellipse:
        return BlenderCurvePrimitives.create_ellipse
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Sector:
        return BlenderCurvePrimitives.create_sector
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Segment:
        return BlenderCurvePrimitives.create_segment
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Rectangle:
        return BlenderCurvePrimitives.create_rectangle
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Rhomb:
        return BlenderCurvePrimitives.create_rhomb
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Trapezoid:
        return BlenderCurvePrimitives.create_trapezoid
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Polygon:
        return BlenderCurvePrimitives.create_polygon
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Polygon_ab:
        return BlenderCurvePrimitives.create_polygon_ab
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Arc:
        return BlenderCurvePrimitives.create_arc
    elif curve_primitive == blender_definitions.BlenderCurvePrimitiveTypes.Spiral:
        return BlenderCurvePrimitives.create_spiral

    raise TypeError("Unknown primitive")


class BlenderCurvePrimitives:
    @staticmethod
    def create_point(curve_type=blender_definitions.BlenderCurveTypes.NURBS, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Point,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_line_to(end_location, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.LineTo,
            Simple_endlocation=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(end_location)
            ).value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_line(length, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Distance,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_center=True,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_angle(length, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Angle,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_angle=Angle.from_string(angle).to_degrees().value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_circle(radius, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Circle,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_sides=64,
            **kwargs,
        )

    @staticmethod
    def create_ellipse(radius_x, radius_y, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Ellipse,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_x)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_y)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_arc(radius, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Arc,
            Simple_sides=64,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_sector(radius, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Sector,
            Simple_sides=64,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            **kwargs,
        )

    @staticmethod
    def create_segment(outter_radius, inner_radius, angle, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Segment,
            Simple_sides=64,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(outter_radius)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(inner_radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            **kwargs,
        )

    @staticmethod
    def create_rectangle(length, width, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Rectangle,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_width=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            Simple_rounded=0,
            **kwargs,
        )

    @staticmethod
    def create_rhomb(length, width, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Rhomb,
            Simple_length=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_width=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            Simple_center=True,
            **kwargs,
        )

    @staticmethod
    def create_polygon(number_of_sides, radius, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Polygon,
            Simple_sides=number_of_sides,
            Simple_radius=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_polygon_ab(number_of_sides, length, width, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Polygon_ab,
            Simple_sides=number_of_sides,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_trapezoid(length_upper, length_lower, height, **kwargs):
        create_simple_curve(
            blender_definitions.BlenderCurvePrimitiveTypes.Trapezoid,
            Simple_a=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length_upper)
            ).value,
            Simple_b=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length_lower)
            ).value,
            Simple_h=blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(height)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_spiral(
        number_of_turns: "int",
        height: DimensionOrItsFloatOrStringValue,
        radius: DimensionOrItsFloatOrStringValue,
        is_clockwise: bool = True,
        radius_end: Optional[DimensionOrItsFloatOrStringValue] = None,
        **kwargs,
    ):
        enable_curve_extra_objects_addon()

        heightMeters = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(height)
            ).value
        )

        radiusMeters = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value
        )

        radius_endMeters = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_end)
            )
            if radius_end
            else None
        )

        radiusDiff = (
            0 if radius_endMeters is None else (
                radius_endMeters - radiusMeters).value
        )

        curve_type: blender_definitions.BlenderCurveTypes = (
            kwargs["curve_type"]
            if "curve_type" in kwargs and kwargs["curve_type"]
            else blender_definitions.BlenderCurvePrimitiveTypes.Spiral.get_default_curve_type()
        )

        curve_typeName: str = curve_type.name

        bpy.ops.curve.spirals(
            spiral_type="ARCH",
            turns=number_of_turns,
            steps=24,
            edit_mode=False,
            radius=radiusMeters,
            dif_z=heightMeters / number_of_turns,
            dif_radius=radiusDiff,
            curve_type=curve_typeName,
            spiral_direction="CLOCKWISE" if is_clockwise else "COUNTER_CLOCKWISE",
        )


def create_simple_curve(
    curve_primitiveType: blender_definitions.BlenderCurvePrimitiveTypes, **kwargs
):
    """
    assumes add_curve_extra_objects is enabled
    https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
    """
    curve_type: blender_definitions.BlenderCurveTypes = (
        kwargs["curve_type"]
        if "curve_type" in kwargs and kwargs["curve_type"]
        else curve_primitiveType.get_default_curve_type()
    )

    kwargs.pop("curve_type", None)  # remove curve_type from kwargs

    enable_curve_extra_objects_addon()

    assert isinstance(
        curve_primitiveType, blender_definitions.BlenderCurvePrimitiveTypes
    ), "{} is not a known curve primitive. Options: {}".format(
        curve_primitiveType,
        [b.name for b in blender_definitions.BlenderCurvePrimitiveTypes],
    )

    assert isinstance(
        curve_type, blender_definitions.BlenderCurveTypes
    ), "{} is not a known simple curve type. Options: {}".format(
        curve_type, [b.name for b in blender_definitions.BlenderCurveTypes]
    )

    # Make sure an object or curve with the same name don't already exist:
    blenderObject = bpy.data.objects.get(curve_primitiveType.name)
    blender_curve = bpy.data.curves.get(curve_primitiveType.name)

    assert (
        blenderObject is None
    ), f"An object with name {curve_primitiveType.name} already exists."
    assert (
        blender_curve is None
    ), f"A curve with name {curve_primitiveType.name} already exists."

    # Default values:
    # bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple=True, Simple_Change=False, Simple_Delete="", Simple_Type='Point', Simple_endlocation=(2, 2, 2), Simple_a=2, Simple_b=1, Simple_h=1, Simple_angle=45, Simple_startangle=0, Simple_endangle=45, Simple_sides=3, Simple_radius=1, Simple_center=True, Simple_degrees_or_radians='Degrees', Simple_width=2, Simple_length=2, Simple_rounded=0, shape='2D', outputType='BEZIER', use_cyclic_u=True, endp_u=True, order_u=4, handleType='VECTOR', edit_mode=True)
    bpy.ops.curve.simple(
        Simple_Type=curve_primitiveType.name,
        outputType=curve_type.name,
        order_u=2,
        shape="2D",
        edit_mode=False,
        **kwargs,
    )
