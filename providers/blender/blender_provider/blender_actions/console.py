import bpy
from console_python import replace_help
from functools import wraps
from importlib import reload


def start_debugger(host: str = "localhost", port: int = 5678):
    import debugpy

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
    import codetocad.enums
    import codetocad.core
    import providers.blender.blender_provider
    import inspect

    all_providers_modules = inspect.getmembers(
        codetocad.enums, predicate=inspect.ismodule
    )

    for module_name, module in all_providers_modules:
        print(f"Reloading {module_name}")
        reload(module)

    reload(codetocad.enums)

    all_providers_modules = inspect.getmembers(
        codetocad.core, predicate=inspect.ismodule
    )

    for module_name, module in all_providers_modules:
        print(f"Reloading {module_name}")
        reload(module)

    reload(codetocad)

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
    from codetocad.utilities import center, max, min

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
    namespace["min"] = min
    namespace["max"] = max
    namespace["center"] = center
    namespace["Dimension"] = Dimension
    namespace["Dimensions"] = Dimensions
    namespace["Angle"] = Angle

    replace_help(namespace)
