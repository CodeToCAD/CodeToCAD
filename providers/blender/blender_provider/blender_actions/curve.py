from typing import List, Sequence, Tuple, Optional, TYPE_CHECKING
import bpy
import mathutils
from mathutils import Matrix

from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.utilities import create_uuid_like_id
from providers.blender.blender_provider.blender_actions.addons import (
    enable_curve_extra_objects_addon,
)
from providers.blender.blender_provider.blender_actions.collections import (
    assign_object_to_collection,
)
from providers.blender.blender_provider.blender_actions.context import update_view_layer
from providers.blender.blender_provider.blender_actions.objects import (
    create_object,
)
from providers.blender.blender_provider.blender_actions.objects_context import (
    convert_object_using_ops,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderCurvePrimitiveTypes,
    BlenderCurveTypes,
    BlenderLength,
    BlenderObjectTypes,
)


if TYPE_CHECKING:
    from providers.blender.blender_provider.wire import Wire


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

    length = BlenderLength.convert_dimension_to_blender_unit(length)

    curve.extrude = length.value


def set_curve_offset_geometry(curve_name: str, offset: Dimension):
    """
    Changes a curve's Geometry -> Offset property.
    """
    curve = get_curve(curve_name)

    length = BlenderLength.convert_dimension_to_blender_unit(offset)

    curve.offset = length.value


def set_curve_use_path(curve_object: bpy.types.Curve, is_use_path: bool):
    curve_object.use_path = is_use_path


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
        BlenderLength.convert_dimension_to_blender_unit(size).value,
    )
    setattr(curveData, "space_character", character_spacing)
    setattr(curveData, "space_word", word_spacing)
    setattr(curveData, "space_line", line_spacing)

    if font_file_path:
        fontData = bpy.data.fonts.load(font_file_path.replace("\\", "/"))
        setattr(curveData, "font", fontData)

    if bold or italic or underlined:
        curveDataBodyFormat = curveData.body_format  # type: ignore
        for index in range(len(text)):
            curveDataBodyFormat[index].use_underline = underlined
            curveDataBodyFormat[index].use_bold = bold
            curveDataBodyFormat[index].use_italic = italic

        # setattr(curveData, "body_format", curveDataBodyFormat)

    curve_object = create_object(curve_name, curveData)
    assign_object_to_collection(curve_object)

    # issue-160: scaling doesn't work well for TextCurves, so we'll convert it to a normal Curve.
    convert_object_using_ops(curve_object, BlenderObjectTypes.CURVE)

    curveData.use_path = False

    return curveData


def create_curve(
    curve_name: str,
    curve_type: BlenderCurveTypes,
    points: Sequence[str | list[str] | list[float] | list[Dimension] | Point],
    interpolation=64,
    is_3d=False,
    order_u: int = 2,
) -> Tuple[
    bpy.types.Spline,
    bpy.types.Curve,
    List[bpy.types.SplinePoint | bpy.types.BezierSplinePoint],
]:
    """
    Create a bpy.types.curve instance if one with `curve_name` doesn't already exist, then create a spline with the points provided.
    """
    curve_data = get_curve_or_none(curve_name) or bpy.data.curves.new(
        curve_name, type="CURVE"
    )
    curve_data.dimensions = "3D" if is_3d else "2D"
    curve_data.resolution_u = interpolation
    curve_data.use_path = False
    curve_data.fill_mode = "FULL" if is_3d else "BOTH"  # type: ignore
    points_parsed: List[Point] = [
        Point.from_list_of_float_or_string(point) for point in points
    ]

    points_expanded: List = [
        [
            BlenderLength.convert_dimension_to_blender_unit(dimension).value
            for dimension in point.to_list()
        ]
        for point in points_parsed
    ]

    points_expanded = [mathutils.Vector(p) for p in points_expanded]

    if len(curve_data.splines) == 0:
        reference_spline = create_spline(
            blender_curve=curve_data,
            curve_type=curve_type,
            order_u=order_u,
        )

        added_points = add_points_to_spline(
            spline=reference_spline, points=points_expanded, overwrite_first_point=True
        )

        return reference_spline, curve_data, added_points

    reference_spline = curve_data.splines[0]

    spline, added_points = add_points_to_curve(
        reference_spline=reference_spline,
        points=points_expanded,
    )

    return spline, curve_data, added_points


