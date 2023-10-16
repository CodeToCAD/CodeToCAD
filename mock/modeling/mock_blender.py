from typing import Any, Optional, Union

import numpy as np

from mock.modeling.mock_blender_math import Matrix, Vector


class Material:
    def __init__(self, name: str) -> None:
        self.name = name


class Mesh:
    def __init__(self, name: str, verticies: list[
            'Mesh.MeshVertex']) -> None:
        self.name = name
        self.vertices: list[Mesh.MeshVertex] = verticies
        self.materials: list[Material] = []

    def copy(self) -> 'Mesh':
        copy = Mesh(self.name, self.vertices)

        global mockBpy
        mockBpy.data.meshes.meshes.append(copy)

        return copy

    def assign_vertices(self, vectors: list[Vector]):
        self.vertices = [Mesh.MeshVertex(vector) for vector in vectors]

    @property
    def bound_box(self) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
        minX, minY, minZ = np.min(
            [v.co.vector for v in self.vertices], axis=0).tolist()
        maxX, maxY, maxZ = np.max(
            [v.co.vector for v in self.vertices], axis=0).tolist()

        return ((minX, minY, minZ), (minX, minY, maxZ),  (minX, maxY, maxZ), (minX, maxY, minZ), (maxX, minY, minZ), (maxX, minY, maxZ), (maxX, maxY, maxZ),  (maxX, maxY, minZ))

    def calculate_dimensions(self, scale: Optional[Vector]) -> Vector:
        dimensions = Vector((
            np.max(
                [v.co.vector for v in self.vertices], axis=0) - np.min([v.co.vector for v in self.vertices], axis=0)
        ).tolist())
        if scale:
            dimensions *= scale
        return dimensions

    def transform(self, matrix: Matrix):
        self.vertices = [Mesh.MeshVertex(
            (v.co.to_1x4() @ matrix).to_1x3()) for v in self.vertices]

    @property
    def dimensions(self) -> Vector:
        return self.calculate_dimensions(None)

    class MeshVertex:
        def __init__(self, co: Vector) -> None:
            self.co = co


class Object:
    is_hide = False

    def __init__(self, name, default_users_collection: Optional['Collection']) -> None:
        self.name = name
        self.data: Optional[Any] = None
        self.children: list['Object'] = []
        self.parent: Optional[Object] = None
        self.matrix_world = Matrix()
        self.users_collection = [
            default_users_collection] if default_users_collection else []
        self.modifiers = Object.Modifiers()
        self.constraints = Object.Constraints()

    @property
    def location(self) -> Vector:
        return self.matrix_world.translation

    @location.setter
    def location(self, value):
        pass

    @property
    def scale(self) -> Vector:
        return self.matrix_world.scale_vector

    @scale.setter
    def scale(self, value):
        pass

    @property
    def rotation_euler(self) -> Vector:
        return Vector(self.matrix_world.rotation.to_euler())

    @rotation_euler.setter
    def rotation_euler(self, value):
        pass

    @property
    def matrix_basis(self) -> Matrix:
        return self.matrix_world

    @matrix_basis.setter
    def matrix_basis(self, value):
        pass

    @property
    def matrix_local(self) -> Matrix:
        if self.parent is None:
            return self.matrix_world
        return self.parent.matrix_world @ (1 if self.parent is None else self.parent.location - self.location)

    @property
    def bound_box(self):
        if isinstance(self.data, Mesh):
            return self.data.bound_box
        raise TypeError()

    @property
    def dimensions(self):

        if isinstance(self.data, Mesh):
            return self.data.calculate_dimensions(self.scale)

        raise TypeError()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "location":
            self.matrix_world.translate(
                __value[0], __value[1], __value[2])

            for child in self.children:
                child.matrix_world.translate(
                    __value[0], __value[1], __value[2])

        if __name == "parent":
            if __value == None:
                if hasattr(self, "parent") and self.parent:
                    self.parent.children.remove(self)
            else:
                __value.children.append(self)

        if __name == "scale":
            self.matrix_world.scale(
                __value[0], __value[1], __value[2])

        if __name == "rotation_euler":
            self.matrix_world.rotate_by_euler_angle(
                __value[0], __value[1], __value[2])

        if __name == "matrix_basis":
            # [translation, rotation, scale] = __value.to_4x4().decompose()
            # self.location = translation
            # self.rotation_euler = rotation.to_euler()
            # self.scale = scale
            self.matrix_world = __value

        super().__setattr__(__name, __value)

    def visible_get(self):
        return not self.is_hide

    def hide_set(self, is_hide):
        self.is_hide = is_hide

    def select_set(self, is_selected):
        global mockBpy
        mockBpy.data.selectedObject = self if is_selected else None

    def evaluated_get(self, dg):
        return self

    def copy(self) -> 'Object':
        global mockBpy
        copy = Object(self.name, mockBpy.context.default_user_collection)
        copy.data = self.data
        copy.children = self.children
        copy.location = self.location  # type: ignore
        copy.parent = self.parent
        copy.matrix_world = self.matrix_world
        copy.users_collection = self.users_collection

        mockBpy.data.objects.objects.append(copy)

        return copy

    class Modifiers:
        def __init__(self) -> None:
            self.modifiers = []

        def new(self, name, type):
            modifier = Object.Modifiers.Modifier(name, type)
            self.modifiers.append(modifier)
            return modifier

        def get(self, name):
            for modifier in self.modifiers:
                if modifier.name == name:
                    return modifier

        def clear(self):
            self.modifiers = []

        class Modifier:
            def __init__(self, name, type) -> None:
                self.name = name
                self.type = type

    class Constraints:
        def __init__(self) -> None:
            self.constraints = []

        def new(self, name):
            constraint = Object.Constraints.Constraint(name)
            self.constraints.append(constraint)
            return constraint

        def get(self, name):
            for constraint in self.constraints:
                if constraint.name == name:
                    return constraint

        class Constraint:
            def __init__(self, name) -> None:
                self.name = name


