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

    # addToBlenderOperationsQueue adds a callback operation to the self.blenderOperationsQueue queue. Note: Uses a thread Lock.
    def addToBlenderOperationsQueue(self, description, operation, assertion):

        # reset threading Event
        self.blenderOperationsComplete.clear()

        self.blenderOperationsQueueLock.acquire()

        self.blenderOperationsQueue.append(
            {
                "started": False,
                "description": description,
                "operation": operation,
                "assertion": assertion
            }
        )

        self.blenderOperationsQueueLock.release()

        if len(self.blenderOperationsQueue) == 1:
            operation()
    
    # Removes the first item from the BlenderOperationsQueue and returns it Note: Uses a thread Lock.
    def removeFirstFromBlenderOperationsQueue(self):
        
        blenderOperation = None

        self.blenderOperationsQueueLock.acquire()
        
        if len(self.blenderOperationsQueue) > 0:
            blenderOperation = self.blenderOperationsQueue.pop(0)
        
        self.blenderOperationsQueueLock.release()

        return blenderOperation

    # Returns the first item from the BlenderOperationsQueue. Note: Uses a thread Lock.
    def getFirstFromBlenderOperationsQueue(self):
        
        blenderOperation = None

        self.blenderOperationsQueueLock.acquire()
        
        if len(self.blenderOperationsQueue) > 0:
            blenderOperation = self.blenderOperationsQueue[0]
        
        self.blenderOperationsQueueLock.release()

        return blenderOperation

    # Returns the length of the BlenderOperationsQueue. Note: Uses a thread Lock.
    def getLengthOfBlenderOperationsQueue(self):
        
        count = 0

        self.blenderOperationsQueueLock.acquire()
        
        count = len(self.blenderOperationsQueue)
        
        self.blenderOperationsQueueLock.release()

        return count

    # updateEventThread is a thread that runs forever and is used to handle actions when we receive an event from Blender (which are stored in updateEventQueue)
    def updateEventThread(self):

        while 1:
            if len(self.updateEventQueue) == 0:
                sleep(1)
                continue

            self.updateEventQueueLock.acquire()
            update = self.updateEventQueue.pop(0)
            self.updateEventQueueLock.release()


            blenderOperationQueueCount = self.getLengthOfBlenderOperationsQueue()
            
            operation = self.getFirstFromBlenderOperationsQueue()

            if operation == None:
                continue

            print("update:", update.id.name, type(update.id), "transformOperation:", update.is_updated_transform,"geometryOperation:", update.is_updated_geometry, "currentOperation:", operation["description"], "Operations left:", blenderOperationQueueCount)
            
            if operation["assertion"](update):
                print("assertion complete:", operation["description"])
                
                runNextOperation = True
                while runNextOperation:
                    self.removeFirstFromBlenderOperationsQueue()

                    operation = self.getFirstFromBlenderOperationsQueue()

                    if operation == None:
                        print("All operations complete")
                        self.blenderOperationsComplete.set()
                    else:    

                        print("Starting operation", operation["description"])

                        if operation["operation"]():
                            runNextOperation = False
                        else:
                            print("Skipping operation", operation["description"])




    # onReceiveBlenderDependencyGraphUpdate is called when we receive an event from blender.
    def onReceiveBlenderDependencyGraphUpdate(self, scene, depsgraph):
        
        for update in depsgraph.updates:
            self.updateEventQueueLock.acquire()
            self.updateEventQueue.append(update)
            self.updateEventQueueLock.release()