def create_spline(
    blender_curve: bpy.types.Curve,
    curve_type: BlenderCurveTypes,
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
        if is_points_touching(point.co, target_vector, tolerance):
            return point
    return None


def is_points_touching(
    point1: mathutils.Vector | List[float],
    point2: mathutils.Vector | List[float],
    tolerance: float = 0.001,
) -> bool:
    """
    Check if two points are touching within a given tolerance.
    """
    point1 = mathutils.Vector(point1)
    point2 = mathutils.Vector(point2)
    return (point1.xyz - point2.xyz).length < tolerance


def merge_touching_splines(curve: bpy.types.Curve, reference_spline_index: int):
    """
    Iterates through all the splines in a curve. If any splines share the same start and end points, their points get merged into the same spline.
    """
    if reference_spline_index >= len(curve.splines) - 1:
        return

    for spline in curve.splines[reference_spline_index:]:
        reference_spline = curve.splines[reference_spline_index]

        reference_spline_points = get_spline_points(reference_spline)
        reference_first_point: mathutils.Vector = reference_spline_points[0].co
        reference_last_point: mathutils.Vector = reference_spline_points[-1].co

        spline_points = get_spline_points(spline)
        points_first_point: mathutils.Vector = spline_points[0].co
        points_last_point: mathutils.Vector = spline_points[-1].co

        first_point_touching_spline_start = is_points_touching(
            points_first_point, reference_first_point
        )
        last_point_touching_spline_start = is_points_touching(
            points_last_point, reference_first_point
        )
        first_point_touching_spline_end = is_points_touching(
            points_first_point, reference_last_point
        )
        last_point_touching_spline_end = is_points_touching(
            points_last_point, reference_last_point
        )

        if spline != reference_spline and (
            first_point_touching_spline_start
            or last_point_touching_spline_start
            or first_point_touching_spline_end
            or last_point_touching_spline_end
        ):
            add_points_to_curve(
                reference_spline=reference_spline,
                points=[point.co for point in spline_points],
            )

            curve.splines.remove(spline)

            merge_touching_splines(
                curve=curve, reference_spline_index=reference_spline_index
            )

    merge_touching_splines(
        curve=curve, reference_spline_index=reference_spline_index + 1
    )


def is_spline_cyclical(
    spline: bpy.types.Spline,
) -> bool:
    return spline.use_cyclic_u or spline.use_bezier_v


def get_spline_points(
    spline: bpy.types.Spline,
) -> bpy.types.SplineBezierPoints | bpy.types.SplinePoints:
    return (
        spline.bezier_points
        if spline.type == BlenderCurveTypes.BEZIER.name
        else spline.points
    )


def set_spline_point(
    spline_points: bpy.types.SplineBezierPoints | bpy.types.SplinePoints,
    new_coord: tuple[float, float, float],
    index: int,
):
    """
    Replace a splint point with the given coordinate.
    NOTE: this does not copy bezier control point handle data.
    """
    if isinstance(spline_points, bpy.types.SplineBezierPoints):
        spline_points[index].co = new_coord
        spline_points[index].handle_left = new_coord
        spline_points[index].handle_right = new_coord
        spline_points[index].handle_left_type = "FREE"
        spline_points[index].handle_right_type = "FREE"
    else:
        x, y, z = new_coord
        spline_points[index].co = (x, y, z, 1)


def add_points_to_spline(
    spline: bpy.types.Spline,
    points: List[mathutils.Vector],
    overwrite_first_point: bool = False,
) -> list[bpy.types.SplinePoint | bpy.types.BezierSplinePoint]:
    """
    Adds points to a specific spline
    """
    added_points: List[bpy.types.SplinePoint | bpy.types.BezierSplinePoint] = []

    spline_points = get_spline_points(spline)

    if overwrite_first_point:
        set_spline_point(
            spline_points=spline_points, new_coord=points[0].to_tuple(), index=0
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
            new_coord=coord.to_tuple(),
            index=new_point_index,
        )

        added_points.append(spline_points[new_point_index])

    return added_points


def add_points_to_curve(
    reference_spline: bpy.types.Spline,
    points: List[mathutils.Vector],
) -> Tuple[bpy.types.Spline, List[bpy.types.SplinePoint | bpy.types.BezierSplinePoint]]:
    """
    Adds points to a curve. If the points are touching the start or end points of the `reference_spline`, then the points will be appended to this spline. Otherwise, a new spline will be created and the points added to that instead.

    NOTE: You may want to call `merge_touching_splines()` after calling this function to clean up disconnected splines.
    """
    reference_first_point = get_spline_points(reference_spline)[0]
    reference_last_point = get_spline_points(reference_spline)[-1]

    points_first_point = mathutils.Vector(points[0])
    points_last_point = mathutils.Vector(points[-1])

    first_point_touching_spline_start = is_points_touching(
        points_first_point, reference_first_point.co
    )
    last_point_touching_spline_start = is_points_touching(
        points_last_point, reference_first_point.co
    )
    first_point_touching_spline_end = is_points_touching(
        points_first_point, reference_last_point.co
    )
    last_point_touching_spline_end = is_points_touching(
        points_last_point, reference_last_point.co
    )

    spline_to_add_points_to = reference_spline

    added_points = []

    overwrite_first_point = False

    if not (
        first_point_touching_spline_start
        or last_point_touching_spline_start
        or first_point_touching_spline_end
        or last_point_touching_spline_end
    ):
        # Create a new spline
        spline_to_add_points_to = create_spline(
            blender_curve=reference_spline.id_data,
            curve_type=BlenderCurveTypes[reference_spline.type],
            order_u=reference_spline.order_u,
        )
        overwrite_first_point = True
    else:
        if first_point_touching_spline_start or last_point_touching_spline_start:
            # If the first and last points of the spline are touching, then close the spline:
            spline_to_add_points_to.use_cyclic_u = True
        if first_point_touching_spline_start or first_point_touching_spline_end:
            points = points[1:]
            added_points.append(reference_first_point)
        if last_point_touching_spline_start or last_point_touching_spline_end:
            points = points[:-1]
            added_points.append(reference_last_point)

    added_points = added_points + add_points_to_spline(
        spline_to_add_points_to, points, overwrite_first_point=overwrite_first_point
    )

    return spline_to_add_points_to, added_points


def subdivide_bezier_points(
    bezier_spline: bpy.types.Spline,
    resolution: int,
    start_at_index: int = 0,
    end_at_index: int | None = None,
    is_cyclic: bool = False,
) -> list[mathutils.Vector]:
    if bezier_spline.type != "BEZIER":
        raise Exception("Spline must be a bezier spline for interpolation.")

    bezier_points = bezier_spline.bezier_points[start_at_index:end_at_index]

    poly_points: list[mathutils.Vector] = []

    for i in range(len(bezier_points) - 1):
        bp0 = bezier_points[i]
        bp1 = bezier_points[i + 1]

        co = mathutils.geometry.interpolate_bezier(
            bp0.co, bp0.handle_right, bp1.handle_left, bp1.co, resolution
        )

        poly_points += co[0:-1]

    if is_cyclic:
        bp0 = bezier_points[-1]
        bp1 = bezier_points[0]

        co = mathutils.geometry.interpolate_bezier(
            bp0.co, bp0.handle_right, bp1.handle_left, bp1.co, resolution
        )

        poly_points += co[0:-1]
    else:
        poly_points.append(co[-1])

    return poly_points


def get_vertices_from_edges(edges: list[EdgeInterface], world_matrix: Matrix):
    vertices = []
    for edge in edges:
        v1 = edge.v1.location.to_tuple_float(BlenderLength.DEFAULT_BLENDER_UNIT.value)
        v2 = edge.v2.location.to_tuple_float(BlenderLength.DEFAULT_BLENDER_UNIT.value)
        v1 = world_matrix @ mathutils.Vector(v1)
        v2 = world_matrix @ mathutils.Vector(v2)

        vertices.append(v1.to_tuple())
        vertices.append(v2.to_tuple())

    vertices = list(dict.fromkeys(vertices))

    return vertices


def get_vertices_from_bezier_curve(spline: bpy.types.Spline, world_matrix: Matrix):
    NUM_BEZIER_POINTS = 32

    vertices = []

    vertices_len = len(spline.bezier_points)
    resolution = int(NUM_BEZIER_POINTS / vertices_len) - 3
    if resolution < 2:
        resolution = 2
    end_index = (
        None
        if NUM_BEZIER_POINTS - vertices_len > vertices_len
        else NUM_BEZIER_POINTS - vertices_len
    )

    vertices = subdivide_bezier_points(
        spline, 2 + resolution, end_at_index=end_index, is_cyclic=(not end_index)
    )

    vertices = [world_matrix @ point for point in vertices]

    vertices_len = len(vertices)

    return vertices


def custom_codetocad_loft(
    wire_1: "WireInterface", wire_2: "WireInterface"
) -> bpy.types.Mesh:
    """
    This is a loft implemented in CodeToCAD. Mileage may vary.
    """
    update_view_layer()

    name = create_uuid_like_id()

    mesh = bpy.data.meshes.new(name=name)

    blender_object = create_object(name, mesh)
    assign_object_to_collection(blender_object)

    wire_1_world_matrix = Matrix.Identity(3)
    wire_2_world_matrix = Matrix.Identity(3)

    parent_object = wire_1.get_parent().get_native_instance()
    if isinstance(parent_object, bpy.types.Object):
        wire_1_world_matrix = parent_object.matrix_world

    parent_object = wire_2.get_parent().get_native_instance()
    if isinstance(parent_object, bpy.types.Object):
        wire_2_world_matrix = parent_object.matrix_world

    # wire_1_mesh = bpy.data.meshes.new_from_object(wire_1_parent)
    # wire_2_mesh = bpy.data.meshes.new_from_object(wire_2_parent)

    # edges_1_from_mesh = [
    #     edge
    #     for wire in get_wires_from_blender_entity(wire_1_mesh)
    #     for edge in wire.edges
    # ]
    # edges_2_from_mesh = [
    #     edge
    #     for wire in get_wires_from_blender_entity(wire_2_mesh)
    #     for edge in wire.edges
    # ]

    # wire_1_edges = edges_1_from_mesh
    # wire_2_edges = edges_2_from_mesh

    spline_1_vertices: List = []
    spline_2_vertices: List = []

    wire_1_edges = wire_1.edges
    wire_2_edges = wire_2.edges

    wire_1_spline = wire_1.get_native_instance()
    wire_2_spline = wire_2.get_native_instance()

    if not isinstance(wire_1_spline, bpy.types.Spline):
        raise Exception("Wire 1 is not a spline")
    if not isinstance(wire_2_spline, bpy.types.Spline):
        raise Exception("Wire 2 is not a spline")

    if wire_1_spline.type == "BEZIER":
        spline_1_vertices = get_vertices_from_bezier_curve(
            wire_1_spline, wire_1_world_matrix
        )
    else:
        spline_1_vertices = get_vertices_from_edges(wire_1_edges, wire_1_world_matrix)

    if wire_2_spline.type == "BEZIER":
        spline_2_vertices = get_vertices_from_bezier_curve(
            wire_2_spline, wire_2_world_matrix
        )
    else:
        spline_2_vertices = get_vertices_from_edges(wire_2_edges, wire_2_world_matrix)

    spline1_len = len(spline_1_vertices)
    spline2_len = len(spline_2_vertices)

    if spline1_len != spline2_len:
        raise Exception(
            "Splines don't have the same number of vertices and cannot be lofted."
        )

    spline1_edges = [(i, i + 1) for i in range(spline1_len - 1)] + [
        (0, spline1_len - 1)
    ]
    spline2_edges = [
        (i + spline1_len, i + spline1_len + 1) for i in range(spline2_len - 1)
    ] + [(spline1_len, spline1_len + spline2_len - 1)]
    spline1_2_edges = [(i, i + spline1_len) for i in range(spline1_len)]

    spline_1_faces = [tuple(range(spline1_len))]
    spline_2_faces = [tuple(range(spline1_len, spline1_len + spline2_len))]

    spline_1_2_faces = [
        (
            spline1_edges[i][1],
            spline1_2_edges[i + 1][1],
            spline2_edges[i][0],
            spline1_2_edges[i][0],
        )
        for i in range(len(spline1_2_edges) - 1)
    ] + [
        (
            spline1_edges[-1][1],
            spline1_2_edges[-1][1],
            spline2_edges[-1][0],
            spline1_2_edges[0][0],
        )
    ]

    # Create a mesh from the control points of the splines
    mesh.from_pydata(
        vertices=spline_1_vertices + spline_2_vertices,
        edges=spline1_edges + spline2_edges + spline1_2_edges,
        faces=spline_1_faces + spline_2_faces + spline_1_2_faces,
    )

    # Update the mesh
    mesh.update()

    return mesh


def add_bevel_object_to_curve(
    path_curve_blender_object: bpy.types.Object,
    profile_curve_blender_object: bpy.types.Object,
    fill_cap=False,
):
    """
    Effectively sweeps an object along a path
    """
    assert isinstance(
        profile_curve_blender_object.data, bpy.types.Curve
    ), f"Profile Object {path_curve_blender_object.name} is not a Curve object. Please use a Curve object."

    curve = path_curve_blender_object.data

    if not isinstance(curve, bpy.types.Curve):
        raise Exception("Only bpy.types.Curve type can be bevelled")

    curve.bevel_mode = "OBJECT"
    curve.bevel_object = profile_curve_blender_object
    curve.use_fill_caps = fill_cap


def get_blender_curve_primitive_function(
    curve_primitive: BlenderCurvePrimitiveTypes,
):
    if curve_primitive == BlenderCurvePrimitiveTypes.Point:
        return BlenderCurvePrimitives.create_point
    elif curve_primitive == BlenderCurvePrimitiveTypes.LineTo:
        return BlenderCurvePrimitives.create_line_to
    elif curve_primitive == BlenderCurvePrimitiveTypes.Distance:
        return BlenderCurvePrimitives.create_line
    elif curve_primitive == BlenderCurvePrimitiveTypes.Angle:
        return BlenderCurvePrimitives.create_angle
    elif curve_primitive == BlenderCurvePrimitiveTypes.Circle:
        return BlenderCurvePrimitives.create_circle
    elif curve_primitive == BlenderCurvePrimitiveTypes.Ellipse:
        return BlenderCurvePrimitives.create_ellipse
    elif curve_primitive == BlenderCurvePrimitiveTypes.Sector:
        return BlenderCurvePrimitives.create_sector
    elif curve_primitive == BlenderCurvePrimitiveTypes.Segment:
        return BlenderCurvePrimitives.create_segment
    elif curve_primitive == BlenderCurvePrimitiveTypes.Rectangle:
        return BlenderCurvePrimitives.create_rectangle
    elif curve_primitive == BlenderCurvePrimitiveTypes.Rhomb:
        return BlenderCurvePrimitives.create_rhomb
    elif curve_primitive == BlenderCurvePrimitiveTypes.Trapezoid:
        return BlenderCurvePrimitives.create_trapezoid
    elif curve_primitive == BlenderCurvePrimitiveTypes.Polygon:
        return BlenderCurvePrimitives.create_polygon
    elif curve_primitive == BlenderCurvePrimitiveTypes.Polygon_ab:
        return BlenderCurvePrimitives.create_polygon_ab
    elif curve_primitive == BlenderCurvePrimitiveTypes.Arc:
        return BlenderCurvePrimitives.create_arc
    elif curve_primitive == BlenderCurvePrimitiveTypes.Spiral:
        return BlenderCurvePrimitives.create_spiral

    raise TypeError("Unknown primitive")


class BlenderCurvePrimitives:
    @staticmethod
    def create_point(curve_type=BlenderCurveTypes.NURBS, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Point,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_line_to(end_location, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.LineTo,
            Simple_endlocation=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(end_location)
            ).value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_line(length, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Distance,
            Simple_length=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_center=True,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_angle(length, angle, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Angle,
            Simple_length=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_angle=Angle.from_string(angle).to_degrees().value,
            use_cyclic_u=False,
            **kwargs,
        )

    @staticmethod
    def create_circle(radius, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Circle,
            Simple_radius=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_sides=64,
            **kwargs,
        )

    @staticmethod
    def create_ellipse(radius_x, radius_y, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Ellipse,
            Simple_a=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_x)
            ).value,
            Simple_b=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_y)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_arc(radius, angle, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Arc,
            Simple_sides=64,
            Simple_radius=BlenderLength.convert_dimension_to_blender_unit(
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
            BlenderCurvePrimitiveTypes.Sector,
            Simple_sides=64,
            Simple_radius=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            **kwargs,
        )

    @staticmethod
    def create_segment(outter_radius, inner_radius, angle, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Segment,
            Simple_sides=64,
            Simple_a=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(outter_radius)
            ).value,
            Simple_b=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(inner_radius)
            ).value,
            Simple_startangle=0,
            Simple_endangle=Angle.from_string(angle).to_degrees().value,
            **kwargs,
        )

    @staticmethod
    def create_rectangle(length, width, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Rectangle,
            Simple_length=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_width=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            Simple_rounded=0,
            **kwargs,
        )

    @staticmethod
    def create_rhomb(length, width, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Rhomb,
            Simple_length=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_width=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            Simple_center=True,
            **kwargs,
        )

    @staticmethod
    def create_polygon(number_of_sides, radius, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Polygon,
            Simple_sides=number_of_sides,
            Simple_radius=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_polygon_ab(number_of_sides, length, width, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Polygon_ab,
            Simple_sides=number_of_sides,
            Simple_a=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length)
            ).value,
            Simple_b=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(width)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_trapezoid(length_upper, length_lower, height, **kwargs):
        create_simple_curve(
            BlenderCurvePrimitiveTypes.Trapezoid,
            Simple_a=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length_upper)
            ).value,
            Simple_b=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(length_lower)
            ).value,
            Simple_h=BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(height)
            ).value,
            **kwargs,
        )

    @staticmethod
    def create_spiral(
        number_of_turns: "int",
        height: str | float | Dimension,
        radius: str | float | Dimension,
        is_clockwise: bool = True,
        radius_end: Optional[str | float | Dimension] = None,
        **kwargs,
    ):
        enable_curve_extra_objects_addon()

        heightMeters = BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(height)
        ).value

        radiusMeters = BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_string(radius)
        ).value

        radius_endMeters = (
            BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(radius_end)
            )
            if radius_end
            else None
        )

        radiusDiff = (
            0 if radius_endMeters is None else (radius_endMeters - radiusMeters).value
        )

        curve_type: BlenderCurveTypes = (
            kwargs["curve_type"]
            if "curve_type" in kwargs and kwargs["curve_type"]
            else BlenderCurvePrimitiveTypes.Spiral.get_default_curve_type()
        )

        curve_typeName: str = curve_type.name

        bpy.ops.curve.spirals(  # type: ignore
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


def create_simple_curve(curve_primitiveType: BlenderCurvePrimitiveTypes, **kwargs):
    """
    assumes add_curve_extra_objects is enabled
    https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
    """
    curve_type: BlenderCurveTypes = (
        kwargs["curve_type"]
        if "curve_type" in kwargs and kwargs["curve_type"]
        else curve_primitiveType.get_default_curve_type()
    )

    kwargs.pop("curve_type", None)  # remove curve_type from kwargs

    enable_curve_extra_objects_addon()

    assert isinstance(
        curve_primitiveType, BlenderCurvePrimitiveTypes
    ), "{} is not a known curve primitive. Options: {}".format(
        curve_primitiveType,
        [b.name for b in BlenderCurvePrimitiveTypes],
    )

    assert isinstance(
        curve_type, BlenderCurveTypes
    ), "{} is not a known simple curve type. Options: {}".format(
        curve_type, [b.name for b in BlenderCurveTypes]
    )

    # Make sure an object or curve with the same name don't already exist:
    blender_object = bpy.data.objects.get(curve_primitiveType.name)
    blender_curve = bpy.data.curves.get(curve_primitiveType.name)

    assert (
        blender_object is None
    ), f"An object with name {curve_primitiveType.name} already exists."
    assert (
        blender_curve is None
    ), f"A curve with name {curve_primitiveType.name} already exists."

    # Default values:
    # bpy.ops.curve.simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), Simple=True, Simple_Change=False, Simple_Delete="", Simple_Type='Point', Simple_endlocation=(2, 2, 2), Simple_a=2, Simple_b=1, Simple_h=1, Simple_angle=45, Simple_startangle=0, Simple_endangle=45, Simple_sides=3, Simple_radius=1, Simple_center=True, Simple_degrees_or_radians='Degrees', Simple_width=2, Simple_length=2, Simple_rounded=0, shape='2D', outputType='BEZIER', use_cyclic_u=True, endp_u=True, order_u=4, handleType='VECTOR', edit_mode=True)
    bpy.ops.curve.simple(  # type: ignore
        Simple_Type=curve_primitiveType.name,
        outputType=curve_type.name,
        order_u=2,
        shape="2D",
        edit_mode=False,
        **kwargs,
    )