class Collection:
    def __init__(self, name) -> None:
        self.name = name
        self.objects = Collection.CollectionObjects(self)

    def object_belongs_to_collection(self, object: Object) -> bool:
        global mockBpy
        return self in object.users_collection

    @ property
    def linked_objects(self):
        return list(filter(self.object_belongs_to_collection, mockBpy.data.objects.objects))

    class CollectionObjects:

        def __init__(self, collection: 'Collection') -> None:
            self.collection = collection

        def unlink(self, object: Object):
            object.users_collection.remove(self.collection)

        def link(self, object: Object):
            object.users_collection.append(self.collection)


class Objects:
    def __init__(self) -> None:
        self.objects: list[Object] = []

    def get(self, name):
        for object in self.objects:
            if object.name == name:
                return object

    def remove(self, object):
        self.objects.remove(object)

    def remove_using_data(self, data):
        matching = []
        for object in self.objects:
            if object.data == data:
                matching.append(object)
        for object in matching:
            self.objects.remove(object)


class Collections:
    def __init__(self) -> None:
        self.collections: list[Collection] = []

    def get(self, name):
        for collection in self.collections:
            if collection.name == name:
                return collection


class Meshes:
    def __init__(self) -> None:
        self.meshes: list[Mesh] = []

    def get(self, name):
        for mesh in self.meshes:
            if mesh.name == name:
                return mesh

    def remove(self, mesh):
        self.meshes.remove(mesh)

        global mockBpy
        mockBpy.data.objects.remove_using_data(mesh)


class Materials:
    def __init__(self) -> None:
        self.materials: list[Material] = []

    def new(self, name):
        material = Material(name)
        self.materials.append(material)
        return material

    def get(self, name):
        for material in self.materials:
            if material.name == name:
                return material

    def remove(self, material):
        self.materials.remove(material)


class Data:

    def __init__(self) -> None:
        self.objects = Objects()
        self.meshes = Meshes()
        self.materials = Materials()
        self.collections = Collections()
        self.collections.collections.append(Collection("Scene"))

        self.selectedObject: Optional[Object] = None

    def create_mesh_object(self, object_name, mesh_name, verticies: list[Mesh.MeshVertex]):
        global mockBpy

        mesh = Mesh(mesh_name, verticies)
        obj = Object(object_name, mockBpy.context.default_user_collection)
        obj.data = mesh
        mockBpy.data.objects.objects.append(obj)
        mockBpy.data.meshes.meshes.append(mesh)


