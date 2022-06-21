from threading import Event, Thread, Lock, Timer
from time import sleep

class BlenderEvents:
    # blenderEventQueue is updated when we receive an event from Blender
    blenderEventQueueLock = Lock()
    blenderEventQueue = []
    #self.blenderOperationsQueue is used to keep track of operations we want to send to Blender.
    blenderOperationsComplete = Event()
    blenderOperationsQueueLock = Lock()
    blenderOperationsQueue = []

    isWaitForAssertionsEnabled = True

    def startBlenderEventThread(self):
        Thread(target=self.blenderEventThread).start()

    def startBlenderEventTimer(self, bpy):
        blenderEventsHandler = self.BlenderEventsHandler(self)
        bpy.app.timers.register(blenderEventsHandler.processEventsAndOperations)

    # addToBlenderOperationsQueue adds a callback operation to the self.blenderOperationsQueue queue. Note: Uses a thread Lock.
    def addToBlenderOperationsQueue(self, description, operation, assertion, timeout = 60):

        # reset threading Event
        self.blenderOperationsComplete.clear()

        self.blenderOperationsQueueLock.acquire()

        self.blenderOperationsQueue.append(
            {
                "started": False,
                "description": description,
                "operation": operation,
                "assertion": assertion,
                "timeout": timeout
            }
        )

        self.blenderOperationsQueueLock.release()

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
        
    def clearBlenderOperationsQueue(self):

        self.blenderOperationsQueueLock.acquire()
        
        self.blenderOperationsQueue = []
        
        self.blenderOperationsQueueLock.release()

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
            if update.id == None:
                print("Received an update without an id: {}", update)
                continue
            self.blenderEventQueueLock.acquire()
            self.blenderEventQueue.append(update)
            self.blenderEventQueueLock.release()
    
    class BlenderEventsHandler:
        currentBlenderEvent = None
        remainingEventsCount = 0
        currentOperation = None
        remainingOperationsCount = 0

        timeoutTimer = Timer(60.0, None)
        timeoutLock = Lock()

        # Make sure any methods that use this lock don't call each other so there is no deadlock
        def useTimeOutLock(timeoutLockUser):
            def wrapper(*args, **kwargs):
                [self] = args

                if self:
                    self.timeoutLock.acquire()

                output = timeoutLockUser(*args, **kwargs)

                if self:
                    self.timeoutLock.release()
                
                return output
                
            return wrapper

        defaultShortDelay = 0.001 #1ms thread sleep for this thread so other threads can do things
        defaultLongDelay = 1.0

        # Requires a BlenderEvents instance to be passed to this
        def __init__(self, blenderEvents):
            self.blenderEvents = blenderEvents

        def operationStarted(self):
            print(
"""

Starting operation: {}

"""
                .format( self.currentOperation["description"])
            )

            self.timeoutTimer = Timer(
                self.currentOperation["timeout"],
                self.triggerTimeout
                )
            self.timeoutTimer.start()

        def operationCompleted(self):
            print(
"""

Completed Operation: {}

"""
                .format( self.currentOperation["description"])
            )
            self.currentOperation = None
            
            self.timeoutTimer.cancel()

            return self.defaultShortDelay

        def operationFailed(self, errorMessage, clearOperationsQueue):
            print(
"""

Failed Operation: {}, Reason: {}

"""
                .format( self.currentOperation["description"], errorMessage)
            )

            self.currentOperation = None

            if clearOperationsQueue:

                self.blenderEvents.clearBlenderOperationsQueue()

                self.remainingEventsCount = 0
                
            return self.defaultShortDelay



        @useTimeOutLock
        def triggerTimeout(self):
            # Note: when operation times out here, we clear the operations queue because we are assuming a fatal error. However, this flow is inconsistent with the "skip operation" flow when an operation fails to start. Perhaps there could be a "fatalIfFails" flag, but there's currently no way to pass that in.
            self.operationFailed("Timeout Triggered", True)

        # Processes the BlenderEvents's blenderEventsQueue and blenderOperationsQueue
        # Returns a float equal to the amount of time a thread should sleep before processing the next event and operation.
        @useTimeOutLock
        def processEventsAndOperations(self):

            if self.currentBlenderEvent == None:
                (self.currentBlenderEvent, self.remainingEventsCount) = self.blenderEvents.popFirstFromBlenderEventQueue()

            currentOperationStartFunction = None

            if self.currentOperation == None:

                (self.currentOperation, self.remainingOperationsCount) = self.blenderEvents.popFirstFromBlenderOperationsQueue()

                if (self.currentOperation != None and "operation" in self.currentOperation):

                    currentOperationStartFunction = self.currentOperation["operation"]

                elif self.currentOperation != None:
                    
                    return self.operationFailed("Operation is missing its start function", False)

            # the operation object has an "operation" key that's a callback to start the operation, we should call exactly once to fire off the operation in Blender
            if currentOperationStartFunction != None:

                # If we fail to dispatch the start function, dismiss the operation
                try:
                    currentOperationStartFunction()

                    self.operationStarted()
               
                except Exception as e:
                    
                    return self.operationFailed(e, False)

            # If there are no operations, dismiss the event
            if self.currentOperation == None:

                self.currentBlenderEvent = None

                return self.defaultLongDelay

            currentOperationAssertionFunction = self.currentOperation["assertion"]

            # if the operation doesn't have an assertion, call completion right away
            if currentOperationAssertionFunction == None or not self.blenderEvents.isWaitForAssertionsEnabled:
                
                return self.operationCompleted()


            # If there are no events, put the thread to sleep
            if self.currentBlenderEvent == None:

                return self.defaultLongDelay

            print(
                """ 
Received Update Event From Blender: {} Type: {}
CurrentOperation: {}
RemainingOperation: {}
RemainingEventsCount: {}
                """.format(
                    self.currentBlenderEvent.id.name, type(self.currentBlenderEvent.id),
                    self.currentOperation["description"],
                    self.remainingOperationsCount,
                    self.remainingEventsCount
                    )
            )

            # If we receive an update that an operation was complete, dimiss the event and the operation. Otherwise, dimiss the event and keep waiting for the operation to be

            if currentOperationAssertionFunction(self.currentBlenderEvent) == True:
                self.currentBlenderEvent = None
                
                self.operationCompleted()

            else:
                
                self.currentBlenderEvent = None
            
            return self.defaultShortDelay