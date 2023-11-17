import bpy


def addon_set_enabled(addon_name: str, is_enabled: bool):
    preferences = bpy.ops.preferences

    command = preferences.addon_enable if is_enabled else preferences.addon_disable

    command(module=addon_name)


def enable_curve_extra_objects_addon():
    addon_name = "add_curve_extra_objects"

    # check if the addon is enabled, enable it if it is not.
    addon = bpy.context.preferences.addons.get(addon_name)
    if addon is None:
        addon_set_enabled(addon_name, True)
        addon = bpy.context.preferences.addons.get(addon_name)

    assert (
        addon is not None
    ), f"Could not enable the {addon_name} addon to create simple curves"
