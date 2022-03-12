import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

def onReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {}".format(update.id.name))

bpy.app.handlers.depsgraph_update_post.append(onReceiveBlenderDependencyGraphUpdateEvent)