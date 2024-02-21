def terminate():
    """Terminate this script.  If defined, the module's 'stop' function will be called.  If this module is debugging, the debugger is stopped.  The script's module and any modules imported relative to this module are removed from sys.modules and released."""
    pass


def autoTerminate(value):
    """Get or set the autoTerminate flag for this module.  The current value is returned when called with no arguments.  Call with a single Boolean value to set this current value.  When set to True (the default), the script will automatically terminate when code execution returns from the module's main block.  When set to False, the script's module will remain loaded until 'terminate' is called or the script is externally stopped.  Typically, a script that subscribes to events would set this to False after attaching event handlers to events before returning from it's 'run' function."""
    return bool()


def doEvents():
    """Process any pending system events or messages.  This allows the Fusion UI to update and perform any event or message driven operations.  This may be useful to avoid blocking UI updates while performing a long operation, or while waiting for asynchronous operations to be processed."""
    pass
