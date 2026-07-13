"""Blender (bpy) adapter classes for CodeToCAD.

The adapter ``Part3D``/``Part2D`` subclasses replay the operations recorded
by the CodeToCAD API onto Blender mesh objects: base primitive, booleans
(boolean modifier), shell (solidify modifier), fillet/chamfer (bevel
modifier), holes (boolean with a cylinder cutter) and transforms (object
transforms). Modifiers are baked through the dependency graph, so everything
works headless (``blender --background``).

Units are meters throughout, matching CodeToCAD's core and Blender's default
scene units. Meshes are tessellated, so analysis values are approximate to
the tessellation (segments are generous).

Custom shapes: subclass ``Part3D`` and override ``build_native()`` to return
any Blender mesh object; all CodeToCAD operations still apply on top of it.
"""

from __future__ import annotations

import math
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Vector as BVector

import codetocad
from codetocad.location import Location, quat_rotate_vector
from codetocad.topology import Edge, Face, Vertex
from codetocad.units import LengthWithUnit
from codetocad.vectors import Vec3

CIRCLE_SEGMENTS = 96
SPHERE_SEGMENTS = (64, 32)


# -- low-level helpers --


def _link(obj: bpy.types.Object) -> None:
    bpy.context.collection.objects.link(obj)


def _select_only(obj: bpy.types.Object) -> None:
    # Refresh first: the view layer can hold stale entries right after
    # objects (e.g. boolean cutters) are removed.
    bpy.context.view_layer.update()
    for other in list(bpy.context.view_layer.objects):
        if other is not None:
            other.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def _new_mesh_object(name: str, bm: bmesh.types.BMesh) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    _link(obj)
    return obj


def _bake_modifiers(obj: bpy.types.Object) -> None:
    """Apply all modifiers into the mesh via the depsgraph (headless-safe)."""
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    baked = bpy.data.meshes.new_from_object(evaluated)
    old = obj.data
    obj.data = baked
    obj.modifiers.clear()
    if old.users == 0:
        bpy.data.meshes.remove(old)


def _remove_object(obj: bpy.types.Object) -> None:
    mesh = obj.data if obj.type == "MESH" else None
    bpy.data.objects.remove(obj, do_unlink=True)
    if mesh is not None and mesh.users == 0:
        bpy.data.meshes.remove(mesh)


def _world_matrix(obj: bpy.types.Object):
    # matrix_world is stale after direct transform changes until the
    # dependency graph re-evaluates.
    bpy.context.view_layer.update()
    return obj.matrix_world


def _world_bmesh(obj: bpy.types.Object) -> bmesh.types.BMesh:
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(_world_matrix(obj))
    return bm


def _bvector_to_location(vector: BVector) -> Location:
    return Location(float(vector.x), float(vector.y), float(vector.z))


# -- primitive meshes --


def _cube_bmesh(length: float, width: float, height: float) -> bmesh.types.BMesh:
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for vertex in bm.verts:
        vertex.co.x *= length
        vertex.co.y *= width
        vertex.co.z *= height
    return bm


def _cylinder_bmesh(radius: float, height: float) -> bmesh.types.BMesh:
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=CIRCLE_SEGMENTS,
        radius1=radius,
        radius2=radius,
        depth=height,
    )
    return bm


def _sphere_bmesh(radius: float) -> bmesh.types.BMesh:
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=SPHERE_SEGMENTS[0],
        v_segments=SPHERE_SEGMENTS[1],
        radius=radius,
    )
    return bm


