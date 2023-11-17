from typing import Union
import bpy
import bmesh
import mathutils

from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from codetocad import BoundaryAxis, BoundaryBox

from . import update_view_layer, get_object


def get_mesh(
    mesh_name: str,
) -> bpy.types.Mesh:
    blenderMesh = bpy.data.meshes.get(mesh_name)

    assert blenderMesh is not None, f"Mesh {mesh_name} does not exists"

    return blenderMesh


def remove_mesh(
    mesh_nameOrInstance: Union[str, bpy.types.Mesh],
):
    mesh: bpy.types.Mesh = mesh_nameOrInstance
    # if a (str) name is passed in, fetch the mesh object reference
    if isinstance(mesh_nameOrInstance, str):
        mesh = get_mesh(mesh_nameOrInstance)

    bpy.data.meshes.remove(mesh)


def set_edges_mean_crease(mesh_name: str, mean_crease_value: float):
    blenderMesh = get_mesh(mesh_name)

    for edge in blenderMesh.edges:
        edge.crease = mean_crease_value


def recalculate_normals(mesh_name: str):
    # references https://blender.stackexchange.com/a/72687

    mesh = get_mesh(mesh_name)

    bMesh = bmesh.new()
    bMesh.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bMesh, faces=bMesh.faces)
    bMesh.to_mesh(mesh)
    bMesh.clear()

    mesh.update()


# Note: transformations have to be applied for this to be reliable.
def is_collision_between_two_objects(
    object1_name: str,
    object2_name: str,
):
    update_view_layer()

    blenderObject1 = get_object(object1_name)
    blenderObject2 = get_object(object2_name)

    # References https://blender.stackexchange.com/a/144609
    bm1 = bmesh.new()
    bm2 = bmesh.new()

    bm1.from_mesh(get_mesh(blenderObject1.name))
    bm2.from_mesh(get_mesh(blenderObject2.name))

    bm1.transform(blenderObject1.matrix_world)
    bm2.transform(blenderObject2.matrix_world)

    obj_now_BVHtree = BVHTree.FromBMesh(bm1)
    obj_next_BVHtree = BVHTree.FromBMesh(bm2)

    uniqueIndecies = obj_now_BVHtree.overlap(obj_next_BVHtree)

    return len(uniqueIndecies) > 0


# References https://docs.blender.org/api/current/mathutils.kdtree.html
def create_kd_tree_for_object(
    object_name: str,
):
    blenderObject = get_object(object_name)
    mesh: bpy.types.Mesh = blenderObject.data
    size = len(mesh.vertices)
    kd = KDTree(size)

    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)

    kd.balance()
    return kd


# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def get_closest_face_to_vertex(object_name: str, vertex) -> bpy.types.MeshPolygon:
    blenderObject = get_object(object_name)

    assert (
        len(vertex) == 3
    ), "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blenderObject.matrix_world
    invertedMatrixWorld = matrixWorld.inverted()

    # vertex in object space:
    vertexInverted = invertedMatrixWorld @ mathutils.Vector(vertex)

    # polygonIndex references an index at blenderObject.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal, polygonIndex] = blenderObject.closest_point_on_mesh(
        vertexInverted
    )

    assert isFound, f"Could not find a point close to {vertex} on {object_name}"

    assert (
        polygonIndex is not None and polygonIndex != -1
    ), f"Could not find a face near {vertex} on {object_name}"

    mesh: bpy.types.Mesh = blenderObject.data
    blenderPolygon = mesh.polygons[polygonIndex]

    return blenderPolygon


# Returns a list of (co, index, dist)
def get_closest_points_to_vertex(
    object_name: str, vertex, number_of_points=2, object_kd_tree=None
):
    blenderObject = get_object(object_name)

    kdTree = object_kd_tree or create_kd_tree_for_object(object_name)

    assert (
        len(vertex) == 3
    ), "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blenderObject.matrix_world
    invertedMatrixWorld = matrixWorld.inverted()

    vertexInverted: mathutils.Vector = invertedMatrixWorld @ mathutils.Vector(
        vertex)

    return kdTree.find_n(vertexInverted, number_of_points)


# References https://blender.stackexchange.com/a/32288/138679
def get_bounding_box(
    object_name: str,
):
    update_view_layer()

    blenderObject = get_object(object_name)

    local_coords = blenderObject.bound_box[:]

    # om = blenderObject.matrix_world
    om = blenderObject.matrix_basis

    # matrix multiple world transform by all the vertices in the boundary
    coords = [(om @ mathutils.Vector(p[:])).to_tuple() for p in local_coords]
    coords = coords[::-1]
    # Coords should be a 1x8 array containing 1x3 vertices, example:
    # [(1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0)]

    # After zipping we should get
    # x (1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0)
    # y (1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0)
    # z (-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    zipped = zip("xyz", zip(*coords))

    boundingBox = BoundaryBox(None, None, None)

    for axis, _list in zipped:
        minVal = min(_list)
        maxVal = max(_list)

        setattr(boundingBox, axis, BoundaryAxis(minVal, maxVal, "m"))

    return boundingBox


def separate_object(object_name):
    bpy.ops.object.select_all(action="DESELECT")

    blenderObject = get_object(object_name)

    blenderObject.select_set(True)

    isSuccess = bpy.ops.mesh.separate(type="LOOSE") == {"FINISHED"}

    assert isSuccess is True, "Could not separate object"
