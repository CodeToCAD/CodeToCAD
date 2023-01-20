from typing import Any, Optional
import typing


class Mesh:
    def __init__(self) -> None:
        self.name = ""


class Matrix:
    def __init__(self) -> None:
        self.translation = (0, 0, 0)


class Object:
    isHide = False

    def __init__(self) -> None:
        self.name = ""
        self.data: Optional[Any] = None
        self.children: list['Object'] = []
        self.location = (0, 0, 0)
        self.matrix_world = Matrix()

    def visible_get(self):
        return not self.isHide

    def hide_set(self, isHide):
        self.isHide = isHide

    def select_set(self, isSelected):
        global mockBpy
        mockBpy.data.selectedObject = self if isSelected else None


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

        self.selectedObject: Optional[Object] = None

    def createMeshObject(self, objectName, meshName):
        mesh = Mesh()
        mesh.name = meshName
        obj = Object()
        obj.name = objectName
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
                filepath: typing.Union[str, typing.Any] = "",
                use_selection: typing.Union[bool, typing.Any] = False,
                global_scale: typing.Optional[typing.Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsExportScene:
        @staticmethod
        def obj(
                filepath: typing.Union[str, typing.Any] = "",
                use_selection: typing.Union[bool, typing.Any] = False,
                global_scale: typing.Optional[typing.Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsWM:
        @staticmethod
        def obj_export(
                filepath: typing.Union[str, typing.Any] = "",
                export_selected_objects: typing.Union[bool,
                                                      typing.Any] = False,
                global_scale: typing.Optional[typing.Any] = 1.0
        ):
            return {'FINISHED'}

    class OpsObject:
        @staticmethod
        def select_all(action: typing.Optional[typing.Any] = 'TOGGLE'):
            pass

    class OpsMesh:
        @staticmethod
        def primitive_cube_add(
                size: typing.Optional[typing.Any] = 2.0,
                location: typing.Optional[typing.Any] = (
                    0.0, 0.0, 0.0),
                rotation: typing.Optional[typing.Any] = (
                    0.0, 0.0, 0.0),
                scale: typing.Optional[typing.Any] = (0.0, 0.0, 0.0)):
            global mockBpy
            mockBpy.data.createMeshObject("Cube", "Cube")


class Context:
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


def resetMockBpy():
    global mockBpy
    mockBpy = Bpy()
