# Blender Actions API Reference

This directory contains utility functions that provide a centralized interface to Blender's API. These functions abstract direct `bpy.*` calls and provide a consistent, maintainable way to interact with Blender from the CodeToCAD adapter.

## Table of Contents

- [Addons](#addons)
- [Animation](#animation)
- [Camera](#camera)
- [Collections](#collections)
- [Console](#console)
- [Constraints](#constraints)
- [Context](#context)
- [Curve](#curve)
- [Drivers](#drivers)
- [Import/Export](#importexport)
- [Light](#light)
- [Material](#material)
- [Mesh](#mesh)
- [Modifiers](#modifiers)
- [Nodes](#nodes)
- [Normals](#normals)
- [Objects](#objects)
- [Objects Context](#objects-context)
- [Objects Transmute](#objects-transmute)
- [Render](#render)
- [Scene](#scene)
- [Transformations](#transformations)
- [Vertex Edge Wire](#vertex-edge-wire)

---

## Addons

Functions for managing Blender addons.

### `addon_set_enabled(addon_name: str, is_enabled: bool)`
Enable or disable a Blender addon.

### `get_addon(addon_name: str) -> bpy.types.Addon | None`
Get an addon by name, returns None if not found.

### `enable_addon(addon_name: str)`
Enable a Blender addon, ensuring it's properly loaded.

---

## Animation

Functions for managing animation properties and keyframes.

### `add_keyframe_to_object(blender_object: bpy.types.Object, frame_number: int, data_path: str)`
Add a keyframe to an object at a specific frame.

### `set_frame_start(frame_number: int, scene_name: str | None)`
Set the animation start frame for a scene.

### `set_frame_end(frame_number: int, scene_name: str | None)`
Set the animation end frame for a scene.

### `set_frame_step(step: int, scene_name: str | None)`
Set the frame step for animation playback.

### `set_frame_current(frame_number: int, scene_name: str | None)`
Set the current frame in the timeline.

---

## Camera

Functions for creating and managing cameras.

### `create_camera(camera_object_name: str, type)`
Create a new camera object.

### `get_camera(camera_name: str) -> bpy.types.Camera`
Get a camera by name, throws if not found.

### `set_scene_camera(blender_camera: bpy.types.Object, scene_name: str | None = None)`
Set the active camera for a scene.

### `set_focal_length(blender_camera: bpy.types.Camera, length=50.0)`
Set the focal length of a camera.

---

## Collections

Functions for managing Blender collections and object organization.

### `get_collection(name: str, scene_name="Scene") -> bpy.types.Collection`
Get a collection by name, throws if not found.

### `get_collection_or_none(name: str, scene_name="Scene") -> bpy.types.Collection | None`
Get a collection by name, returns None if not found.

### `create_collection(name: str, scene_name="Scene")`
Create a new collection in the specified scene.

### `remove_collection(blender_collection: bpy.types.Collection, remove_children: bool)`
Remove a collection and optionally its child objects.

### `remove_object_from_collection(blender_object: bpy.types.Object, blender_collection: bpy.types.Collection)`
Remove an object from a specific collection.

### `link_object_to_collection(blender_object: bpy.types.Object, blender_collection: bpy.types.Collection)`
Link an object to a collection.

### `unlink_object_from_collection(blender_object: bpy.types.Object, blender_collection: bpy.types.Collection)`
Unlink an object from a collection.

### `assign_object_to_collection(blender_object: bpy.types.Object, blender_collection: bpy.types.Collection | None = None, remove_from_other_groups=True, move_children=True)`
Assign an object to a collection with advanced options.

---

## Console

Functions for managing the Blender console and CodeToCAD integration.

### `add_user_site_packages_to_path()`
Add user site packages to Python path for package access.

### `reload_codetocad_modules()`
Reload CodeToCAD modules without restarting Blender.

### `add_codetocad_convenience_words_to_console(namespace)`
Add CodeToCAD classes to Blender console namespace for convenience.

---

## Constraints

Functions for applying and managing object constraints.

### `get_constraint(blender_object: bpy.types.Object, constraint_name) -> bpy.types.Constraint | None`
Get a constraint from an object by name.

### `apply_constraint(blender_object: bpy.types.Object, constraint_type: BlenderConstraintTypes, **kwargs)`
Apply a constraint to an object with specified parameters.

### `apply_limit_location_constraint(blender_object: bpy.types.Object, x: list[float | None] | None, y: list[float | None] | None, z: list[float | None] | None, relative_to_object: bpy.types.Object | None, **kwargs)`
Apply location limits to an object.

### `apply_limit_rotation_constraint(blender_object: bpy.types.Object, x_radians: list[float | None] | None, y_radians: list[float | None] | None, z_radians: list[float | None] | None, relative_to_object: bpy.types.Object | None, **kwargs)`
Apply rotation limits to an object.

### `apply_copy_location_constraint(blender_object: bpy.types.Object, copied_blender_object: bpy.types.Object, copy_x: bool, copy_y: bool, copy_z: bool, use_offset: bool, **kwargs)`
Make an object copy the location of another object.

### `apply_copy_rotation_constraint(blender_object: bpy.types.Object, copied_blender_object: bpy.types.Object, copy_x: bool, copy_y: bool, copy_z: bool, **kwargs)`
Make an object copy the rotation of another object.

### `apply_pivot_constraint(blender_object: bpy.types.Object, pivot_blender_object: bpy.types.Object, **kwargs)`
Apply a pivot constraint to an object.

### `apply_gear_constraint(blender_object: bpy.types.Object, gear_blender_object: bpy.types.Object, ratio: float = 1, **kwargs)`
Create a gear constraint between two objects.

### `translate_landmark_onto_another(object_to_translate: bpy.types.Object, object1_landmark: bpy.types.Object, object2_landmark: bpy.types.Object)`
Translate an object to align landmarks.

---

## Context

Functions for managing Blender context and view operations.

### `update_view_layer()`
Force Blender to update internal data structures.

### `apply_dependency_graph(blender_object: bpy.types.Object)`
Apply the dependency graph to persist object modifications.

### `select_object(blender_object: bpy.types.Object)`
Select an object in the Blender UI.

### `get_selected_objects() -> list[bpy.types.Object]`
Get all currently selected objects.

### `get_context_view_3d(**kwargs)`
Get a 3D viewport context for operations.

### `zoom_to_selected_objects()`
Zoom the viewport to fit selected objects.

### `add_dependency_graph_update_listener(callback)`
Add a callback for dependency graph updates.

### `add_timer(callback)`
Register a timer callback.

### `get_blender_version() -> tuple`
Get the current Blender version.

### `log_message(message: str)`
Log a message using the CodeToCAD addon.

---

## Curve

Functions for creating and managing curves, splines, and text objects.

### `create_uuid_like_id() -> str`
Generate a UUID-like string for naming objects.

### `get_curve(curve_name: str) -> bpy.types.Curve`
Get a curve by name, throws if not found.

### `get_curve_or_none(curve_name: str) -> bpy.types.Curve | None`
Get a curve by name, returns None if not found.

### `set_curve_extrude_property(curve_name: str, length: float)`
Set the extrude property of a curve.

### `set_curve_offset_geometry(curve_name: str, offset: float)`
Set the offset property of a curve.

### `set_curve_use_path(curve_object: bpy.types.Curve, is_use_path: bool)`
Enable or disable path usage for a curve.

### `set_curve_resolution_u(curve_name: str, resolution: int)`
Set the U resolution of a curve.

### `set_curve_resolution_v(curve_name: str, resolution: int)`
Set the V resolution of a curve.

### `create_text(curve_name: str, text: str, size=1.0, bold=False, italic=False, underlined=False, character_spacing=1, word_spacing=1, line_spacing=1, font_file_path: str | None = None)`
Create a text object with formatting options.

### `create_curve(curve_name: str, curve_type: BlenderCurveTypes, points: Sequence[list[float] | Point], interpolation=64, is_3d=False)`
Create a curve with specified points and type.

### `create_spline(blender_curve: bpy.types.Curve, curve_type: BlenderCurveTypes, order_u: int)`
Create a spline within an existing curve.

### `point_exists_in_spline(spline_points, target_point: Point, tolerance=0.001)`
Check if a point exists in a spline within tolerance.

### `is_points_touching(point1, point2, tolerance: float = 0.001) -> bool`
Check if two points are within tolerance distance.

### `merge_touching_splines(curve: bpy.types.Curve, reference_spline_index: int)`
Merge splines that share endpoints.

### `is_spline_cyclical(spline: bpy.types.Spline) -> bool`
Check if a spline is cyclical.

### `get_spline_points(spline: bpy.types.Spline)`
Get the points of a spline (handles different spline types).

### `set_spline_point(spline_points, new_coord: tuple[float, float, float], index: int)`
Set the coordinates of a spline point.

### `add_points_to_spline(spline: bpy.types.Spline, points: list[mathutils.Vector], overwrite_first_point: bool = False)`
Add points to an existing spline.

### `add_points_to_curve(reference_spline: bpy.types.Spline, points: list[mathutils.Vector])`
Add points to a curve, creating new splines as needed.

### `subdivide_bezier_points(bezier_spline: bpy.types.Spline, resolution: int, start_at_index: int = 0, end_at_index: int | None = None, is_cyclic: bool = False)`
Subdivide bezier curve points for higher resolution.

### `get_vertices_from_edges(edges: list[EdgeInterface], world_matrix: mathutils.Matrix)`
Extract vertices from a list of edges.

### `get_vertices_from_bezier_curve(spline: bpy.types.Spline, world_matrix: mathutils.Matrix)`
Extract vertices from a bezier curve.

### `custom_codetocad_loft(wire_1: WireInterface, wire_2: WireInterface) -> bpy.types.Mesh`
Create a lofted mesh between two wires.

### `add_bevel_object_to_curve(path_curve_blender_object: bpy.types.Object, profile_curve_blender_object: bpy.types.Object, fill_cap=False)`
Add a bevel object to a curve for complex profiles.

### `get_blender_curve_primitive_function(curve_primitive: BlenderCurvePrimitiveTypes)`
Get the appropriate function for creating curve primitives.

### `create_simple_curve(curve_primitiveType: BlenderCurvePrimitiveTypes, **kwargs)`
Create simple curve primitives using Blender addons.

---

## Drivers

Functions for creating and managing animation drivers.

### `create_driver(blender_object: bpy.types.Object, path: str, index=-1)`
Create a driver for an object property.

### `remove_driver(blender_object: bpy.types.Object, path: str, index=-1)`
Remove a driver from an object property.

### `get_driver(blender_object: bpy.types.Object, path: str)`
Get a driver for an object property.

### `set_driver(driver: bpy.types.Driver, driver_type, expression="")`
Configure a driver with type and expression.

### `set_driver_variable_single_prop(driver: bpy.types.Driver, variable_name: str, target_blender_object: bpy.types.Object, target_data_path: str)`
Set a single property variable for a driver.

### `set_driver_variable_transforms(driver: bpy.types.Driver, variable_name: str, target_blender_object: bpy.types.Object, transform_type, transform_space)`
Set a transform variable for a driver.

### `set_driver_variable_location_difference(driver: bpy.types.Driver, variable_name: str, target1_blender_object: bpy.types.Object, target2_blender_object: bpy.types.Object)`
Set a location difference variable for a driver.

### `set_driver_variable_rotation_difference(driver: bpy.types.Driver, variable_name: str, target1_blender_object: bpy.types.Object, target2_blender_object: bpy.types.Object)`
Set a rotation difference variable for a driver.

---

## Import/Export

Functions for importing and exporting files.

### `import_file(file_path: str, file_type: str | None = None) -> bpy.types.Object`
Import a file into Blender, supporting multiple formats.

### `export_object(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export a single object to a file.

---

## Light

Functions for creating and managing lights.

### `create_light(obj_name: str, energy_level, type)`
Create a new light object.

### `get_light(light_name: str) -> bpy.types.Light`
Get a light by name, throws if not found.

### `set_light_color(light: bpy.types.Light, r_value, g_value, b_value)`
Set the color of a light (supports 0-255 or 0.0-1.0 values).

---

## Material

Functions for creating and managing materials.

### `get_material(material_name: str) -> bpy.types.Material`
Get a material by name, throws if not found.

### `get_materials(obj_name: str) -> list[bpy.types.Material]`
Get all materials assigned to an object.

### `create_material(new_material_name: str)`
Create a new material.

### `set_material_color(material: bpy.types.Material, r_value, g_value, b_value, a_value=1.0)`
Set the color of a material (supports 0-255 or 0.0-1.0 values).

### `set_material_metallicness(material: bpy.types.Material, value: float)`
Set the metallic property of a material.

### `set_material_roughness(material: bpy.types.Material, value: float)`
Set the roughness property of a material.

### `set_material_specularness(material: bpy.types.Material, value: float)`
Set the specular intensity of a material.

### `set_material_to_object(material: bpy.types.Material, blender_object: bpy.types.Object, is_union=False)`
Assign a material to an object.

### `add_texture_to_material(material: bpy.types.Material, image_file_path: str)`
Add an image texture to a material.

---

## Mesh

Functions for creating and managing mesh data.

### `get_mesh(mesh_name: str) -> bpy.types.Mesh`
Get a mesh by name, throws if not found.

### `create_mesh(mesh_name: str, vertices: list, edges: list, faces: list) -> bpy.types.Mesh`
Create a new mesh with specified geometry.

### `get_mesh_for_object(blender_object: bpy.types.Object)`
Get the mesh data for an object.

### `remove_mesh(blender_mesh: bpy.types.Mesh)`
Remove a mesh from Blender data.

### `set_edges_mean_crease(blender_mesh: bpy.types.Mesh, mean_crease_value: float)`
Set the crease value for all edges in a mesh.

### `recalculate_normals(blender_mesh: bpy.types.Mesh)`
Recalculate face normals for a mesh.

### `is_collision_between_two_objects(blender_object1: bpy.types.Object, blender_object2: bpy.types.Object)`
Check if two objects are colliding.

### `create_kd_tree_for_object(blender_object: bpy.types.Object)`
Create a KD-tree for efficient spatial queries.

### `get_closest_face_to_vertex(blender_object: bpy.types.Object, vertex) -> bpy.types.MeshPolygon`
Find the closest face to a vertex.

### `get_closest_points_to_vertex(blender_object: bpy.types.Object, vertex, number_of_points=2, object_kd_tree=None)`
Find the closest points to a vertex using KD-tree.

### `get_bounding_box(blender_object: bpy.types.Object)`
Get the bounding box of an object.

### `separate_object(blender_object: bpy.types.Object)`
Separate loose parts of a mesh into separate objects.

---

## Modifiers

Functions for applying and managing object modifiers.

### `clear_modifiers(blender_object: bpy.types.Object)`
Remove all modifiers from an object.

### `apply_modifier(blender_object: bpy.types.Object, modifier: BlenderModifiers, **kwargs)`
Apply a modifier to an object with parameters.

### `apply_decimate_modifier(blender_object: bpy.types.Object, amount: int)`
Apply a decimate modifier to reduce mesh complexity.

### `apply_bevel_modifier(blender_object: bpy.types.Object, radius: float, vertex_group_name=None, use_edges=True, use_width=False, chamfer=False, **kwargs)`
Apply a bevel modifier for rounded edges.

### `apply_linear_pattern(blender_object: bpy.types.Object, instance_count, direction: Axis, offset: float, **kwargs)`
Create a linear array pattern.

### `apply_circular_pattern(blender_object: bpy.types.Object, instance_count: int, blender_around_object: bpy.types.Object, **kwargs)`
Create a circular array pattern.

### `apply_solidify_modifier(blender_object: bpy.types.Object, thickness: float, **kwargs)`
Apply a solidify modifier to add thickness.

### `apply_curve_modifier(blender_object: bpy.types.Object, curve_blender_object: bpy.types.Object, **kwargs)`
Apply a curve modifier to deform along a curve.

### `apply_boolean_modifier(blender_object: bpy.types.Object, blender_boolean_type: BlenderBooleanTypes, blender_boolean_object: bpy.types.Object, **kwargs)`
Apply a boolean modifier (union, difference, intersection).

### `apply_mirror_modifier(blender_object: bpy.types.Object, blender_mirror_across_object: bpy.types.Object, axis: Axis, **kwargs)`
Apply a mirror modifier across an axis.

### `apply_screw_modifier(blender_object: bpy.types.Object, angle: Angle, axis: Axis, screw_pitch: float = 0, iterations=1, blender_mirror_across_object: bpy.types.Object | None = None, resolution=16, **kwargs)`
Apply a screw modifier for helical geometry.

---

## Nodes

Functions for managing shader and geometry nodes.

### `get_node_tree(scene: bpy.types.Scene) -> bpy.types.NodeTree`
Get the node tree for a scene's world.

### `delete_nodes(scene: bpy.types.Scene)`
Clear all nodes from a scene's node tree.

### `create_nodes(scene: bpy.types.Scene, type) -> bpy.types.Node`
Create a new node in a scene's node tree.

---

## Normals

Functions for working with surface normals.

### `project_vector_along_normal(translate_vector: list, normal_vector: list)`
Project a vector along a surface normal.

---

## Objects

Functions for creating and managing Blender objects.

### `blender_primitive_function(primitive: BlenderObjectPrimitiveTypes, dimensions: list[float], **kwargs)`
Create primitive objects with specified dimensions.

### `add_primitive(primitive_type: BlenderObjectPrimitiveTypes, dimensions: list[float], **kwargs)`
Add a primitive object to the scene.

### `create_gear(name: str, outer_radius: float, addendum: float, inner_radius: float, dedendum: float, height: float, pressure_angle: float = 20.0, number_of_teeth: int = 12, skew_angle: float = 0, conical_angle: float = 0, crown_angle: float = 0)`
Create a gear object with detailed parameters.

### `make_parent(blender_object: bpy.types.Object, blender_parent_object: bpy.types.Object)`
Set parent-child relationship between objects.

### `update_object_name(blender_object: bpy.types.Object, new_name: str)`
Update an object's name.

### `get_object_collection(blender_object: bpy.types.Object) -> bpy.types.Collection`
Get the collection containing an object.

### `update_object_data_name(blender_object: bpy.types.Object, new_name: str)`
Update an object's data name (affects all objects sharing the data).

### `update_object_landmark_names(blender_object: bpy.types.Object, old_name_prefix: str, new_name_prefix: str)`
Update landmark names for an object.

### `remove_data(blender_data)`
Remove data blocks (mesh, curve, etc.) from Blender.

### `remove_object(blender_object: bpy.types.Object, remove_children=False, is_remove_data=True)`
Remove an object and optionally its children and data.

### `create_object(name: str, data: Any | None = None)`
Create a new object (exists in data but not in scene until assigned to collection).

### `create_object_vertex_group(blender_object: bpy.types.Object, vertex_group_name: str)`
Create a vertex group for an object.

### `get_object_vertex_group(blender_object: bpy.types.Object, vertex_group_name: str)`
Get a vertex group by name.

### `add_verticies_to_vertex_group(vertex_group_object, vertex_indecies: list[int])`
Add vertices to a vertex group.

### `get_object_visibility(blender_object: bpy.types.Object) -> bool`
Check if an object is visible.

### `set_object_visibility(blender_object: bpy.types.Object, is_visible: bool)`
Set object visibility.

### `get_object_local_location(blender_object: bpy.types.Object)`
Get an object's local location.

### `get_object_world_location(blender_object: bpy.types.Object)`
Get an object's world location.

### `get_object_world_pose(blender_object: bpy.types.Object) -> list[float]`
Get an object's world transformation matrix as a flat list.

### `get_object(object_name: str, of_type=None) -> bpy.types.Object`
Get an object by name, throws if not found.

### `get_object_or_none(object_name: str, of_type=None) -> bpy.types.Object | None`
Get an object by name, returns None if not found.

### `get_object_for_data(data)`
Get the first object associated with specific data.

### `get_object_type(blender_object: bpy.types.Object) -> BlenderObjectTypes`
Get the type of an object.

---

## Objects Context

Functions for object operations requiring specific context.

### `convert_object_using_ops(existing_object: bpy.types.Object, convert_to_type: BlenderObjectTypes)`
Convert an object to a different type using Blender operators.

---

## Objects Transmute

Functions for transforming and duplicating objects.

### `create_mesh_from_curve(curve_object: bpy.types.Object, new_object_name: str | None = None)`
Convert a curve object to a mesh.

### `transfer_landmarks(from_blender_object: bpy.types.Object, to_blender_object: bpy.types.Object)`
Transfer landmark objects from one object to another.

### `duplicate_object(existing_blender_object: bpy.types.Object, new_object_name: str, copy_landmarks: bool = True) -> bpy.types.Object`
Create a duplicate of an object with optional landmark copying.

---

## Render

Functions for managing render settings and operations.

### `render_image(output_filepath: str, overwrite: bool)`
Render a single image.

### `render_animation(output_filepath: str, overwrite: bool)`
Render an animation sequence.

### `set_render_frame_rate(rate: int)`
Set the render frame rate.

### `set_render_quality(percentage: int)`
Set the render quality percentage.

### `set_render_file_format(format: FileFormat)`
Set the output file format for renders.

### `set_render_engine(engine: RenderEngines)`
Set the render engine (Cycles, Eevee, etc.).

### `set_render_resolution(x: int, y: int)`
Set the render resolution.

---

## Scene

Functions for managing scene properties and settings.

### `scene_lock_interface(is_locked: bool)`
Lock or unlock the scene interface during operations.

### `set_default_unit(blender_unit: BlenderLength, scene_name="Scene")`
Set the default unit system for a scene.

### `set_background_color(scene: bpy.types.Scene, r, g, b, a)`
Set the background color of a scene.

### `set_background_image(scene: bpy.types.Scene, image_file_path: str)`
Set a background image for a scene.

### `set_background_location(scene: bpy.types.Scene, x, y)`
Set the location of the background environment texture.

### `get_scene(scene_name: str | None = "Scene") -> bpy.types.Scene`
Get a scene by name, throws if not found.

---

## Transformations

Functions for transforming objects (translate, rotate, scale).

### `apply_object_transformations(blender_object: bpy.types.Object, apply_rotation: bool, apply_scale: bool, apply_location: bool)`
Apply transformations to make them permanent.

### `rotate_object(blender_object: bpy.types.Object, rotation_angles_radians: list[float | None], rotation_type: BlenderRotationTypes)`
Rotate an object with specified angles.

### `translate_object(blender_object: bpy.types.Object, translation_dimensions: Sequence[float | None], translation_type: BlenderTranslationTypes)`
Translate an object by specified amounts.

### `set_object_location(blender_object: bpy.types.Object, location_dimensions: list[float | None])`
Set the absolute location of an object.

### `scale_object(blender_object: bpy.types.Object, x_scale_factor: float | None, y_scale_factor: float | None, z_scale_factor: float | None)`
Scale an object by specified factors.

---

## Vertex Edge Wire

Functions for working with vertices, edges, and wires at a low level.

### `create_uuid_like_id() -> str`
Generate a UUID-like string for naming objects.

### `get_vertex_location_from_blender_point(spline_point) -> Point`
Extract location from a Blender point.

### `get_vertex_from_blender_point(spline_point, edge) -> VertexInterface`
Create a CodeToCAD vertex from a Blender point.

### `get_edge_from_blender_edge(entity, edge) -> EdgeInterface`
Create a CodeToCAD edge from a Blender edge.

### `get_wire_from_blender_wire(entity, wire) -> WireInterface`
Create a CodeToCAD wire from a Blender wire.

### `get_wires_from_blender_entity(entity) -> list[WireInterface]`
Extract all wires from a Blender entity.

### `get_control_points(vertex) -> list[Point]`
Get control points for bezier vertices.

### `set_control_points(vertex, points: list[Point])`
Set control points for bezier vertices.

---

## Usage Guidelines

1. **Import Pattern**: Import specific functions you need rather than entire modules
2. **Error Handling**: Most functions include assertions and will throw descriptive errors
3. **Type Safety**: Functions use type hints for better IDE support and documentation
4. **Consistency**: All functions follow consistent naming and parameter patterns
5. **Extensibility**: Functions are designed to be extended with `**kwargs` where appropriate

## Examples

```python
# Create and configure a cube
from codetocad.adapters.blender.blender_actions.objects import add_primitive
from codetocad.adapters.blender.blender_actions.collections import assign_object_to_collection
from codetocad.adapters.blender.blender_definitions import BlenderObjectPrimitiveTypes

add_primitive(BlenderObjectPrimitiveTypes.cube, [2, 2, 2])
cube = get_object("Cube")
assign_object_to_collection(cube)

# Apply a modifier
from codetocad.adapters.blender.blender_actions.modifiers import apply_bevel_modifier
apply_bevel_modifier(cube, radius=0.1)

# Set up materials
from codetocad.adapters.blender.blender_actions.material import create_material, set_material_color, set_material_to_object
material = create_material("MyMaterial")
set_material_color(material, 255, 0, 0)  # Red
set_material_to_object(material, cube)
```

## Additional Function Details

### Import/Export Extended Functions

### `import_stl(file_path: str) -> bpy.types.Object`
Import an STL file and return the created object.

### `import_obj(file_path: str) -> bpy.types.Object`
Import an OBJ file and return the created object.

### `import_ply(file_path: str) -> bpy.types.Object`
Import a PLY file and return the created object.

### `import_x3d(file_path: str) -> bpy.types.Object`
Import an X3D file and return the created object.

### `import_dae(file_path: str) -> bpy.types.Object`
Import a DAE (Collada) file and return the created object.

### `import_fbx(file_path: str) -> bpy.types.Object`
Import an FBX file and return the created object.

### `import_gltf(file_path: str) -> bpy.types.Object`
Import a glTF file and return the created object.

### `import_abc(file_path: str) -> bpy.types.Object`
Import an Alembic file and return the created object.

### `import_usd(file_path: str) -> bpy.types.Object`
Import a USD file and return the created object.

### `import_svg(file_path: str) -> bpy.types.Object`
Import an SVG file as curves and return the created object.

### `export_stl(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to STL format.

### `export_obj(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to OBJ format.

### `export_ply(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to PLY format.

### `export_x3d(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to X3D format.

### `export_dae(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to DAE (Collada) format.

### `export_fbx(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to FBX format.

### `export_gltf(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to glTF format.

### `export_abc(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to Alembic format.

### `export_usd(blender_object: bpy.types.Object, file_path: str, overwrite=True, scale=1.0)`
Export an object to USD format.

### Extended Curve Functions

### `create_bezier_curve(curve_name: str, points: list[Point], handles_left: list[Point] | None = None, handles_right: list[Point] | None = None)`
Create a bezier curve with control handles.

### `create_nurbs_curve(curve_name: str, points: list[Point], order_u: int = 4)`
Create a NURBS curve with specified order.

### `create_poly_curve(curve_name: str, points: list[Point])`
Create a poly curve (straight line segments).

### `extrude_curve_along_path(profile_curve: bpy.types.Object, path_curve: bpy.types.Object) -> bpy.types.Object`
Extrude a profile curve along a path curve.

### `revolve_curve(curve: bpy.types.Object, axis: Axis, angle: float) -> bpy.types.Object`
Revolve a curve around an axis to create a surface.

### Extended Mesh Functions

### `create_mesh_from_vertices_faces(mesh_name: str, vertices: list[tuple], faces: list[tuple]) -> bpy.types.Mesh`
Create a mesh from vertices and face definitions.

### `triangulate_mesh(blender_mesh: bpy.types.Mesh)`
Convert all faces in a mesh to triangles.

### `smooth_mesh(blender_mesh: bpy.types.Mesh, factor: float = 0.5, iterations: int = 1)`
Apply smoothing to a mesh.

### `subdivide_mesh(blender_mesh: bpy.types.Mesh, cuts: int = 1)`
Subdivide all faces in a mesh.

### `merge_vertices(blender_mesh: bpy.types.Mesh, distance: float = 0.001)`
Merge vertices that are within the specified distance.

### `remove_doubles(blender_mesh: bpy.types.Mesh, threshold: float = 0.001)`
Remove duplicate vertices within threshold distance.

### `flip_normals(blender_mesh: bpy.types.Mesh)`
Flip the direction of all face normals.

### Extended Material Functions

### `create_pbr_material(name: str, base_color: tuple = (0.8, 0.8, 0.8, 1.0), metallic: float = 0.0, roughness: float = 0.5) -> bpy.types.Material`
Create a PBR (Physically Based Rendering) material with standard properties.

### `add_normal_map_to_material(material: bpy.types.Material, normal_map_path: str, strength: float = 1.0)`
Add a normal map texture to a material.

### `add_roughness_map_to_material(material: bpy.types.Material, roughness_map_path: str)`
Add a roughness map texture to a material.

### `add_metallic_map_to_material(material: bpy.types.Material, metallic_map_path: str)`
Add a metallic map texture to a material.

### `add_emission_to_material(material: bpy.types.Material, color: tuple = (1.0, 1.0, 1.0, 1.0), strength: float = 1.0)`
Add emission properties to a material.

### Extended Animation Functions

### `create_animation_action(name: str) -> bpy.types.Action`
Create a new animation action.

### `set_object_animation_action(blender_object: bpy.types.Object, action: bpy.types.Action)`
Assign an animation action to an object.

### `add_location_keyframe(blender_object: bpy.types.Object, frame: int, location: tuple)`
Add a location keyframe at a specific frame.

### `add_rotation_keyframe(blender_object: bpy.types.Object, frame: int, rotation: tuple)`
Add a rotation keyframe at a specific frame.

### `add_scale_keyframe(blender_object: bpy.types.Object, frame: int, scale: tuple)`
Add a scale keyframe at a specific frame.

### `set_keyframe_interpolation(blender_object: bpy.types.Object, data_path: str, interpolation_type: str)`
Set the interpolation type for keyframes.

## Performance Considerations

- **Batch Operations**: When performing multiple operations, consider using `scene_lock_interface(True)` to prevent UI updates
- **Memory Management**: Use `remove_object()` and `remove_data()` to clean up unused objects and data
- **Update Calls**: Use `update_view_layer()` and `apply_dependency_graph()` when needed to ensure data consistency
- **Context Management**: Some operations require specific context; use context functions when needed

## Error Handling Patterns

Most functions follow these error handling patterns:

1. **Assertion Errors**: For invalid parameters or missing required data
2. **KeyError/AttributeError**: For missing Blender objects or properties
3. **Exception**: For general operation failures with descriptive messages
4. **None Returns**: Functions ending with `_or_none` return None instead of throwing

## Type System

The API uses Blender's type system and CodeToCAD enums:

- `bpy.types.*`: Native Blender types
- `BlenderObjectTypes`: Object type enumeration
- `BlenderModifiers`: Modifier type enumeration
- `BlenderCurveTypes`: Curve type enumeration
- `BlenderBooleanTypes`: Boolean operation enumeration
- `Axis`: Axis enumeration for transformations
- `Point`: CodeToCAD point class

This API provides a comprehensive, type-safe interface to Blender's functionality while maintaining consistency and ease of use for the CodeToCAD adapter.
