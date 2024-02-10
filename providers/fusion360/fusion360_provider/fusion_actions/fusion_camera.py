import adsk.core
from codetocad import *
from .common import make_axis_vector, make_matrix, make_vector

class FusionCamera:
    def __init__(self):
        app = adsk.core.Application.get()
        self.viewport = app.activeViewport

    def translate(self, x: float, y: float, z: float):
        transform = make_matrix()
        transform.translation = make_vector(x, y, z)
        self.update_camera(transform)

    def target(self):
        app = adsk.core.Application.get()
        self.viewport = app.activeViewport
        des = app.activeProduct
        boundBox = des.rootComponent.boundingBox
        target = adsk.core.Point3D.create(
            (boundBox.minPoint.x + boundBox.maxPoint.x) / 2,
            (boundBox.minPoint.y + boundBox.maxPoint.y) / 2,
            (boundBox.minPoint.z + boundBox.maxPoint.z) / 2,
        )
        return target

    def rotate(
        self,
        axis_input: AxisOrItsIndexOrItsName,
        angle: AngleOrItsFloatOrStringValue
    ):
        axis = make_axis_vector(axis_input)
        angle = Angle.from_angle_or_its_float_or_string_value(angle).to_radians().value

        origin = self.viewport.camera.eye

        transform = make_matrix()
        transform.setToRotation(angle, axis, origin)
        self.update_camera(transform)

    def update_camera(
        self,
        transform: adsk.core.Matrix3D,
        extents=None
    ):
        camera = self.viewport.camera
        cameraExtents = camera.viewExtents
        if extents != None:
            cameraExtents = extents
        offset = self.target()
        offset.transformBy(transform)
        camera.eye = offset
        camera.viewExtents = cameraExtents
        camera.upVector = self.get_up_vector()
        self.viewport.camera = camera

    def get_up_vector(self) -> adsk.core.Vector3D:
        camera = self.viewport.camera
        upVector = adsk.core.Vector3D.create(1, 0, 0)
        angle = upVector.angleTo(camera.upVector)
        if adsk.core.Vector3D.create(-1, 0, 0).angleTo(camera.upVector) < angle:
            upVector = adsk.core.Vector3D.create(-1, 0, 0)
            angle = upVector.angleTo(camera.upVector)

        if adsk.core.Vector3D.create(0, 1, 0).angleTo(camera.upVector) < angle:
            upVector = adsk.core.Vector3D.create(0, 1, 0)
            angle = upVector.angleTo(camera.upVector)

        if adsk.core.Vector3D.create(0, -1, 0).angleTo(camera.upVector) < angle:
            upVector = adsk.core.Vector3D.create(0, -1, 0)
            angle = upVector.angleTo(camera.upVector)

        if adsk.core.Vector3D.create(0, 0, 1).angleTo(camera.upVector) < angle:
            upVector = adsk.core.Vector3D.create(0, 0, 1)
            angle = upVector.angleTo(camera.upVector)

        if adsk.core.Vector3D.create(0, 0, -1).angleTo(camera.upVector) < angle:
            upVector = adsk.core.Vector3D.create(0, 0, -1)
            angle = upVector.angleTo(camera.upVector)

        return upVector
