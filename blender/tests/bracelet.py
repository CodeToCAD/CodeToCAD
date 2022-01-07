import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))


import bpy
from utilities import Dimension, Units, getDimensionsFromString

collectionName = "Bracelet"
if collectionName in bpy.data.collections:
    bpy.data.collections.remove(bpy.data.collections[collectionName])
collection = bpy.data.collections.new(collectionName)
bpy.context.scene.collection.children.link(collection)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collectionName]

bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), major_segments=48, minor_segments=12, mode='MAJOR_MINOR', major_radius=1.0, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75, generate_uvs=True)
bpy.data.objects[-1].name = "bracelet"
