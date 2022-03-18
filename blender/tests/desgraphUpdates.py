import bpy

def onReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {} type {}".format(update.id.name, type(update.id)))

bpy.app.handlers.depsgraph_update_post.append(onReceiveBlenderDependencyGraphUpdateEvent)