class Ops:
    def __init__(self) -> None:
        self.object = Ops.OpsObject()
        self.mesh = Ops.OpsMesh()
        self.curve = Ops.OpsCurve()
        self.export_mesh = Ops.OpsExportMesh()
        self.export_scene = Ops.OpsExportScene()
        self.wm = Ops.OpsWM()

    class OpsExportMesh:
        @ staticmethod
        def stl(
                filepath: Union[str, Any] = "",
                use_selection: Union[bool, Any] = False,
                global_scale: Optional[Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsExportScene:
        @ staticmethod
        def obj(
                filepath: Union[str, Any] = "",
                use_selection: Union[bool, Any] = False,
                global_scale: Optional[Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsWM:
        @ staticmethod
        def obj_export(
                filepath: Union[str, Any] = "",
                export_selected_objects: Union[bool,
                                               Any] = False,
                global_scale: Optional[Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsObject:
        @ staticmethod
        def empty_add(radius, **keywordArguments):
            global mockBpy
            mockBpy.data.objects.objects.append(
                Object("Empty", mockBpy.context.default_user_collection))

        @ staticmethod
        def select_all(action: Optional[Any] = 'TOGGLE'):
            pass

    class OpsCurve:
        @staticmethod
        def simple(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), simple=True, simple_Change=False, simple_Delete="", simple_Type='Point', simple_endlocation=(2, 2, 2), simple_a=2, simple_b=1, simple_h=1, simple_angle=45, simple_startangle=0, simple_endangle=45,
                   simple_sides=3, simple_radius=1, simple_center=True, simple_degrees_or_radians='Degrees', simple_width=2, simple_length=2, simple_rounded=0, shape='2D', output_type='BEZIER', use_cyclic_u=True, endp_u=True, order_u=4, handle_type='VECTOR', edit_mode=True):
            raise NotImplementedError()

    class OpsMesh:

        @staticmethod
        def primitive_gear(
                name,
                number_of_teeth,
                radius,
                addendum,
                dedendum,
                angle,
                base,
                width,
                skew,
                conangle,
                crown):
            global mockBpy
            mockBpy.data.create_mesh_object("Gear", "Gear", [Mesh.MeshVertex(v * 0.5 * radius * Vector((1, 1, 1))) for v in [Vector((-1.0, -1.0, -1.0)), Vector((-1.0, -1.0, 1.0)), Vector((-1.0, 1.0, -1.0)), Vector(
                (-1.0, 1.0, 1.0)), Vector((1.0, -1.0, -1.0)), Vector((1.0, -1.0, 1.0)), Vector((1.0, 1.0, -1.0)), Vector((1.0, 1.0, 1.0))]])

        @ staticmethod
        def primitive_cube_add(
                size: Optional[Any] = 2.0,
                location: Optional[Any] = (
                    0.0, 0.0, 0.0),
                rotation: Optional[Any] = (
                    0.0, 0.0, 0.0),
                scale: Optional[Any] = (0.0, 0.0, 0.0)):
            global mockBpy
            mockBpy.data.create_mesh_object("Cube", "Cube", [Mesh.MeshVertex(v * 0.5 * size * Vector(scale or (1, 1, 1))) for v in [Vector((-1.0, -1.0, -1.0)), Vector((-1.0, -1.0, 1.0)), Vector((-1.0, 1.0, -1.0)), Vector(
                (-1.0, 1.0, 1.0)), Vector((1.0, -1.0, -1.0)), Vector((1.0, -1.0, 1.0)), Vector((1.0, 1.0, -1.0)), Vector((1.0, 1.0, 1.0))]])


class Context:

    @ property
    def default_user_collection(self):
        global mockBpy
        return mockBpy.data.collections.collections[0]

    def __init__(self) -> None:
        self.view_layer = Context.ViewLayer()

    def evaluated_depsgraph_get(self):
        pass

    class ViewLayer:
        def update(self):
            pass


class Bpy:
    def __init__(self) -> None:
        self.ops = Ops()
        self.data = Data()
        self.context = Context()


mockBpy = Bpy()


def inject_mock_bpy():
    global mockBpy

    import bpy
    setattr(bpy, "data", mockBpy.data)
    setattr(bpy, "ops", mockBpy.ops)
    setattr(bpy, "context", mockBpy.context)

    import mathutils
    setattr(mathutils, "Matrix", Matrix)
    setattr(mathutils, "Vector", Vector)


def reset_mock_bpy():
    global mockBpy
    mockBpy = Bpy()
