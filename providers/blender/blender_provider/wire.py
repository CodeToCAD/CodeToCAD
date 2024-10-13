from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.utilities import create_uuid_like_id
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.proxy.edge import Edge
from codetocad.proxy.sketch import Sketch
from codetocad.proxy.vertex import Vertex
from codetocad.proxy.landmark import Landmark
from codetocad.proxy.part import Part
from codetocad.interfaces.entity_interface import EntityInterface
from providers.blender.blender_provider import implementables
from providers.blender.blender_provider.blender_actions.modifiers import (
    apply_curve_modifier,
    apply_screw_modifier,
)
from providers.blender.blender_provider.blender_actions.objects_transmute import (
    create_mesh_from_curve,
)
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.blender.blender_provider.blender_definitions import (
    BlenderLength,
    BlenderTypes,
)
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities.override import override
from providers.blender.blender_provider.blender_actions.curve import (
    add_bevel_object_to_curve,
    is_spline_cyclical,
    loft,
    set_curve_offset_geometry,
)
from providers.blender.blender_provider.blender_actions.mesh import recalculate_normals
from providers.blender.blender_provider.blender_actions.normals import (
    calculate_normal,
    project_vector_along_normal,
)
from providers.blender.blender_provider.blender_actions.objects import get_object
from providers.blender.blender_provider.entity import Entity


