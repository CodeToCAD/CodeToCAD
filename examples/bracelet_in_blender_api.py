import bpy
import math
import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))


bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"

collection_name = "BraceletApi"
if collection_name in bpy.data.collections:
    for obj in bpy.data.collections[collection_name].objects:
        bpy.data.objects.remove(obj)
    bpy.data.collections.remove(bpy.data.collections[collection_name])

collection = bpy.data.collections.new(collection_name)
bpy.context.scene.collection.children.link(collection)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[
    collection_name]

# in mm
measurements = {
    "bracelet": {
        "outerDiameter": 161,
        "innerDiameter": 81,
        "thickness": 83
    },
    "button": {
        "diameter": 60,
        "depth": 13.6
    },
    "buttonInner": {
        "diameter": 40,
        "depth": 5
    }
}

bpy.ops.mesh.primitive_torus_add(mode='EXT_INT', abso_major_rad=(
    measurements["bracelet"]["outerDiameter"]/2), abso_minor_rad=(measurements["bracelet"]["innerDiameter"]/2))
bpy.data.objects[-1].name = "bracelet"

bpy.ops.mesh.primitive_torus_add(mode='EXT_INT', abso_major_rad=((measurements["bracelet"]["outerDiameter"]/2)+(
    measurements["button"]["depth"]/4)), abso_minor_rad=(measurements["bracelet"]["innerDiameter"]/2))
bpy.data.objects[-1].name = "circlet"

bpy.ops.mesh.primitive_cylinder_add(radius=(
    measurements["button"]["diameter"]/4), depth=(measurements["button"]["depth"]))
bpy.data.objects[-1].name = "button"

bpy.ops.mesh.primitive_cylinder_add(radius=(
    measurements["buttonInner"]["diameter"]/4), depth=(measurements["buttonInner"]["depth"]))
bpy.data.objects[-1].name = "buttonInner"

bpy.data.objects['button'].rotation_euler = [math.radians(90), 0, 0]
buttonTranslation = (
    measurements["bracelet"]["outerDiameter"]/2) - (measurements["button"]["depth"]/2)
bpy.data.objects['button'].location = [0, buttonTranslation, 0]

bpy.data.objects['buttonInner'].rotation_euler = [math.radians(90), 0, 0]
buttonTranslation = (
    measurements["bracelet"]["outerDiameter"]/2 - measurements["buttonInner"]["depth"]/2)
bpy.data.objects['buttonInner'].location = [0, buttonTranslation, 0]

buttonBoolean = bpy.data.objects['button'].modifiers.new(
    type="EDGE_SPLIT", name="EdgeDiv")
# buttonBoolean.split_angle = math.radians(60)
buttonBoolean = bpy.data.objects['button'].modifiers.new(
    type="SUBSURF", name="Subdivision")
buttonBoolean.levels = 3

buttonInnerBoolean = bpy.data.objects['buttonInner'].modifiers.new(
    type="EDGE_SPLIT", name="EdgeDiv")
# buttonInnerBoolean.split_angle = math.radians(60)
buttonInnerBoolean = bpy.data.objects['buttonInner'].modifiers.new(
    type="SUBSURF", name="Subdivision")
buttonInnerBoolean.levels = 3


braceletBoolean = bpy.data.objects['bracelet'].modifiers.new(
    type="EDGE_SPLIT", name="EdgeDiv")
braceletBoolean.split_angle = math.radians(60)
braceletBoolean = bpy.data.objects['bracelet'].modifiers.new(
    type="SUBSURF", name="Subdivision")
braceletBoolean.levels = 3

circletBoolean = bpy.data.objects['circlet'].modifiers.new(
    type="EDGE_SPLIT", name="EdgeDiv")
circletBoolean.split_angle = math.radians(60)
circletBoolean = bpy.data.objects['circlet'].modifiers.new(
    type="SUBSURF", name="Subdivision")
circletBoolean.levels = 3

buttonBoolean = bpy.data.objects['button'].modifiers.new(
    type="BOOLEAN", name="bool 2")
buttonBoolean.object = bpy.data.objects['buttonInner']
buttonBoolean.operation = 'DIFFERENCE'

buttonBoolean = bpy.data.objects['button'].modifiers.new(
    type="BOOLEAN", name="bool 1")
buttonBoolean.object = bpy.data.objects['bracelet']
buttonBoolean.operation = 'INTERSECT'


buttonBooleanMesh = bpy.data.objects['button'].evaluated_get(
    bpy.context.evaluated_depsgraph_get()).data.copy()
bpy.data.objects['button'].modifiers.clear()

bpy.data.objects.remove(bpy.data.objects['buttonInner'])


braceletScale = measurements["bracelet"]["thickness"] / \
    bpy.data.objects['bracelet'].dimensions.z

bpy.data.objects['bracelet'].scale = [1, 1, braceletScale]
bpy.data.objects['circlet'].scale = [1, 1, braceletScale]
bpy.data.objects['button'].scale = [braceletScale, braceletScale, 1]


braceletBoolean = bpy.data.objects['bracelet'].modifiers.new(
    type="BOOLEAN", name="DIFFERENCE")
braceletBoolean.object = bpy.data.objects['button']
braceletBoolean.operation = 'DIFFERENCE'

braceletBooleanMesh = bpy.data.objects['bracelet'].evaluated_get(
    bpy.context.evaluated_depsgraph_get()).data.copy()
bpy.data.objects['bracelet'].modifiers.clear()

circletBoolean = bpy.data.objects['circlet'].modifiers.new(
    type="BOOLEAN", name="DIFFERENCE")
circletBoolean.object = bpy.data.objects['button']
circletBoolean.operation = 'DIFFERENCE'

circletBooleanMesh = bpy.data.objects['circlet'].evaluated_get(
    bpy.context.evaluated_depsgraph_get()).data.copy()
bpy.data.objects['circlet'].modifiers.clear()

# apply modified meshes:
bpy.data.objects['bracelet'].data = braceletBooleanMesh
bpy.data.objects['circlet'].data = circletBooleanMesh
bpy.data.objects['button'].data = buttonBooleanMesh
