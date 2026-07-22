"""Preset primitive functions to quickly generate Part2D or Part3D objects."""

from __future__ import annotations

from codetocad.location import Location, _angle_to_radians
from codetocad.parts import Part2D, Part3D
from codetocad.units import AngleWithUnit, LengthMeters, LengthWithUnit
from codetocad.vectors import Vec3


def _draft(draft_angle: AngleWithUnit) -> dict:
    """A ``{"draft_angle": radians}`` fragment for a primitive dict, or an
    empty dict when there is no draft. Bare numbers are degrees."""
    radians = _angle_to_radians(draft_angle, floats_are_degrees=True)
    return {"draft_angle": radians} if radians else {}


def _apply_start_location(part, start_location: Location | None) -> None:
    if start_location is not None:
        part._origin = Vec3(*start_location.to_tuple())
        # Where the primitive was created, before any transform() calls;
        # federated backends place the base solid here and replay transforms.
        part._start_origin = Vec3(*start_location.to_tuple())


def _make_part3d(
    kind: str,
    start_location: Location | None = None,
    part_class: type[Part3D] = Part3D,
    **dimensions: float,
) -> Part3D:
    part = part_class()
    part._primitive = {"kind": kind, **dimensions}
    _apply_start_location(part, start_location)
    return part


def _make_part2d(
    kind: str, start_location: Location | None = None, **dimensions
) -> Part2D:
    part = Part2D()
    part._primitive = {"kind": kind, **dimensions}
    _apply_start_location(part, start_location)
    return part


# 2D presets


def rectangle(
    width: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part2D:
    return _make_part2d(
        "rectangle",
        start_location,
        width=LengthMeters(width).value,
        height=LengthMeters(height).value,
    )


def circle(
    radius: LengthWithUnit, start_location: Location | None = None
) -> Part2D:
    return _make_part2d("circle", start_location, radius=LengthMeters(radius).value)


def text(
    text: str,
    font: str,
    size: LengthWithUnit,
    start_location: Location | None = None,
) -> Part2D:
    part = Part2D()
    part._primitive = {
        "kind": "text",
        "text": text,
        "font": font,
        "size": LengthMeters(size).value,
    }
    _apply_start_location(part, start_location)
    return part


# 3D presets


def cube(
    length: LengthWithUnit,
    width: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
    draft_angle: AngleWithUnit = 0,
) -> Part3D:
    """``draft_angle`` tapers the four side walls away from vertical (bare
    numbers are degrees): a positive draft shrinks the top face, the base
    keeps its full ``length`` x ``width`` — as needed to release a moulded
    part from a die."""
    return _make_part3d(
        "cube",
        start_location,
        length=LengthMeters(length).value,
        width=LengthMeters(width).value,
        height=LengthMeters(height).value,
        **_draft(draft_angle),
    )


def cylinder(
    radius: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
    draft_angle: AngleWithUnit = 0,
) -> Part3D:
    """``draft_angle`` tapers the wall into a cone frustum (bare numbers are
    degrees): a positive draft shrinks the top radius, the base keeps
    ``radius``."""
    return _make_part3d(
        "cylinder",
        start_location,
        radius=LengthMeters(radius).value,
        height=LengthMeters(height).value,
        **_draft(draft_angle),
    )


def sphere(
    radius: LengthWithUnit, start_location: Location | None = None
) -> Part3D:
    return _make_part3d("sphere", start_location, radius=LengthMeters(radius).value)


def import_file(file_path: str, start_location: Location | None = None) -> Part3D:
    """Import an STL or other file as a Part3D."""
    part = Part3D()
    part._primitive = {"kind": "imported", "file_path": file_path}
    _apply_start_location(part, start_location)
    return part
