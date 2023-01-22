from typing import Any, Optional, Union
from mock.modeling.MockBlenderMath import Vector, Matrix


class Mesh:
    def __init__(self, name) -> None:
        self.name = name

    def copy(self) -> 'Mesh':
        copy = Mesh(self.name)

        global mockBpy
        mockBpy.data.meshes.meshes.append(copy)

        return copy


class Object:
    isHide = False

    def __init__(self, name, default_users_collection: Optional['Collection']) -> None:
        self.name = name
        self.data: Optional[Any] = None
        self.children: list['Object'] = []
        self.parent: Optional[Object] = None
        self.matrix_world = Matrix()
        self.matrix_basis = self.matrix_world
        self.bound_box = [[0, 0, 0] for i in range(8)]
        self.users_collection = [
            default_users_collection] if default_users_collection else []
        self.modifiers = Object.Modifiers()
        self.constraints = Object.Constraints()

    @property
    def matrix_local(self) -> Matrix:
        if self.parent is None:
            return self.matrix_world
        return self.parent.matrix_world - self.matrix_world

    @property
    def location(self):
        return self.matrix_local.translation

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "location":
            self.matrix_world.translate(
                __value[0], __value[1], __value[2])

            for child in self.children:
                child.matrix_world.translate(
                    __value[0], __value[1], __value[2])
            return

        if __name == "parent":
            if __value == None:
                if hasattr(self, "parent") and self.parent:
                    self.parent.children.remove(self)
            else:
                __value.children.append(self)

        super().__setattr__(__name, __value)

    def visible_get(self):
        return not self.isHide

    def hide_set(self, isHide):
        self.isHide = isHide

    def select_set(self, isSelected):
        global mockBpy
        mockBpy.data.selectedObject = self if isSelected else None

    def copy(self) -> 'Object':
        global mockBpy
        copy = Object(self.name, mockBpy.context.default_user_collection)
        copy.data = self.data
        copy.children = self.children
        copy.location = self.location
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

    def objectBelongsToCollection(self, object: Object) -> bool:
        global mockBpy
        return self in object.users_collection

    @property
    def linkedObjects(self):
        return list(filter(self.objectBelongsToCollection, mockBpy.data.objects.objects))

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

    def removeUsingData(self, data):
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
        mockBpy.data.objects.removeUsingData(mesh)


class Data:

    def __init__(self) -> None:
        self.objects = Objects()
        self.meshes = Meshes()
        self.collections = Collections()
        self.collections.collections.append(Collection("Scene"))

        self.selectedObject: Optional[Object] = None

    def createMeshObject(self, objectName, meshName):
        global mockBpy

        mesh = Mesh(meshName)
        obj = Object(objectName, mockBpy.context.default_user_collection)
        obj.data = mesh
        mockBpy.data.objects.objects.append(obj)
        mockBpy.data.meshes.meshes.append(mesh)


class Ops:
    def __init__(self) -> None:
        self.object = Ops.OpsObject()
        self.mesh = Ops.OpsMesh()
        self.export_mesh = Ops.OpsExportMesh()
        self.export_scene = Ops.OpsExportScene()
        self.wm = Ops.OpsWM()

    class OpsExportMesh:
        @staticmethod
        def stl(
                filepath: Union[str, Any] = "",
                use_selection: Union[bool, Any] = False,
                global_scale: Optional[Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsExportScene:
        @staticmethod
        def obj(
                filepath: Union[str, Any] = "",
                use_selection: Union[bool, Any] = False,
                global_scale: Optional[Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsWM:
        @staticmethod
        def obj_export(
                filepath: Union[str, Any] = "",
                export_selected_objects: Union[bool,
                                               Any] = False,
                global_scale: Optional[Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsObject:
        @staticmethod
        def empty_add(radius, **keywordArguments):
            global mockBpy
            mockBpy.data.objects.objects.append(
                Object("Empty", mockBpy.context.default_user_collection))

        @staticmethod
        def select_all(action: Optional[Any] = 'TOGGLE'):
            pass

    class OpsMesh:

        @staticmethod
        def primitive_cube_add(
                size: Optional[Any] = 2.0,
                location: Optional[Any] = (
                    0.0, 0.0, 0.0),
                rotation: Optional[Any] = (
                    0.0, 0.0, 0.0),
                scale: Optional[Any] = (0.0, 0.0, 0.0)):
            global mockBpy
            mockBpy.data.createMeshObject("Cube", "Cube")


class Context:

    @property
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


def injectMockBpy():
    global mockBpy

    import bpy
    setattr(bpy, "data", mockBpy.data)
    setattr(bpy, "ops", mockBpy.ops)
    setattr(bpy, "context", mockBpy.context)

    import mathutils
    setattr(mathutils, "Matrix", Matrix)
    setattr(mathutils, "Vector", Vector)


def resetMockBpy():
    global mockBpy
    mockBpy = Bpy()
