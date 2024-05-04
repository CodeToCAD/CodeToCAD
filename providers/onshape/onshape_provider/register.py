# THIS IS AN AUTO-GENERATED FILE. DO NOT CHANGE.

from .entity import Entity
from codetocad.interfaces.entity_interface import EntityInterface
from .part import Part
from codetocad.interfaces.part_interface import PartInterface
from .sketch import Sketch
from codetocad.interfaces.sketch_interface import SketchInterface
from .vertex import Vertex
from codetocad.interfaces.vertex_interface import VertexInterface
from .edge import Edge
from codetocad.interfaces.edge_interface import EdgeInterface
from .wire import Wire
from codetocad.interfaces.wire_interface import WireInterface
from .landmark import Landmark
from codetocad.interfaces.landmark_interface import LandmarkInterface
from .joint import Joint
from codetocad.interfaces.joint_interface import JointInterface
from .material import Material
from codetocad.interfaces.material_interface import MaterialInterface
from .animation import Animation
from codetocad.interfaces.animation_interface import AnimationInterface
from .light import Light
from codetocad.interfaces.light_interface import LightInterface
from .camera import Camera
from codetocad.interfaces.camera_interface import CameraInterface
from .render import Render
from codetocad.interfaces.render_interface import RenderInterface
from .scene import Scene
from codetocad.interfaces.scene_interface import SceneInterface
from .analytics import Analytics
from codetocad.interfaces.analytics_interface import AnalyticsInterface


def register():
    __import__("codetocad").providers.register(Entity, EntityInterface)
    __import__("codetocad").providers.register(Part, PartInterface)
    __import__("codetocad").providers.register(Sketch, SketchInterface)
    __import__("codetocad").providers.register(Vertex, VertexInterface)
    __import__("codetocad").providers.register(Edge, EdgeInterface)
    __import__("codetocad").providers.register(Wire, WireInterface)
    __import__("codetocad").providers.register(Landmark, LandmarkInterface)
    __import__("codetocad").providers.register(Joint, JointInterface)
    __import__("codetocad").providers.register(Material, MaterialInterface)
    __import__("codetocad").providers.register(Animation, AnimationInterface)
    __import__("codetocad").providers.register(Light, LightInterface)
    __import__("codetocad").providers.register(Camera, CameraInterface)
    __import__("codetocad").providers.register(Render, RenderInterface)
    __import__("codetocad").providers.register(Scene, SceneInterface)
    __import__("codetocad").providers.register(Analytics, AnalyticsInterface)
