import bpy
from console_python import replace_help
from functools import wraps


def install_debugpy(uninstall: bool = False):
    """
    Attempts to pip install debugpy inside Blender
    """
    # references https://github.com/hextantstudios/hextant_python_debugger/blob/main/__init__.py
    import os
    import sys
    import subprocess

    python = os.path.abspath(sys.executable)

    if uninstall:
        subprocess.call([python, "-m", "pip", "uninstall", "debugpy", "--yes"])
        return

    subprocess.call([python, "-m", "pip", "install", "debugpy"])


def start_debugger(host: str = "localhost", port: int = 5678):
    try:
        import debugpy
    except Exception as e:
        print("debugpy is not installed, will try to auto-install.", e)
        install_debugpy()
        __import__("time").sleep(5)
        return start_debugger(host, port)

    try:
        debugpy.listen((host, port))
        write_to_console(
            f"debugpy server has started on {host}:{port}. You may connect to it by attaching your IDE's debugger to a remote debugger at {host}:{port}.",
            "OUTPUT",
        )
    except (Exception, RuntimeError) as e:
        write_to_console(f"Cannot start the debugger server: {e}", "ERROR")


def reload_codetocad_modules():
    print("Reloading CodeToCAD modules")

    import inspect
    from importlib import reload

    import codetocad

    reload(codetocad)

    import providers.blender.blender_provider

    reload(providers.blender.blender_provider)

    all_providers_modules = inspect.getmembers(
        providers.blender.blender_provider, predicate=inspect.ismodule
    )
    for module_name, module in all_providers_modules:
        print(f"Reloading {module_name}")
        reload(module)

    from providers.blender.blender_provider.register import register

    print("Registering BlenderAddon as codetocad.factory provider.")
    register()


def write_to_console(message: str, text_type: str = "INFO"):
    """
    Write to the visible console.

    text_type is one of ('OUTPUT', 'INPUT', 'INFO', 'ERROR')
    """
    # References https://blender.stackexchange.com/a/78332
    area, space, region = console_get()

    context_override = bpy.context.copy()
    context_override.update(
        {
            "space": space,
            "area": area,
            "region": region,
        }
    )
    print(message)
    with bpy.context.temp_override(**context_override):
        for line in message.split("\n"):
            bpy.ops.console.scrollback_append(text=line, type=text_type)


def console_get():
    for area in bpy.context.screen.areas:
        if area.type == "CONSOLE":
            for space in area.spaces:
                if space.type == "CONSOLE":
                    for region in area.regions:
                        if region.type == "WINDOW":
                            return area, space, region
    raise Exception("Can't get the UI's console")


@wraps(replace_help)
def add_codetocad_convenience_words_to_console(namespace):
    # references https://blender.stackexchange.com/a/2751

    print("Adding Blender Console Convenience Words")

    from codetocad import (
        Analytics,
        Animation,
        Joint,
        Landmark,
        Material,
        Part,
        Scene,
        Sketch,
        Dimension,
        Dimensions,
        Angle,
    )

    from codetocad.enums.axis import Axis

    namespace["Part"] = Part
    namespace["Shape"] = Part
    namespace["Sketch"] = Sketch
    namespace["Curve"] = Sketch
    namespace["Landmark"] = Landmark
    namespace["Scene"] = Scene
    namespace["Analytics"] = Analytics
    namespace["Joint"] = Joint
    namespace["Material"] = Material
    namespace["Animation"] = Animation
    namespace["Axis"] = Axis
    namespace["Dimension"] = Dimension
    namespace["Dimensions"] = Dimensions
    namespace["Angle"] = Angle

    replace_help(namespace)
