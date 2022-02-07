from threading import Event, Thread
from time import sleep
import bpy


blenderOperationsComplete = Event()
blenderOperations = []

def addBlenderOperation(description, operation, assertion):
    global blenderOperations,blenderOperationsComplete

    blenderOperationsComplete.clear()

    blenderOperations.append(
        {
            "started": False,
            "description": description,
            "operation": operation,
            "assertion": assertion
        }
    )

    if len(blenderOperations) == 1:
        operation()

updateEventQueue = []

def updateEventHandler():
    global blenderOperations,blenderOperationsComplete, updateEventQueue
    while 1:
        sleep(0.5)
        if len(updateEventQueue) == 0:
            return
        
        update = updateEventQueue.pop(0)

        if len(blenderOperations) == 0:
            return
        
        operation = blenderOperations[0]

        print("update:", update.id.name, type(update.id), "transformOperation:", update.is_updated_transform,"geometryOperation:", update.is_updated_geometry, "currentOperation:", operation["description"], "Operations left:", len(blenderOperations))
        
        if operation["assertion"](update):
            print("assertion complete:", operation["description"])
            blenderOperations.pop(0)
            if len(blenderOperations) == 0:
                print("All operations complete")
                blenderOperationsComplete.set()
            else:    
                operation = blenderOperations[0]
                operation["operation"]()
                
Thread(target=updateEventHandler).start()

def on_depsgraph_update(scene, depsgraph):

    global updateEventQueue
    
    for update in depsgraph.updates:
        updateEventQueue.append(update)
  
bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)