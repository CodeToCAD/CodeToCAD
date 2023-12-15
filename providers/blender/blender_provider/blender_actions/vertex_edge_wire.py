from typing import List, Tuple, Union, TYPE_CHECKING
import bpy

from codetocad.core.dimension import Dimension
from codetocad.core.point import Point
from codetocad.utilities import create_uuid_like_id

from .. import blender_definitions


if TYPE_CHECKING:
    from .. import Vertex, Edge, Wire


def get_vertex_location_from_blender_point(
    spline_point: Union[
        bpy.types.BezierSplinePoint, bpy.types.SplinePoint, bpy.types.MeshVertex
    ]
) -> "Point":
    point = spline_point.co

    point = point[0:3]

    point_dimension: List[Dimension] = [
        Dimension(p, blender_definitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)
        for p in point
    ]

    return Point.from_list(point_dimension)


def get_vertex_from_blender_point(
    spline_point: Union[
        bpy.types.BezierSplinePoint, bpy.types.SplinePoint, bpy.types.MeshVertex
    ],
    edge: Union[
        bpy.types.Spline,
        bpy.types.MeshEdge,
        Tuple[
            bpy.types.SplinePoint | bpy.types.BezierSplinePoint,
            bpy.types.SplinePoint | bpy.types.BezierSplinePoint,
        ],
    ],
) -> "Vertex":
    from .. import Vertex

    return Vertex(
        location=get_vertex_location_from_blender_point(spline_point),
        name=create_uuid_like_id(),
        native_instance=spline_point,
        parent_entity=edge,
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

        v1 = get_vertex_from_blender_point(points[0], edge)
        v2 = get_vertex_from_blender_point(points[1], edge)
    elif isinstance(edge, tuple):
        v1 = get_vertex_from_blender_point(edge[0], edge)
        v2 = get_vertex_from_blender_point(edge[1], edge)
    elif isinstance(edge, bpy.types.MeshEdge) and isinstance(entity, bpy.types.Mesh):
        points = [entity.vertices[index] for index in edge.vertices]

        v1 = get_vertex_from_blender_point(points[0], edge)
        v2 = get_vertex_from_blender_point(points[1], edge)
    else:
        raise Exception(f"Edge type {type(edge)} is not supported.")

    return Edge(
        v1=v1,
        v2=v2,
        name=create_uuid_like_id(),
        parent_entity=entity.name,
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
        face_edge_map = {ek: mesh_edges[i] for i, ek in enumerate(all_edge_keys)}

        edges = [
            get_edge_from_blender_edge(entity=entity, edge=face_edge_map[edge_key])
            for edge_key in wire_edge_keys
        ]
    else:
        raise Exception(f"Wire type {type(wire)} is not supported.")

    return Wire(
        edges=edges,
        name=create_uuid_like_id(),
        parent_entity=entity.name,
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
