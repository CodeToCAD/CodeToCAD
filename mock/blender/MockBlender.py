from typing import Any, Optional
import typing


def injectMockBpy():
    global mockBpy

    import bpy

    setattr(bpy, "data", mockBpy.data)
    setattr(bpy, "ops", mockBpy.ops)


class Mesh:
    name = ""


class Object:
    name = ""
    data: Optional[Any] = None
    children: list['Object'] = []


class Objects:
    objects: list[Object] = []

    def get(self, name):
        for object in self.objects:
            if object.name == name:
                return object


class Meshes:
    meshes: list[Mesh] = []

    def get(self, name):
        for mesh in self.meshes:
            if mesh.name == name:
                return mesh


class Data:
    objects = Objects()
    meshes = Meshes()

    def createMeshObject(self, objectName, meshName):
        mesh = Mesh()
        mesh.name = meshName
        obj = Object()
        obj.name = objectName
        obj.data = mesh
        mockBpy.data.objects.objects.append(obj)
        mockBpy.data.meshes.meshes.append(mesh)


class Ops:
    class Mesh:
        def primitive_cube_add(override_context: typing.
                               Union[typing.Dict, 'bpy.types.Context'] = None,
                               execution_context: typing.Union[str,
                                                               int] = None,
                               undo: typing.Optional[bool] = None,
                               *,
                               size: typing.Optional[typing.Any] = 2.0,
                               calc_uvs: typing.Union[bool, typing.Any] = True,
                               enter_editmode: typing.Union[bool,
                                                            typing.Any] = False,
                               align: typing.Optional[typing.Any] = 'WORLD',
                               location: typing.Optional[typing.Any] = (
                                   0.0, 0.0, 0.0),
                               rotation: typing.Optional[typing.Any] = (
                                   0.0, 0.0, 0.0),
                               scale: typing.Optional[typing.Any] = (0.0, 0.0, 0.0)):
            global mockBpy
            mockBpy.data.createMeshObject("Cube", "Cube")

    mesh = Mesh()


class Bpy:
    ops = Ops()
    data = Data()


mockBpy = Bpy()
