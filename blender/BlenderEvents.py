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

    def startBlenderEventTimer(self, bpy):
        blenderEventsHandler = self.BlenderEventsHandler(self)
        bpy.app.timers.register(blenderEventsHandler.processEventsAndOperations)

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

        blenderEventsHandler = self.BlenderEventsHandler(self)

        while 1:
            sleep(blenderEventsHandler.processEventsAndOperations())
        

    # onReceiveBlenderDependencyGraphUpdateEvent is called when we receive an event from blender.
    def onReceiveBlenderDependencyGraphUpdateEvent(self, scene, depsgraph):
        
        for update in depsgraph.updates:
            self.blenderEventQueueLock.acquire()
            self.blenderEventQueue.append(update)
            self.blenderEventQueueLock.release()
    
    class BlenderEventsHandler:
        currentBlenderEvent = None
        remainingEventsCount = 0
        currentOperation = None
        remainingOperationsCount = 0

        defaultShortDelay = 0.1 #100ms thread sleep for this thread so other threads can do things
        defaultLongDelay = 1.0

        # Requires a BlenderEvents instance to be passed to this
        def __init__(self, blenderEvents):
            self.blenderEvents = blenderEvents

        # Processes the BlenderEvents's blenderEventsQueue and blenderOperationsQueue
        # Returns a float equal to the amount of time a thread should sleep before processing the next event and operation.
        def processEventsAndOperations(self):
            if self.currentBlenderEvent == None:
                (self.currentBlenderEvent, self.remainingEventsCount) = self.blenderEvents.popFirstFromBlenderEventQueue()

            currentOperationStartFunction = None

            if self.currentOperation == None:

                (self.currentOperation, self.remainingOperationsCount) = self.blenderEvents.popFirstFromBlenderOperationsQueue()

                if (self.currentOperation != None and "operation" in self.currentOperation):

                    currentOperationStartFunction = self.currentOperation["operation"]

                elif self.currentOperation != None:

                    print(
    """

    Operation is missing its start function: {}

    """
                        .format( self.currentOperation["description"])
                    )

                    self.currentOperation = None

                    return self.defaultShortDelay



            # the operation object has an "operation" key that's a callback to start the operation, we should call exactly once to fire off the operation in Blender
            if currentOperationStartFunction != None:

                # If we fail to dispatch the start function, dismiss the operation
                if currentOperationStartFunction() == False:
                    print(
    """

    Failed to start operation {}

    """
                        .format( self.currentOperation["description"])
                    )

                    self.currentOperation = None
                    return self.defaultShortDelay

                else:
                    print(
    """

    Starting operation: {}

    """
                        .format( self.currentOperation["description"])
                    )

            # If there are no operations, dismiss the event
            if self.currentOperation == None:

                self.currentBlenderEvent = None

            # If there are no events, put the thread to sleep
            if self.currentBlenderEvent == None:

                return self.defaultLongDelay

            print(
                """ 
    Received Update Event From Blender: {} Type: {}
    CurrentOperationsCount: {}
    RemainingOperation: {}
    RemainingEventsCount: {}
                """.format(
                    self.currentBlenderEvent.id.name, type(self.currentBlenderEvent.id),
                    self.currentOperation["description"],
                    self.remainingOperationsCount,
                    self.remainingEventsCount
                    )
            )
            
            currentOperationAssertionFunction = self.currentOperation["assertion"]

            # If we receive an update that an operation was complete, dimiss the event and the operation. Otherwise, dimiss the event and keep waiting for the operation to be
            if currentOperationAssertionFunction(self.currentBlenderEvent) == True:
                print(
    """

    Assertion complete for operation: {}

    """
                    .format( self.currentOperation["description"])
                )
                self.currentBlenderEvent = None
                self.currentOperation = None

            else:
                
                self.currentBlenderEvent = None
            
            return self.defaultShortDelay