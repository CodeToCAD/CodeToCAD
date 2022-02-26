from threading import Event, Thread, Lock
from time import sleep

class BlenderEvents:
    # blenderEventQueue is updated when we receive an event from Blender
    blenderEventQueueLock = Lock()
    blenderEventQueue = []
    #self.blenderOperationsQueue is used to keep track of operations we want to send to Blender.
    blenderOperationsComplete = Event()
    blenderOperationsQueueLock = Lock()
    blenderOperationsQueue = []

    def startBlenderEventThread(self):
        Thread(target=self.blenderEventThread).start()

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

    # Returns the first item from the BlenderOperationsQueue. Note: Uses a thread Lock.
    def popFirstFromBlenderOperationsQueue(self):
        
        blenderOperation = None

        self.blenderOperationsQueueLock.acquire()

        remainingOperationsCount = len(self.blenderOperationsQueue)
        
        if remainingOperationsCount > 0:
            blenderOperation = self.blenderOperationsQueue.pop(0)
            remainingOperationsCount -= 1
        
        self.blenderOperationsQueueLock.release()

        return (blenderOperation, remainingOperationsCount)

    # Returns the length of the BlenderOperationsQueue. Note: Uses a thread Lock.
    def getLengthOfBlenderOperationsQueue(self):
        
        count = 0

        self.blenderOperationsQueueLock.acquire()
        
        count = len(self.blenderOperationsQueue)
        
        self.blenderOperationsQueueLock.release()

        return count


    # Returns the first item from the BlenderEventQueue. Note: Uses a thread Lock.
    def popFirstFromBlenderEventQueue(self):
        
        blenderEvent = None

        self.blenderEventQueueLock.acquire()
        
        remainingEventsCount = len(self.blenderEventQueue)
        
        if len(self.blenderEventQueue) > 0:
            blenderEvent = self.blenderEventQueue.pop(0)
            remainingEventsCount -= 1
        
        self.blenderEventQueueLock.release()

        return (blenderEvent, remainingEventsCount)

    # blenderEventThread is a thread that runs forever and is used to handle actions when we receive an event from Blender (which are stored in blenderEventQueue)
    def blenderEventThread(self):

        currentBlenderEvent = None
        remainingEventsCount = 0
        currentOperation = None
        remainingOperationsCount = 0

        while 1:
            sleep(0.1) #100ms thread sleep for this thread so other threads can do things
            if currentBlenderEvent == None:
                (currentBlenderEvent, remainingEventsCount) = self.popFirstFromBlenderEventQueue()

            currentOperationStartFunction = None

            if currentOperation == None:

                (currentOperation, remainingOperationsCount) = self.popFirstFromBlenderOperationsQueue()

                if (currentOperation != None and "operation" in currentOperation):

                    currentOperationStartFunction = currentOperation["operation"]

                elif currentOperation != None:

                    print(
"""

Operation is missing its start function: {}

"""
                        .format( currentOperation["description"])
                    )

                    currentOperation = None
                    continue



            # the operation object has an "operation" key that's a callback to start the operation, we should call exactly once to fire off the operation in Blender
            if currentOperationStartFunction != None:

                # If we fail to dispatch the start function, dismiss the operation
                if currentOperationStartFunction() == False:
                    print(
"""

Failed to start operation {}

"""
                        .format( currentOperation["description"])
                    )

                    currentOperation = None
                    continue

                else:
                    print(
"""

Starting operation: {}

"""
                        .format( currentOperation["description"])
                    )

            # If there are no operations, dismiss the event
            if currentOperation == None:

                currentBlenderEvent = None

            # If there are no events, put the thread to sleep
            if currentBlenderEvent == None:
                sleep(1)
                continue

            print(
                """ 
Received Update Event From Blender: {} Type: {}
CurrentOperationsCount: {}
Remaininperation: {}
RemainingEventsCount: {}
                """.format(
                    currentBlenderEvent.id.name, type(currentBlenderEvent.id),
                    currentOperation["description"],
                    remainingOperationsCount,
                    remainingEventsCount
                    )
            )
            
            currentOperationAssertionFunction = currentOperation["assertion"]

            # If we receive an update that an operation was complete, dimiss the event and the operation. Otherwise, dimiss the event and keep waiting for the operation to be
            if currentOperationAssertionFunction(currentBlenderEvent) == True:
                print(
"""

Assertion complete for operation {}

"""
                    .format( currentOperation["description"])
                )
                currentBlenderEvent = None
                currentOperation = None

            else:
                
                currentBlenderEvent = None


    # onReceiveBlenderDependencyGraphUpdateEvent is called when we receive an event from blender.
    def onReceiveBlenderDependencyGraphUpdateEvent(self, scene, depsgraph):
        
        for update in depsgraph.updates:
            self.blenderEventQueueLock.acquire()
            self.blenderEventQueue.append(update)
            self.blenderEventQueueLock.release()