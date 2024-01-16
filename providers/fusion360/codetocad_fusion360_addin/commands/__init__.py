# Here you define the commands that will be added to your add-in.

from .commandDialog import entry as commandDialog
from .paletteShow import entry as paletteShow
from .paletteSend import entry as paletteSend

# TODO add your imported modules to this list.
# Fusion will automatically call the start() and stop() functions.
commands = [
    commandDialog,
    # paletteShow,
    # paletteSend
]


# Assumes you defined a "start" function in each of your modules.
# The start function will be run when the add-in is started.
def start():
    for command in commands:
        command.start()


# Assumes you defined a "stop" function in each of your modules.
# The stop function will be run when the add-in is stopped.
def stop():
    for command in commands:
        command.stop()
