import bpy


def create_driver(blender_object: bpy.types.Object, path: str, index=-1):
    return blender_object.driver_add(path, index).driver


def remove_driver(blender_object: bpy.types.Object, path: str, index=-1):
    blender_object.driver_remove(path, index)


def get_driver(
    blender_object: bpy.types.Object,
    path: str,
):
    """this returns an FCurve object
    References https://docs.blender.org/api/current/bpy.types.FCurve.html
    """
    fcurve = blender_object.animation_data.drivers.find(path)

    assert (
        fcurve is not None
    ), f"Could not find driver {path} for object {blender_object.name}."

    return fcurve.driver


def set_driver(
    driver: bpy.types.Driver,
    driver_type,  # : BlenderDriverTypes,
    expression="",
):
    driver.type = driver_type

    driver.expression = expression if expression else ""


def set_driver_variable_single_prop(
    driver: bpy.types.Driver,
    variable_name: str,
    target_blender_object: bpy.types.Object,
    target_data_path: str,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "SINGLE_PROP"

    variable.targets[0].id = target_blender_object

    variable.targets[0].data_path = target_data_path


def set_driver_variable_transforms(
    driver: bpy.types.Driver,
    variable_name: str,
    target_blender_object: bpy.types.Object,
    transform_type,  # : BlenderDriverVariableTransformTypes,
    transform_space,  # : BlenderDriverVariableTransformSpaces
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "TRANSFORMS"

    variable.targets[0].id = target_blender_object

    variable.targets[0].transform_type = transform_type

    variable.targets[0].transform_space = transform_space


def set_driver_variable_location_difference(
    driver: bpy.types.Driver,
    variable_name: str,
    target1_blender_object: bpy.types.Object,
    target2_blender_object: bpy.types.Object,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "LOC_DIFF"

    variable.targets[0].id = target1_blender_object

    variable.targets[1].id = target2_blender_object


def set_driver_variable_rotation_difference(
    driver: bpy.types.Driver,
    variable_name: str,
    target1_blender_object: bpy.types.Object,
    target2_blender_object: bpy.types.Object,
):
    variable = driver.variables.get(variable_name)

    if variable is None:
        variable = driver.variables.new()
        driver.variables[-1].name = variable_name

    variable.type = "ROTATION_DIFF"

    variable.targets[0].id = target1_blender_object

    variable.targets[1].id = target2_blender_object
