import bpy
from CodeToCAD import *
import BlenderActions

# Override context while stroke is applied
# https://github.com/christian-vorhemus/procedural-3d-image-generation/blob/master/blenderBackgroundTask.py#L54


def context_override():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {'window': window, 'screen': screen, 'area': area, 'region': region, 'scene': bpy.context.scene}


# Clear all objects
try:
    bpy.ops.object.mode_set(mode='OBJECT')
except:
    pass
for obj in bpy.context.scene.objects:
    obj.select_set(True)
bpy.ops.object.delete()

# Create basic ico_sphere with 7 subdivisions
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=7)
bpy.ops.object.mode_set(mode='SCULPT')
bpy.data.objects[0].select_set(True)
bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False

# Define path of stroke
num_steps = 10
steps = range(0, 10)
points = []
for i, s in enumerate(steps):
    px = i
    py = s
    pz = 0
    points.append([px, py, pz])

# Define stroke parameters
strokes = []
for i, p in enumerate(points):
    stroke = {
        "name": "stroke",
        "mouse": (0, 0),
        "pen_flip": False,
        "is_start": True if i == 0 else False,
        "location": p,
        "size": 0.5,
        "pressure": 1.0,
        "time": float(i),
        "mouse_event": (0, 0),
        "x_tilt": 0,
        "y_tilt": 0}
    strokes.append(stroke)

# Set brush settings
bpy.data.scenes["Scene"].tool_settings.unified_paint_settings.use_locked_size = "SCENE"
bpy.data.scenes["Scene"].tool_settings.unified_paint_settings.unprojected_radius = 0.5


# Uncomment line bellow to switch between BLOB brush and CLOTH brush
bpy.ops.paint.brush_select(sculpt_tool='CLOTH', toggle=False)
# bpy.ops.paint.brush_select(sculpt_tool='BLOB', toggle=False)

# More brush settings
bpy.data.brushes["Blob"].strength = 0.5
bpy.data.brushes["Blob"].curve_preset = "SMOOTH"
bpy.data.brushes["Blob"].auto_smooth_factor = 1.0

# Apply stroke
bpy.ops.sculpt.brush_stroke(context_override(), stroke=strokes)