def _rectangle_bmesh(width: float, height: float) -> bmesh.types.BMesh:
    bm = bmesh.new()
    corners = [
        bm.verts.new((x * width / 2, y * height / 2, 0.0))
        for x, y in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    bm.faces.new(corners)
    return bm


def _circle_bmesh(radius: float) -> bmesh.types.BMesh:
    bm = bmesh.new()
    bmesh.ops.create_circle(
        bm, cap_ends=True, segments=CIRCLE_SEGMENTS, radius=radius
    )
    return bm


def _text_object(name: str, primitive: dict, height: float) -> bpy.types.Object:
    """Build a (possibly extruded) text mesh, centered at the origin with the
    extrusion spanning z in [-height/2, height/2]."""
    curve = bpy.data.curves.new(f"{name}_curve", type="FONT")
    curve.body = primitive["text"]
    curve.size = primitive["size"]
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    if height:
        curve.extrude = height / 2
    text_obj = bpy.data.objects.new(f"{name}_text", curve)
    _link(text_obj)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(text_obj.evaluated_get(depsgraph))
    bpy.data.objects.remove(text_obj, do_unlink=True)
    obj = bpy.data.objects.new(name, mesh)
    _link(obj)
    # Normalize: Blender's curve extrude conventions vary, so measure the z
    # span and rescale/recenter it to exactly [-height/2, height/2].
    if height and mesh.vertices:
        zs = [v.co.z for v in mesh.vertices]
        z_min, z_max = min(zs), max(zs)
        span = z_max - z_min
        scale = height / span if span > 1e-12 else 1.0
        mid = (z_max + z_min) / 2
        for vertex in mesh.vertices:
            vertex.co.z = (vertex.co.z - mid) * scale
    return obj


def _base_object(name: str, primitive: dict) -> bpy.types.Object:
    kind = primitive["kind"]
    if kind == "cube":
        return _new_mesh_object(
            name,
            _cube_bmesh(primitive["length"], primitive["width"], primitive["height"]),
        )
    if kind == "cylinder":
        return _new_mesh_object(
            name, _cylinder_bmesh(primitive["radius"], primitive["height"])
        )
    if kind == "sphere":
        return _new_mesh_object(name, _sphere_bmesh(primitive["radius"]))
    if kind == "rectangle":
        return _new_mesh_object(
            name, _rectangle_bmesh(primitive["width"], primitive["height"])
        )
    if kind == "circle":
        return _new_mesh_object(name, _circle_bmesh(primitive["radius"]))
    if kind == "text":
        return _text_object(name, primitive, height=0.0)
    if kind == "extrusion":
        profile = primitive["profile"]
        if profile["kind"] == "text":
            return _text_object(name, profile, height=primitive["height"])
        raise NotImplementedError(
            f"Blender adapter cannot extrude a {profile['kind']!r} profile"
        )
    if kind == "imported":
        return _import_object(primitive["file_path"])
    raise NotImplementedError(f"Blender adapter cannot build a {kind!r} primitive")


def _import_object(file_path: str) -> bpy.types.Object:
    suffix = Path(file_path).suffix.lower()
    before = set(bpy.context.view_layer.objects)
    if suffix == ".stl":
        bpy.ops.wm.stl_import(filepath=file_path)
    elif suffix == ".obj":
        bpy.ops.wm.obj_import(filepath=file_path)
    else:
        raise NotImplementedError(
            f"Cannot import {suffix!r} files with the Blender adapter"
        )
    imported = [o for o in bpy.context.view_layer.objects if o not in before]
    if not imported:
        raise ValueError(f"Nothing was imported from {file_path}")
    return imported[0]


class Part3D(codetocad.Part3D):
    """A CodeToCAD Part3D federated to Blender."""

    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._obj: bpy.types.Object | None = None
        self._built_op_count = -1

    # -- building --

    def build_native(self) -> bpy.types.Object:
        """The base mesh object, before CodeToCAD operations are applied.
        Override this in a subclass to define a custom shape with bpy."""
        if self._primitive is None:
            raise NotImplementedError(
                "Override build_native() to return a Blender object for this "
                "shape"
            )
        obj = _base_object(self.name or "part", self._primitive)
        obj.location = (
            self._start_origin.x,
            self._start_origin.y,
            self._start_origin.z,
        )
        return obj

    def build(self):
        """Build the object in Blender, replaying all recorded operations."""
        if self._obj is not None:
            _remove_object(self._obj)
        obj = self.build_native()
        if self.name:
            obj.name = self.name
        for operation in self.operations:
            self._apply_operation(obj, operation)
        if self.material is not None:
            self._apply_material(obj)
        self._obj = obj
        self._built_op_count = len(self.operations)
        return self

    def get_native(self) -> bpy.types.Object:
        """The Blender object, (re)building it if operations changed."""
        if self._obj is None or self._built_op_count != len(self.operations):
            self.build()
        return self._obj

    def _apply_material(self, obj: bpy.types.Object) -> None:
        material = bpy.data.materials.new(self.material.name)
        if self.material.color_rgba is not None:
            material.diffuse_color = self.material.color_rgba.to_tuple()
        obj.data.materials.append(material)

    # -- operation replay --

    def _apply_operation(self, obj: bpy.types.Object, operation: dict) -> None:
        name = operation["operation"]
        if name in codetocad.CONSTRAINT_OPERATIONS:
            # Assembly constraints don't change geometry; simulation
            # integrations turn them into joints.
            return
        if name == "hole":
            self._apply_hole(obj, operation)
        elif name == "shell":
            self._apply_shell(obj, operation)
        elif name in ("fillet", "chamfer"):
            self._apply_bevel(obj, operation)
        elif name in ("subtract", "union", "intersect"):
            self._apply_boolean(obj, operation)
        elif name in codetocad.PATTERN_OPERATIONS:
            self._apply_pattern(obj, operation)
        elif name == "transform":
            self._apply_transform(obj, operation)
        else:
            raise NotImplementedError(
                f"Blender adapter cannot apply operation {name!r}"
            )

    def _apply_hole(self, obj: bpy.types.Object, operation: dict) -> None:
        start_location = self.resolve_location(operation["start_location"])
        radius = operation["radius"].value
        start = start_location.to_numpy()
        if operation["end_location"] is not None:
            end = self.resolve_location(operation["end_location"]).to_numpy()
            depth = float(np.linalg.norm(end - start))
            direction = (end - start) / depth
        else:
            depth = operation["amount"].value
            direction = quat_rotate_vector(start_location.quat, (0.0, 0.0, -1.0))
            if start_location.inverted:
                direction = -direction
            end = start + direction * depth
        # Extend the cutter a hair past both ends to avoid coplanar faces.
        epsilon = 1e-6
        center = (start + end) / 2
        cutter = _new_mesh_object(
            "codetocad_hole_cutter", _cylinder_bmesh(radius, depth + 2 * epsilon)
        )
        cutter.location = tuple(center)
        cutter.rotation_mode = "QUATERNION"
        cutter.rotation_quaternion = BVector((0, 0, 1)).rotation_difference(
            BVector(tuple(direction))
        )
        self._boolean_with_object(obj, cutter, "DIFFERENCE")
        _remove_object(cutter)

    def _apply_shell(self, obj: bpy.types.Object, operation: dict) -> None:
        if operation["start_at_location"] is not None:
            target = self.resolve_location(operation["start_at_location"]).to_numpy()
            world = _world_matrix(obj)
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            opening = min(
                bm.faces,
                key=lambda f: np.linalg.norm(
                    np.array((world @ f.calc_center_median())[:]) - target
                ),
            )
            bmesh.ops.delete(bm, geom=[opening], context="FACES")
            bm.to_mesh(obj.data)
            bm.free()
        modifier = obj.modifiers.new("codetocad_shell", "SOLIDIFY")
        modifier.thickness = operation["thickness"].value
        modifier.offset = -1.0  # thicken inward
        modifier.use_even_offset = True
        _bake_modifiers(obj)

    def _apply_bevel(self, obj: bpy.types.Object, operation: dict) -> None:
        mesh = obj.data
        targets: list[Location] = []
        for edge in operation["edges"] or []:
            targets.append(edge.midpoint)
        for face in operation["faces"] or []:
            targets.append(face.center)
        modifier = obj.modifiers.new("codetocad_bevel", "BEVEL")
        modifier.affect = "EDGES"
        modifier.width = operation["amount"].value
        modifier.segments = 8 if operation["operation"] == "fillet" else 1
        if targets:
            attribute = mesh.attributes.get("bevel_weight_edge")
            if attribute is None:
                attribute = mesh.attributes.new(
                    "bevel_weight_edge", "FLOAT", "EDGE"
                )
            world = _world_matrix(obj)
            midpoints = np.array(
                [
                    (
                        world
                        @ (
                            (
                                mesh.vertices[e.vertices[0]].co
                                + mesh.vertices[e.vertices[1]].co
                            )
                            / 2
                        )
                    )[:]
                    for e in mesh.edges
                ]
            )
            for target in targets:
                index = int(
                    np.argmin(np.linalg.norm(midpoints - target.to_numpy(), axis=1))
                )
                attribute.data[index].value = 1.0
            modifier.limit_method = "WEIGHT"
        else:
            modifier.limit_method = "NONE"
        _bake_modifiers(obj)

    def _apply_boolean(self, obj: bpy.types.Object, operation: dict) -> None:
        other = operation["other_part"]
        temporary = not isinstance(other, Part3D)
        other_part = adapt(other) if temporary else other
        other_obj = other_part.get_native()
        location = operation["location"]
        other_location = operation["other_location"]
        saved_location = tuple(other_obj.location)
        if location is not None and other_location is not None:
            anchor = self.resolve_location(location).to_numpy()
            other_anchor = other_part.resolve_location(other_location).to_numpy()
            offset = anchor - other_anchor
            other_obj.location = tuple(np.array(saved_location) + offset)
        mode = {
            "subtract": "DIFFERENCE",
            "union": "UNION",
            "intersect": "INTERSECT",
        }[operation["operation"]]
        self._boolean_with_object(obj, other_obj, mode)
        if temporary:
            _remove_object(other_obj)
            other_part._obj = None
        else:
            other_obj.location = saved_location

    @staticmethod
    def _boolean_with_object(
        obj: bpy.types.Object, other_obj: bpy.types.Object, mode: str
    ) -> None:
        bpy.context.view_layer.update()
        modifier = obj.modifiers.new("codetocad_boolean", "BOOLEAN")
        modifier.operation = mode
        modifier.solver = "EXACT"
        modifier.object = other_obj
        _bake_modifiers(obj)

    def _apply_pattern(self, obj: bpy.types.Object, operation: dict) -> None:
        from mathutils import Matrix

        count = operation["count"]
        if operation["operation"] == "linear_pattern":
            offset = operation["offset"].to_numpy()
            transforms = [
                Matrix.Translation(tuple(offset * i)) for i in range(1, count)
            ]
        else:
            center = BVector(tuple(operation["center"].to_numpy()))
            axis = BVector(operation["axis"])
            step = operation["separation_angle"].value
            transforms = [
                Matrix.Translation(center)
                @ Matrix.Rotation(step * i, 4, axis)
                @ Matrix.Translation(-center)
                for i in range(1, count)
            ]
        # Duplicate the base object for every instance before any union, so
        # later instances don't copy the already-unioned result.
        base_matrix = _world_matrix(obj).copy()
        instances = []
        for transform in transforms:
            instance = obj.copy()
            instance.data = obj.data.copy()
            _link(instance)
            instance.matrix_world = transform @ base_matrix
            instances.append(instance)
        for instance in instances:
            self._boolean_with_object(obj, instance, "UNION")
            _remove_object(instance)

    def _apply_transform(self, obj: bpy.types.Object, operation: dict) -> None:
        location: Location = operation["location"]
        if operation["mode"] == "absolute":
            obj.location = location.to_tuple()
        else:
            obj.location = tuple(
                np.array(obj.location[:]) + location.to_numpy()
            )
        qx, qy, qz, qw = location.quat
        if abs(qw - 1.0) > 1e-12 or any(abs(q) > 1e-12 for q in (qx, qy, qz)):
            obj.rotation_mode = "QUATERNION"
            # mathutils quaternions are (w, x, y, z).
            from mathutils import Quaternion as BQuaternion

            obj.rotation_quaternion = (
                BQuaternion((qw, qx, qy, qz)) @ obj.rotation_quaternion
            )

    # -- geometry queries on native topology --

    def _native_vertices(self) -> list[Vertex]:
        obj = self.get_native()
        world = _world_matrix(obj)
        return [
            Vertex(_bvector_to_location(world @ v.co), native=v.index)
            for v in obj.data.vertices
        ]

    def _native_edges(self) -> list[Edge]:
        obj = self.get_native()
        world = _world_matrix(obj)
        mesh = obj.data
        return [
            Edge(
                Vertex(_bvector_to_location(world @ mesh.vertices[e.vertices[0]].co)),
                Vertex(_bvector_to_location(world @ mesh.vertices[e.vertices[1]].co)),
                native=e.index,
            )
            for e in mesh.edges
        ]

    def _native_faces(self) -> list[Face]:
        obj = self.get_native()
        world = _world_matrix(obj)
        mesh = obj.data
        faces = []
        for polygon in mesh.polygons:
            vertices = [
                Vertex(_bvector_to_location(world @ mesh.vertices[i].co))
                for i in polygon.vertices
            ]
            faces.append(Face(vertices, native=polygon.index))
        return faces

    def _face_center(self, face: Face) -> Location:
        obj = self.get_native()
        polygon = obj.data.polygons[face.native]
        return _bvector_to_location(_world_matrix(obj) @ polygon.center)

    def get_vertex(self, location, tolerance: float = 1e-2) -> Vertex:
        return self._nearest(
            self._native_vertices(), lambda v: v.location, self._resolve(location), tolerance
        )

    def get_edge(self, location, tolerance: float = 1e-2) -> Edge:
        return self._nearest(
            self._native_edges(), lambda e: e.midpoint, self._resolve(location), tolerance
        )

    def get_face(self, location, tolerance: float = 1e-2) -> Face:
        return self._nearest(
            self._native_faces(), self._face_center, self._resolve(location), tolerance
        )

    def get_vertices(self, location1, location2, location3=None, location4=None, tolerance: float = 1e-2):
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        return self._filter_bounded(
            self._native_vertices(), lambda v: v.location, locations, tolerance
        )

    def get_edges(self, location1, location2, location3=None, location4=None, tolerance: float = 1e-2):
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        return self._filter_bounded(
            self._native_edges(), lambda e: e.midpoint, locations, tolerance
        )

    def get_faces(self, location1, location2, location3=None, location4=None, tolerance: float = 1e-2):
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        return self._filter_bounded(
            self._native_faces(), self._face_center, locations, tolerance
        )

    # -- analysis and export on the native object --

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        obj = self.get_native()
        world = _world_matrix(obj)
        points = np.array([(world @ BVector(corner))[:] for corner in obj.bound_box])
        return (Vec3(*points.min(axis=0)), Vec3(*points.max(axis=0)))

    def get_volume(self) -> float:
        bm = _world_bmesh(self.get_native())
        volume = bm.calc_volume(signed=False)
        bm.free()
        return float(volume)

    def get_area(self) -> float:
        bm = _world_bmesh(self.get_native())
        area = sum(f.calc_area() for f in bm.faces)
        bm.free()
        return float(area)

    def export(self, location: str) -> str:
        obj = self.get_native()
        _select_only(obj)
        suffix = Path(location).suffix.lower()
        filepath = str(Path(location).resolve())
        if suffix == ".stl":
            bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True)
        elif suffix == ".obj":
            bpy.ops.wm.obj_export(filepath=filepath, export_selected_objects=True)
        elif suffix in (".glb", ".gltf"):
            bpy.ops.export_scene.gltf(filepath=filepath, use_selection=True)
        elif suffix == ".fbx":
            bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True)
        elif suffix == ".blend":
            bpy.ops.wm.save_as_mainfile(filepath=filepath)
        else:
            raise ValueError(
                f"Unsupported export format {suffix!r}; use .stl, .obj, .glb, "
                ".fbx or .blend"
            )
        return location


