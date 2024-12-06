import bpy
import bmesh
import mathutils

from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from codetocad.core.boundary_axis import BoundaryAxis
from codetocad.core.boundary_box import BoundaryBox
from providers.blender.blender_provider.blender_actions.context import update_view_layer


def get_mesh(
    mesh_name: str,
) -> bpy.types.Mesh:
    blenderMesh = bpy.data.meshes.get(mesh_name)

    assert blenderMesh is not None, f"Mesh {mesh_name} does not exists"

    return blenderMesh


def get_mesh_for_object(blender_object: bpy.types.Object):

    if blender_object.data is None:
        raise Exception("Object does not have any data")

    return get_mesh(blender_object.data.name)


def remove_mesh(
    blender_mesh: bpy.types.Mesh,
):
    bpy.data.meshes.remove(mesh=blender_mesh)


def set_edges_mean_crease(blender_mesh: bpy.types.Mesh, mean_crease_value: float):
    for edge in blender_mesh.edges:
        edge.crease = mean_crease_value  # type: ignore


def recalculate_normals(
    blender_mesh: bpy.types.Mesh,
):
    # references https://blender.stackexchange.com/a/72687

    b_mesh = bmesh.new()
    b_mesh.from_mesh(blender_mesh)
    bmesh.ops.recalc_face_normals(b_mesh, faces=list(b_mesh.faces))
    b_mesh.to_mesh(blender_mesh)
    b_mesh.clear()

    blender_mesh.update()


# Note: transformations have to be applied for this to be reliable.
def is_collision_between_two_objects(
    blender_object1: bpy.types.Object,
    blender_object2: bpy.types.Object,
):
    update_view_layer()

    # References https://blender.stackexchange.com/a/144609
    bm1 = bmesh.new()
    bm2 = bmesh.new()

    bm1.from_mesh(get_mesh(blender_object1.name))
    bm2.from_mesh(get_mesh(blender_object2.name))

    bm1.transform(blender_object1.matrix_world)
    bm2.transform(blender_object2.matrix_world)

    obj_now_BVHtree = BVHTree.FromBMesh(bm1)
    obj_next_BVHtree = BVHTree.FromBMesh(bm2)

    uniqueIndecies = obj_now_BVHtree.overlap(obj_next_BVHtree)

    return len(uniqueIndecies) > 0


# References https://docs.blender.org/api/current/mathutils.kdtree.html
def create_kd_tree_for_object(
    blender_object: bpy.types.Object,
):
    if blender_object.data is None:
        raise Exception("Object does not have any data")

    mesh: bpy.types.Mesh = get_mesh_for_object(blender_object)

    size = len(mesh.vertices)

    kd = KDTree(size)

    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)

    kd.balance()
    return kd


# uses object.closest_point_on_mesh https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.closest_point_on_mesh
def get_closest_face_to_vertex(
    blender_object: bpy.types.Object, vertex
) -> bpy.types.MeshPolygon:

    assert (
        len(vertex) == 3
    ), "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blender_object.matrix_world
    invertedMatrixWorld = matrixWorld.inverted()

    # vertex in object space:
    vertexInverted = invertedMatrixWorld @ mathutils.Vector(vertex)

    # polygonIndex references an index at blender_object.data.polygons[polygonIndex], in other words, the face or edge data
    [isFound, closestPoint, normal, polygonIndex] = (
        blender_object.closest_point_on_mesh(vertexInverted)
    )

    assert isFound, f"Could not find a point close to {vertex} on {blender_object.name}"

    assert (
        polygonIndex is not None and polygonIndex != -1
    ), f"Could not find a face near {vertex} on {blender_object.name}"

    mesh: bpy.types.Mesh = get_mesh_for_object(blender_object)
    blenderPolygon = mesh.polygons[polygonIndex]

    return blenderPolygon


# Returns a list of (co, index, dist)
def get_closest_points_to_vertex(
    blender_object: bpy.types.Object, vertex, number_of_points=2, object_kd_tree=None
):

    kdTree = object_kd_tree or create_kd_tree_for_object(blender_object)

    assert (
        len(vertex) == 3
    ), "Vertex is not length 3. Please provide a proper vertex (x,y,z)"

    matrixWorld: mathutils.Matrix = blender_object.matrix_world
    invertedMatrixWorld = matrixWorld.inverted()

    vertexInverted: mathutils.Vector = invertedMatrixWorld @ mathutils.Vector(vertex)

    return kdTree.find_n(vertexInverted, number_of_points)


# References https://blender.stackexchange.com/a/32288/138679
def get_bounding_box(
    blender_object: bpy.types.Object,
):
    update_view_layer()

    local_coords = blender_object.bound_box[:]

    # om = blender_object.matrix_world
    om = blender_object.matrix_basis

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

    boundingBox = {}

    for axis, _list in zipped:
        minVal = min(_list)
        maxVal = max(_list)

        boundingBox[axis] = BoundaryAxis(minVal, maxVal, "m")

    return BoundaryBox(boundingBox["x"], boundingBox["y"], boundingBox["z"])


def separate_object(blender_object: bpy.types.Object):
    bpy.ops.object.select_all(action="DESELECT")

    blender_object.select_set(True)

    isSuccess = bpy.ops.mesh.separate(type="LOOSE") == {"FINISHED"}

    assert isSuccess is True, "Could not separate object"
