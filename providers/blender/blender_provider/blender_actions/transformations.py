from typing import Any, Optional, Sequence
import bpy
import mathutils
from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from providers.blender.blender_provider.blender_actions.objects import get_object
from providers.blender.blender_provider.blender_definitions import (
    BlenderRotationTypes,
    BlenderTranslationTypes,
)


def apply_object_transformations(
    object_name: str,
    apply_rotation: bool,
    apply_scale: bool,
    apply_location: bool,
):
    # Apply the object's transformations (under Object Properties tab)
    # references https://blender.stackexchange.com/a/159540/138679
    blenderObject = get_object(object_name)

    assert (
        blenderObject.data is not None
    ), f"Object {object_name} does not have data to transform."

    decomposedMatrix: list[Any] = blenderObject.matrix_basis.decompose()
    translationVector: mathutils.Vector = decomposedMatrix[0]
    rotationQuat: mathutils.Quaternion = decomposedMatrix[1]
    scaleVector: mathutils.Vector = decomposedMatrix[2]

    translation: mathutils.Matrix = mathutils.Matrix.Translation(translationVector)
    rotation: mathutils.Matrix = rotationQuat.to_matrix().to_4x4()
    scale: mathutils.Matrix = mathutils.Matrix.Diagonal(scaleVector).to_4x4()

    transformation: mathutils.Matrix = mathutils.Matrix()
    basis: mathutils.Matrix = mathutils.Matrix()

    if apply_rotation:
        transformation @= rotation
    else:
        basis @= rotation
    if apply_scale:
        transformation @= scale
    else:
        basis @= scale
    if apply_location:
        transformation @= translation
    else:
        basis @= translation

    mesh: bpy.types.Mesh = blenderObject.data
    mesh.transform(transformation)

    # Set the object to its world translation
    blenderObject.matrix_basis = basis

    for child in blenderObject.children:
        child.matrix_basis = transformation @ child.matrix_basis


def rotate_object(
    object_name: str,
    rotation_angles: list[Optional[Angle]],
    rotation_type: BlenderRotationTypes,
):
    blenderObject = get_object(object_name)

    currentRotation = getattr(blenderObject, rotation_type.value)

    outputRotation = []

    for index in range(len(currentRotation)):
        angle = currentRotation[index]
        newAngle = rotation_angles[index]
        if newAngle is not None:
            angle = newAngle.to_radians().value
        outputRotation.append(angle)

    setattr(blenderObject, rotation_type.value, outputRotation)


def translate_object(
    object_name: str,
    translation_dimensions: Sequence[Dimension | None],
    translation_type: BlenderTranslationTypes,
):
    blenderObject = get_object(object_name)

    assert len(translation_dimensions) == 3, "translation_dimensions must be length 3"

    currentLocation = blenderObject.location

    outputLocation = []

    for index in range(3):
        location = currentLocation[index]
        newLocation = translation_dimensions[index]
        if newLocation is not None:
            location = newLocation.value
        outputLocation.append(location)

    setattr(blenderObject, translation_type.value, outputLocation)


def set_object_location(
    object_name: str, location_dimensions: list[Optional[Dimension]]
):
    blenderObject = get_object(object_name)

    assert len(location_dimensions) == 3, "location_dimensions must be length 3"

    currentLocation = blenderObject.location

    outputLocation = []

    for index in range(3):
        location = currentLocation[index]
        newLocation = location_dimensions[index]
        if newLocation is not None:
            location = newLocation.value
        outputLocation.append(location)

    blenderObject.location = outputLocation


def scale_object(
    object_name: str,
    x_scale_factor: Optional[float],
    y_scale_factor: Optional[float],
    z_scale_factor: Optional[float],
):
    blenderObject = get_object(object_name)

    currentScale: mathutils.Vector = blenderObject.scale

    blenderObject.scale = (
        x_scale_factor or currentScale.x,
        y_scale_factor or currentScale.y,
        z_scale_factor or currentScale.z,
    )
