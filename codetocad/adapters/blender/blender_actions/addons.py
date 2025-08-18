import bpy


def addon_set_enabled(addon_name: str, is_enabled: bool):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if is_enabled else preferences.addon_disable

    command(module=addon_name)


def get_addon(addon_name: str) -> "bpy.types.Addon|None":

    preferences = bpy.context.preferences

    if not preferences:
        raise Exception("Blender preferences are not available.")

    return preferences.addons.get(addon_name)


def enable_addon(addon_name: str):
    # check if the addon is enabled, enable it if it is not.
    addon = get_addon(addon_name)

    if addon is None:
        addon_set_enabled(addon_name, True)

        addon = get_addon(addon_name)

    assert addon is not None, f"Could not enable the {addon_name} addon."
