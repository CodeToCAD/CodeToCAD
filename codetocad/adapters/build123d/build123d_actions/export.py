"""
Export functions for build123d objects.
"""

from typing import Union, List
import build123d as bd
from pathlib import Path


def export_step(objects: Union[bd.Shape, list[bd.Shape]], file_path: str) -> None:
    """Export build123d objects to STEP format."""
    if isinstance(objects, list):
        # Export multiple objects - create compound or export individually
        if len(objects) == 1:
            bd.export_step(objects[0], file_path)
        else:
            # For multiple objects, create a compound
            compound = bd.Compound(objects)
            bd.export_step(compound, file_path)
    else:
        # Single object
        bd.export_step(objects, file_path)


def export_stl(
    objects: Union[bd.Shape, list[bd.Shape]], file_path: str, tolerance: float = 0.1
) -> None:
    """Export build123d objects to STL format."""
    if isinstance(objects, list):
        # Export multiple objects - create compound or export individually
        if len(objects) == 1:
            bd.export_stl(objects[0], file_path, tolerance=tolerance)
        else:
            # For multiple objects, create a compound
            compound = bd.Compound(objects)
            bd.export_stl(compound, file_path, tolerance=tolerance)
    else:
        # Single object
        bd.export_stl(objects, file_path, tolerance=tolerance)


def export_obj(objects: Union[bd.Shape, list[bd.Shape]], file_path: str) -> None:
    """Export build123d objects to OBJ format."""
    # Note: build123d may not have direct OBJ export,
    # this is a placeholder for future implementation
    raise NotImplementedError("OBJ export not yet implemented for build123d")


def export_brep(objects: Union[bd.Shape, list[bd.Shape]], file_path: str) -> None:
    """Export build123d objects to BREP format."""
    if isinstance(objects, list):
        # Export multiple objects - create compound or export individually
        if len(objects) == 1:
            bd.export_brep(objects[0], file_path)
        else:
            # For multiple objects, create a compound
            compound = bd.Compound(objects)
            bd.export_brep(compound, file_path)
    else:
        # Single object
        bd.export_brep(objects, file_path)


def import_step(file_path: str) -> list[bd.Shape]:
    """Import STEP file and return list of shapes."""
    # Note: Import functions may need to be implemented differently
    # This is a placeholder for the correct import API
    raise NotImplementedError(
        "STEP import needs to be implemented with correct build123d API"
    )


def import_stl(file_path: str) -> bd.Shape:
    """Import STL file and return shape."""
    # Note: Import functions may need to be implemented differently
    # This is a placeholder for the correct import API
    raise NotImplementedError(
        "STL import needs to be implemented with correct build123d API"
    )


def import_brep(file_path: str) -> list[bd.Shape]:
    """Import BREP file and return list of shapes."""
    # Note: Import functions may need to be implemented differently
    # This is a placeholder for the correct import API
    raise NotImplementedError(
        "BREP import needs to be implemented with correct build123d API"
    )