class Part2D(codetocad.Part2D):
    """A CodeToCAD Part2D (sketch) federated to Blender as a flat mesh."""

    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._obj: bpy.types.Object | None = None

    def build_native(self) -> bpy.types.Object:
        if self._primitive is None:
            raise NotImplementedError(
                "Override build_native() to return a Blender object for this "
                "shape"
            )
        obj = _base_object(self.name or "sketch", self._primitive)
        obj.location = (
            self._start_origin.x,
            self._start_origin.y,
            self._start_origin.z,
        )
        return obj

    def build(self):
        if self._obj is not None:
            _remove_object(self._obj)
        self._obj = self.build_native()
        return self

    def get_native(self) -> bpy.types.Object:
        if self._obj is None:
            self.build()
        return self._obj

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        obj = self.get_native()
        world = _world_matrix(obj)
        points = np.array([(world @ BVector(corner))[:] for corner in obj.bound_box])
        return (Vec3(*points.min(axis=0)), Vec3(*points.max(axis=0)))

    def get_area(self) -> float:
        bm = _world_bmesh(self.get_native())
        area = sum(f.calc_area() for f in bm.faces)
        bm.free()
        return float(area)

    def extrude(self, height: LengthWithUnit) -> Part3D:
        return adapt(super().extrude(height))