class Wire(WireInterface, Entity):

    def __init__(
        self,
        name: "str",
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):
        """
        NOTE: Blender Provider's Wire requires a parent_entity and a native_instance
        """
        assert (
            parent_entity is not None and native_instance is not None
        ), "Blender Provider's Wire requires a parent_entity and a native_instance"
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.edges = edges
        self.parent_entity = parent_entity

    @override
    @supported(SupportLevel.SUPPORTED)
    def get_native_instance(self) -> object:
        return self.native_instance

    @supported(SupportLevel.SUPPORTED, notes="Get normal of the wire")
    def get_normal(self, flip: "bool| None" = False) -> "Point":
        # Note: 3D surfaces will not provide a good result here.
        vertices = self.get_vertices()
        num_vertices = len(vertices)
        normal = calculate_normal(
            vertices[0].get_native_instance().co,
            vertices[int(num_vertices * 1 / 3)].get_native_instance().co,
            vertices[int(num_vertices * 2 / 3)].get_native_instance().co,
        )
        return Point.from_list_of_float_or_string(normal)

    @supported(SupportLevel.SUPPORTED, notes="Get vertices of the wire")
    def get_vertices(self) -> list["VertexInterface"]:
        if len(self.edges) == 0:
            return []
        all_vertices = [self.edges[0].v1, self.edges[0].v2]
        for edge in self.edges[1:]:
            all_vertices.append(edge.v2)
        return all_vertices

    @supported(SupportLevel.SUPPORTED, notes="Check whether the wire is closed")
    def get_is_closed(self) -> bool:
        if not self.native_instance:
            raise Exception(
                "Cannot find native wire instance, this may mean that this reference is stale or the object does not exist in Blender."
            )
        return is_spline_cyclical(self.native_instance)

    @supported(SupportLevel.PLANNED)
    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    @supported(
        SupportLevel.PARTIAL,
        "Needs more edge-case testing. If two wires have different number of vertices, one is subdivided to match the other.",
    )
    def loft(
        self, other: "WireInterface", new_part_name: "str| None" = None
    ) -> "PartInterface":
        blender_mesh = loft(self, other)
        part = Part(blender_mesh.name)
        if new_part_name:
            part.rename(new_part_name)
        else:
            if self.parent_entity:
                parent_name = (
                    self.parent_entity.name
                    if not isinstance(self.parent_entity, str)
                    else self.parent_entity
                )
                if type(get_object(parent_name)) == BlenderTypes.MESH.value:
                    part.union(
                        parent_name, delete_after_union=True, is_transfer_data=True
                    )
                else:
                    Entity(parent_name).delete()
                part.rename(parent_name)
            if other.parent_entity:
                parent_name = (
                    other.parent_entity.name
                    if not isinstance(other.parent_entity, str)
                    else other.parent_entity
                )
                if type(get_object(parent_name)) == BlenderTypes.MESH.value:
                    part.union(
                        parent_name, delete_after_union=True, is_transfer_data=True
                    )
                else:
                    Entity(parent_name).delete()
        recalculate_normals(part.name)
        return part

    @supported(SupportLevel.PLANNED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    @supported(SupportLevel.PLANNED)
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    @supported(SupportLevel.PLANNED)
    def union(
        self,
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")
        return self

    @supported(SupportLevel.PLANNED)
    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )
        return self

    @supported(SupportLevel.PLANNED)
    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        raise NotImplementedError()
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="Twist the wire")
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        assert self.parent_entity, "This wire is not associated with a parent entity."
        parent = self.parent_entity
        if isinstance(parent, str):
            parent = Sketch(parent)
        implementables.twist(parent, angle, screw_pitch, iterations, axis)
        return self

    @supported(SupportLevel.SUPPORTED, notes="Revolve the wire")
    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "PartInterface":
        assert self.parent_entity, "This wire is not associated with a parent entity."
        parent = self.parent_entity
        if isinstance(parent, str):
            parent = Sketch(parent)
        if isinstance(about_entity_or_landmark, LandmarkInterface):
            about_entity_or_landmark = (
                about_entity_or_landmark.get_landmark_entity_name()
            )
        elif isinstance(about_entity_or_landmark, Entity):
            about_entity_or_landmark = about_entity_or_landmark.name
        axis = Axis.from_string(axis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"
        apply_screw_modifier(
            parent.name,
            Angle.from_string(angle).to_radians(),
            axis,
            entity_nameToDetermineAxis=about_entity_or_landmark,
        )
        create_mesh_from_curve(parent.name)
        # Recalculate normals because they're usually wrong after revolving.
        recalculate_normals(parent.name)
        return Part(parent.name, description=parent.description).apply()

    @supported(SupportLevel.SUPPORTED, notes="Get offset of the wire")
    def offset(self, radius: "str|float|Dimension"):
        assert self.parent_entity, "This wire is not associated with a parent entity."
        parent = self.parent_entity
        if isinstance(parent, str):
            parent = Sketch(parent)
        # TODO: Make a vertex group around this wire, and apply the offset only to this vertex group
        radius = Dimension.from_string(radius)
        set_curve_offset_geometry(parent.name, radius)
        return self

    @supported(SupportLevel.SUPPORTED, notes="Extrude the wire")
    def extrude(self, length: "str|float|Dimension") -> "PartInterface":
        # We assume the normal is never perpendicular to the Z axis.
        assert self.parent_entity, "This wire is not associated with a parent entity."
        parent = self.parent_entity
        if isinstance(parent, str):
            parent = Sketch(parent)
        assert isinstance(
            parent, SketchInterface
        ), "Extrude only works on wires in a sketch."
        parsed_length = BlenderLength.convert_dimension_to_blender_unit(
            Dimension.from_dimension_or_its_float_or_string_value(length)
        ).value
        normal = self.get_normal()
        # TODO: add the translation component of the wire's initial rotation. For example, if a rectangle of length 1x1 is rotated 45 degrees, then there is a 0.355 translation in the z axis that needs to be accounted for.
        translate_vector = [0, 0, parsed_length]
        projected_normal = project_vector_along_normal(
            translate_vector, [p.value for p in normal.to_list()]
        )
        temp_sketch_1 = Sketch(parent.name + create_uuid_like_id())
        temp_sketch_1.project(self)
        temp_sketch_1.translate_xyz(*projected_normal)

        wire_name = parent.name + "_" + self.name
        temp_sketch_2 = Sketch(wire_name)
        temp_sketch_2.project(self)

        part = temp_sketch_2.get_wires()[0].loft(temp_sketch_1.get_wires()[0])
        part.description = self.description

        return part

    @supported(SupportLevel.SUPPORTED, notes="Sweep the wire")
    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":
        assert self.parent_entity, "This wire is not associated with a parent entity."
        parent = self.parent_entity
        if isinstance(parent, str):
            parent = Sketch(parent)
        # TODO: This logic was moved from Sketch.py. Sweeping should be applied to a vertex group containing this wire only.
        profile_curve_name = profile_name_or_instance
        if isinstance(profile_curve_name, EntityInterface):
            profile_curve_name = profile_curve_name.name
        add_bevel_object_to_curve(parent.name, profile_curve_name, fill_cap)
        create_mesh_from_curve(parent.name)
        # Recalculate normals because they're usually wrong after sweeping.
        recalculate_normals(parent.name)
        return Part(parent.name, parent.description).apply()

    @supported(SupportLevel.SUPPORTED, notes="Get profile of the wire")
    def profile(self, profile_curve_name: "str|WireInterface|SketchInterface"):
        assert self.parent_entity, "This wire is not associated with a parent entity."
        parent = self.parent_entity
        if isinstance(parent, str):
            parent = Sketch(parent)
        # TODO: this logic was moved from Sketch.py. Profiling should be applied to a vertex group containing this wire only.
        if isinstance(profile_curve_name, Entity):
            profile_curve_name = profile_curve_name.name
        apply_curve_modifier(parent.name, profile_curve_name)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def get_edges(self) -> "list[EdgeInterface]":
        print("get_edges called")
        return [
            Edge(
                v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                name="an edge",
            )
        ]

    @supported(SupportLevel.PLANNED)
    def remesh(self, strategy: "str", amount: "float"):
        raise NotImplementedError()
        print("remesh called", f": {strategy}, {amount}")
        return self

    @supported(SupportLevel.PLANNED)
    def subdivide(self, amount: "float"):
        raise NotImplementedError()
        print("subdivide called", f": {amount}")
        return self

    @supported(SupportLevel.PLANNED)
    def decimate(self, amount: "float"):
        raise NotImplementedError()
        print("decimate called", f": {amount}")
        return self

    @supported(SupportLevel.PLANNED)
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        print("create_from_vertices called", f": {points}, {options}")
        return self

    @supported(SupportLevel.PLANNED)
    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        print("create_point called", f": {point}, {options}")
        return self

    @supported(SupportLevel.PLANNED)
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        print("create_line called", f": {length}, {angle}, {start_at}, {options}")
        return self

    @supported(SupportLevel.PLANNED)
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        print("create_line_to called", f": {to}, {start_at}, {options}")
        return self

    @supported(SupportLevel.PLANNED)
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> Self:
        raise NotImplementedError()
        print(
            "create_arc called", f": {end_at}, {radius}, {start_at}, {flip}, {options}"
        )
        return self

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> Self:

        for vertex in self.get_vertices():
            vertex.translate_xyz(x, y, z)

        return self

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_x(self, amount: "str|float|Dimension") -> Self:

        return self.translate_xyz(amount, 0, 0)

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_y(self, amount: "str|float|Dimension") -> Self:

        return self.translate_xyz(0, amount, 0)

    @override
    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_z(self, amount: "str|float|Dimension") -> Self:

        return self.translate_xyz(0, 0, amount)

    @override
    @supported(SupportLevel.UNSUPPORTED, notes="")
    def set_visible(self, is_visible: "bool") -> Self:
        raise NotImplementedError()
