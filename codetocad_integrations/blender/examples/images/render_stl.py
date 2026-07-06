"""Render an STL to a PNG product shot using Blender's Cycles engine.

Usage (inside blender --background):
    blender --background --factory-startup --python render_stl.py -- in.stl out.png [r g b]
"""
import sys
import math
import mathutils
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
stl_path, png_path = argv[0], argv[1]
color = tuple(float(c) for c in argv[2:5]) if len(argv) >= 5 else (0.62, 0.66, 0.7)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

bpy.ops.wm.stl_import(filepath=stl_path)
obj = bpy.context.selected_objects[0]
obj.name = "part"

# Smooth shading with an auto-smooth-ish look via edge split for hard edges.
for poly in obj.data.polygons:
    poly.use_smooth = True
edge_split = obj.modifiers.new("EdgeSplit", "EDGE_SPLIT")
edge_split.split_angle = math.radians(45)

mat = bpy.data.materials.new("part_mat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (*color, 1.0)
bsdf.inputs["Roughness"].default_value = 0.35
if "Metallic" in bsdf.inputs:
    bsdf.inputs["Metallic"].default_value = 0.15
obj.data.materials.append(mat)

# Frame the object: center it, then place camera on an isometric-ish
# direction at a distance derived from its bounding sphere.
bbox_corners = [obj.matrix_world @ mathutils.Vector(c) for c in obj.bound_box]
minv = mathutils.Vector((min(c[i] for c in bbox_corners) for i in range(3)))
maxv = mathutils.Vector((max(c[i] for c in bbox_corners) for i in range(3)))
center = (minv + maxv) / 2
radius = max((maxv - minv).length / 2, 1e-4)

obj.location -= center

direction = mathutils.Vector((1.6, -1.9, 1.3)).normalized()
distance = radius / math.tan(math.radians(20)) + radius
cam_data = bpy.data.cameras.new("cam")
cam_data.lens_unit = "FOV"
cam_data.angle = math.radians(40)
cam_data.clip_start = distance / 1000
cam_data.clip_end = distance * 100
cam_obj = bpy.data.objects.new("cam", cam_data)
cam_obj.location = direction * distance
rot_quat = direction.to_track_quat("Z", "Y")
cam_obj.rotation_euler = rot_quat.to_euler()
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Three-point-ish lighting: a key sun plus a soft fill area light.
key = bpy.data.lights.new("key", type="SUN")
key.energy = 1.2
key_obj = bpy.data.objects.new("key", key)
key_obj.location = direction * distance + mathutils.Vector((0, 0, radius * 2))
key_obj.rotation_euler = rot_quat.to_euler()
scene.collection.objects.link(key_obj)

fill = bpy.data.lights.new("fill", type="AREA")
fill.energy = radius * radius * 30.0
fill.size = radius * 4
fill_dir = mathutils.Vector((-1.2, 1.6, 0.8)).normalized()
fill_obj = bpy.data.objects.new("fill", fill)
fill_obj.location = fill_dir * distance * 1.3
fill_obj.rotation_euler = fill_dir.to_track_quat("Z", "Y").to_euler()
scene.collection.objects.link(fill_obj)

scene.world = bpy.data.worlds.new("world")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.97, 0.97, 0.98, 1.0)
bg.inputs[1].default_value = 0.5

scene.view_settings.view_transform = "Standard"

scene.render.engine = "CYCLES"
scene.cycles.samples = 128
scene.cycles.use_denoising = True
try:
    scene.cycles.device = "GPU"
except Exception:
    pass
scene.render.resolution_x = 1000
scene.render.resolution_y = 800
scene.render.film_transparent = False
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = png_path

bpy.ops.render.render(write_still=True)
print("RENDERED", png_path)
