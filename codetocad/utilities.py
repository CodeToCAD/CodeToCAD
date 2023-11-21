# utilities.py contains enums and helper functions for CodeToCAD python functionality.

import re
import sys
from uuid import uuid4
from pathlib import Path

from typing import Optional, Union
from codetocad.codetocad_types import FloatOrItsStringValue
from codetocad.core.angle import Angle
from codetocad.core.boundary_axis import BoundaryAxis
from codetocad.core.boundary_box import BoundaryBox
from codetocad.core.dimension import Dimension

from codetocad.enums.angle_unit import AngleUnit
from codetocad.enums.length_unit import LengthUnit


min = "min"
max = "max"
center = "center"

reservedWords = [min, max, center]


def is_reserved_word_in_string(string_to_check: str) -> bool:
    for word in reservedWords:
        if word in string_to_check:
            return True
    return False


def get_filename(relative_file_path: str):
    path = Path(relative_file_path)
    return path.stem


def get_filenameWithExtension(relative_file_path: str):
    path = Path(relative_file_path)
    return path.name


def get_file_extension(file_path: str):
    path = Path(file_path)
    return path.suffix.replace(".", "")


def get_absolute_filepath(relative_file_path: str):
    path = Path(relative_file_path)
    absoluteFilePath = relative_file_path
    if not path.is_absolute():
        absoluteFilePath = str(Path(sys.argv[0]).parent.joinpath(path).resolve())
    return absoluteFilePath


def create_uuid_like_id():
    return str(uuid4()).replace("-", "")[:10]


def format_landmark_entity_name(parent_entity_name: str, landmark_name: str):
    return f"{parent_entity_name}_{landmark_name}"


def get_angles_from_string_list(angles: Union[str, list[str]]) -> list[Angle]:
    anglesList: list[str]
    if isinstance(angles, str):
        anglesList = angles.replace(" ", "").lower().split(",")
    else:
        anglesList = angles

    assert isinstance(anglesList, (list, tuple)), "Only a list of strings is allowed."

    default_unit: AngleUnit = AngleUnit.DEGREES

    angleString = anglesList[-1]

    if isinstance(angleString, str):
        angleString = angleString.replace(" ", "").lower()
        angleString = re.search("[A-Za-z]+$", angleString)

        unitInString = AngleUnit.from_string(angleString[0]) if angleString else None
        if unitInString is not None and angleString is not None:
            default_unit = unitInString
            if len(angleString[0]) == len(anglesList[-1]):
                anglesList.pop()

    parsedAngles = []
    for angle in anglesList:
        parsedAngles.append(Angle.from_string(angle, default_unit))

    return parsedAngles


# Replace "min|max|center" in "min+0.2" to the value in the bounding box's BoundaryAxis
def replace_min_max_center_with_respective_value(
    dimension: str, boundary_axis: BoundaryAxis, default_unit: LengthUnit
):
    dimension = dimension.lower()

    while "min" in dimension:
        dimension = dimension.replace(
            "min",
            "({})".format(
                Dimension(boundary_axis.min, boundary_axis.unit)
                .convert_to_unit(default_unit)
                .value
            ),
        )
    while "max" in dimension:
        dimension = dimension.replace(
            "max",
            "({})".format(
                Dimension(boundary_axis.max, boundary_axis.unit)
                .convert_to_unit(default_unit)
                .value
            ),
        )
    while "center" in dimension:
        dimension = dimension.replace(
            "center",
            "({})".format(
                Dimension(boundary_axis.center, boundary_axis.unit)
                .convert_to_unit(default_unit)
                .value
            ),
        )

    return dimension


def get_unit_in_string(dimension_string):
    if not isinstance(dimension_string, str):
        return None

    dimension_string = dimension_string.replace(" ", "").lower()

    unitSearchResults = re.search("[A-Za-z]+$", dimension_string)

    unitInString = unitSearchResults[0] if unitSearchResults else None

    return (
        unitInString
        if unitInString and not is_reserved_word_in_string(unitInString)
        else None
    )


def get_dimension_list_from_string_list(
    dimensions: Union[str, list[FloatOrItsStringValue]],
    bounding_box: Optional[BoundaryBox] = None,
) -> list[Dimension]:
    if isinstance(dimensions, str):
        dimensions = dimensions.replace(" ", "").lower().split(",")

    assert isinstance(dimensions, (list, tuple)), "Only a list of strings is allowed."

    parsedDimensions = []

    default_unit = None

    unitInString = get_unit_in_string(dimensions[-1])
    if unitInString is not None:
        default_unit = LengthUnit.from_string(unitInString)
        if len(unitInString) == len(dimensions[-1].replace(" ", "").lower()):
            dimensions.pop()

    for index, dimension in enumerate(dimensions):
        if bounding_box is not None and index < 3:
            boundary_axis = getattr(bounding_box, "xyz"[index])
            parsedDimensions.append(
                Dimension.from_string(dimension, default_unit, boundary_axis)
            )
            continue

        parsedDimensions.append(Dimension.from_string(dimension, default_unit, None))

    return parsedDimensions
