# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.

from .entity import Entity
from .part import Part
from .sketch import Sketch
from .vertex import Vertex
from .edge import Edge
from .wire import Wire
from .landmark import Landmark
from .joint import Joint
from .material import Material
from .animation import Animation
from .light import Light
from .camera import Camera
from .render import Render
from .scene import Scene
from .analytics import Analytics


def register():
    __import__("codetocad").facade.entity.Entity.register(Entity)
    __import__("codetocad").facade.part.Part.register(Part)
    __import__("codetocad").facade.sketch.Sketch.register(Sketch)
    __import__("codetocad").facade.vertex.Vertex.register(Vertex)
    __import__("codetocad").facade.edge.Edge.register(Edge)
    __import__("codetocad").facade.wire.Wire.register(Wire)
    __import__("codetocad").facade.landmark.Landmark.register(Landmark)
    __import__("codetocad").facade.joint.Joint.register(Joint)
    __import__("codetocad").facade.material.Material.register(Material)
    __import__("codetocad").facade.animation.Animation.register(Animation)
    __import__("codetocad").facade.light.Light.register(Light)
    __import__("codetocad").facade.camera.Camera.register(Camera)
    __import__("codetocad").facade.render.Render.register(Render)
    __import__("codetocad").facade.scene.Scene.register(Scene)
    __import__("codetocad").facade.analytics.Analytics.register(Analytics)