class ElectricalComponent(Part3D, codetocad.ECADMixin):
    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._init_ecad()


def adapt(part) -> Part2D | Part3D:
    """Adapt any core CodeToCAD part (with its recorded operations, material,
    ledgers, ...) into a Blender-federated part."""
    if isinstance(part, (Part2D, Part3D)):
        return part
    if isinstance(part, codetocad.ElectricalComponent):
        adapter_class = ElectricalComponent
    elif isinstance(part, codetocad.Part2D):
        adapter_class = Part2D
    elif isinstance(part, codetocad.Part3D):
        adapter_class = Part3D
    else:
        raise TypeError(f"Cannot adapt {type(part).__name__} to Blender")
    adapted = adapter_class(part.name, part.description)
    state = dict(part.__dict__)
    state.pop("_obj", None)
    state.pop("_native", None)
    adapted.__dict__.update(state)
    return adapted


# -- factories --


def make_cube(
    length: LengthWithUnit,
    width: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part3D:
    return adapt(codetocad.cube(length, width, height, start_location))


make_box = make_cube


def make_cylinder(
    radius: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part3D:
    return adapt(codetocad.cylinder(radius, height, start_location))


def make_sphere(
    radius: LengthWithUnit, start_location: Location | None = None
) -> Part3D:
    return adapt(codetocad.sphere(radius, start_location))


def make_import(
    file_path: str, start_location: Location | None = None
) -> Part3D:
    return adapt(codetocad.import_file(file_path, start_location))


def make_rectangle(
    width: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part2D:
    return adapt(codetocad.rectangle(width, height, start_location))


def make_circle(
    radius: LengthWithUnit, start_location: Location | None = None
) -> Part2D:
    return adapt(codetocad.circle(radius, start_location))


def make_text(
    text: str,
    font: str,
    size: LengthWithUnit,
    start_location: Location | None = None,
) -> Part2D:
    """Note: Blender's default font is used; the ``font`` name is recorded
    but custom font loading requires a font file path."""
    return adapt(codetocad.text(text, font, size, start_location))


def make_led(**kwargs) -> ElectricalComponent:
    return adapt(codetocad.led(**kwargs))


def make_resistor(resistance: float, **kwargs) -> ElectricalComponent:
    return adapt(codetocad.resistor(resistance, **kwargs))


def make_capacitor(capacitance: float, **kwargs) -> ElectricalComponent:
    return adapt(codetocad.capacitor(capacitance, **kwargs))


def make_fastener(
    fastener: codetocad.CommonFasteners, length: LengthWithUnit | None = None
) -> Part3D:
    return adapt(fastener.build(length))
