import bpy

def onReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {}".format(update.id.name))

bpy.app.handlers.depsgraph_update_post.append(onReceiveBlenderDependencyGraphUpdateEvent)