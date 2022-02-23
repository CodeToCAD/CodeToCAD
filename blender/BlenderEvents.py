from threading import Event, Thread, Lock
from time import sleep

class BlenderEvents:
    # updateEventQueue is updated when we receive an event from Blender
    updateEventQueueLock = Lock()
    updateEventQueue = []
    #self.blenderOperationsQueue is used to keep track of operations we want to send to Blender.
    blenderOperationsComplete = Event()
    blenderOperationsQueueLock = Lock()
    blenderOperationsQueue = []

    def startUpdateEventThread(self):
        Thread(target=self.updateEventThread).start()

    # addBlenderOperation adds a callback operation to the self.blenderOperationsQueue queue
    # TODO: add locks to prevent multithreading issues while accessing self.blenderOperationsQueue queue
    def addBlenderOperation(self, description, operation, assertion):

        self.blenderOperationsComplete.clear()

        self.blenderOperationsQueue.append(
            {
                "started": False,
                "description": description,
                "operation": operation,
                "assertion": assertion
            }
        )

        if len(self.blenderOperationsQueue) == 1:
            operation()

    # updateEventThread is a thread that runs forever and is used to handle actions when we receive an event from Blender (which are stored in updateEventQueue)
    def updateEventThread(self):

        while 1:
            if len(self.updateEventQueue) == 0:
                sleep(1)
                continue

            self.updateEventQueueLock.acquire()
            update = self.updateEventQueue.pop(0)
            self.updateEventQueueLock.release()

            if len(self.blenderOperationsQueue) == 0:
                continue
            
            operation = self.blenderOperationsQueue[0]

            print("update:", update.id.name, type(update.id), "transformOperation:", update.is_updated_transform,"geometryOperation:", update.is_updated_geometry, "currentOperation:", operation["description"], "Operations left:", len(self.blenderOperationsQueue))
            
            if operation["assertion"](update):
                print("assertion complete:", operation["description"])
                self.blenderOperationsQueue.pop(0)
                if len(self.blenderOperationsQueue) == 0:
                    print("All operations complete")
                    self.blenderOperationsComplete.set()
                else:    
                    operation = self.blenderOperationsQueue[0]
                    operation["operation"]()



    # onReceiveBlenderDependencyGraphUpdate is called when we receive an event from blender.
    def onReceiveBlenderDependencyGraphUpdate(self, scene, depsgraph):
        
        for update in depsgraph.updates:
            self.updateEventQueueLock.acquire()
            self.updateEventQueue.append(update)
            self.updateEventQueueLock.release()