import bpy
from CodeToCAD import *
import BlenderActions

# Part("UglySinSphere").createSphere(5).remesh(
#     strategy="edgesplit", amount=7).apply()

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=7)
bpy.ops.object.mode_set(mode='SCULPT')
bpy.data.objects[0].select_set(True)
bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False

bpy.ops.object.mode_set(mode='SCULPT')
bpy.ops.code_to_cad.log_message(message="Line 8")


num_steps = 5
steps = range(0, 10)
points = []
for i, s in enumerate(steps):
    px = i
    py = s
    pz = 0  # np.sin(s)*np.cos(s)
    points.append([px, py, pz])
    # we need a way to figure out what px py pz and i,s are. i'm pretty sure
    # i know what i,s are but it doesn't hurt to check...maybe throw thru IDLE?

correct_points = [[0.0, 1.0, 0], [0.3090169943749474, 0.9510565162951535, 0], [0.5877852522924731, 0.8090169943749475, 0], [
    0.8090169943749475, 0.5877852522924731, 0], [0.9510565162951535, 0.30901699437494745, 0]]

strokes = []
for i, p in enumerate(points):
    stroke = {
        "name": "stroke",
        "mouse": (0, 0),
        "pen_flip": False,
        "is_start": True if i == 0 else False,
        "location": p,
        "size": 10,
        "pressure": 1.0,
        "time": float(i),
        "mouse_event": (0, 0),
        "x_tilt": 0,
        "y_tilt": 0}
    strokes.append(stroke)

'''
strokes = []
for i, p in enumerate(points):
    stroke = {
        "name": "stroke",
        "mouse": (0, 0),
        "mouse_event": (0, 0),
        "pen_flip": False,
        "is_start": True
        if i == 0 else False,
        "location": p,
        "size": 10.0,
        "pressure": 1.0,
        "time": float(i),
        "x_tilt": 0.0,
        "y_tilt": 0.0,
    }
    strokes.append(stroke)

print(strokes)

tester = [{
    "name": "stroke",
    "mouse": (0, 0),
    "mouse_event": (0, 0),
    "pen_flip": False,
    "is_start": True,  # if i==0 else False,
    "location": (1, 1, 1),
    "size": 10.0,
    "pressure": 1.0,
    "time": 0,
    "x_tilt": 0.0,
    "y_tilt": 0.0,
}, {
    "name": "stroke",
    "mouse": (0, 0),
    "mouse_event": (0, 0),
    "pen_flip": False,
    "is_start": False,  # if i==0 else False,
    "location": (2, 2, 1),
    "size": 10.0,
    "pressure": 1.0,
    "time": 1,
    "x_tilt": 0.0,
    "y_tilt": 0.0,
}]
'''

# bpy.ops.object.mode_set(mode='SCULPT')
# bpy.ops.code_to_cad.log_message(message="No more line 39.")

# Set brush settings
bpy.data.scenes["Scene"].tool_settings.unified_paint_settings.use_locked_size = "SCENE"
bpy.data.scenes["Scene"].tool_settings.unified_paint_settings.unprojected_radius = 0.50

bpy.ops.paint.brush_select(sculpt_tool='BLOB', toggle=False)
# bpy.ops.paint.brush_select(sculpt_tool='CLOTH', toggle=False)
bpy.data.brushes["Blob"].strength = 1
bpy.data.brushes["Blob"].curve_preset = "SMOOTH"
bpy.data.brushes["Blob"].auto_smooth_factor = 1.0

# strokeArray = [{'name': 'stroke', 'mouse': (0, 0), 'pen_flip': False, 'is_start': True, 'location': [0, 0, 0], 'size': 1.0, 'pressure': 1.0, 'time': 0.0}]
# Apply stroke
bpy.ops.sculpt.brush_stroke(stroke=strokes)
# bpy.ops.sculpt.brush_stroke(BlenderActions.getContext(), stroke=strokes)
