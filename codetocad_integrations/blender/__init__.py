"""Blender integration: federate CodeToCAD parts to Blender (bpy).

Blender's Python API only exists inside Blender, so scripts using this
integration start with ``ensure_blender()``: when run with a normal Python
interpreter it relaunches the same script under ``blender --background`` and
exits; inside Blender it resets the scene and returns.

Usage::

    from codetocad_integrations.blender import ensure_blender, make_cube

    if __name__ == "__main__":
        ensure_blender()
        cube = make_cube("10cm", "10cm", "5cm")
        cube.hole(cube.top_center, radius="4cm", amount="5cm")
        cube.export("my_cube.stl")

Set the ``CODETOCAD_BLENDER`` environment variable to point at a specific
Blender executable (defaults to ``blender`` on the PATH).
"""

from .launcher import INSIDE_BLENDER, blender_command, ensure_blender, run_in_blender

_ADAPTER_NAMES = {
    "Part2D",
    "Part3D",
    "ElectricalComponent",
    "adapt",
    "make_cube",
    "make_box",
    "make_cylinder",
    "make_sphere",
    "make_import",
    "make_rectangle",
    "make_circle",
    "make_text",
    "make_led",
    "make_resistor",
    "make_capacitor",
    "make_fastener",
}

__all__ = sorted(
    _ADAPTER_NAMES
    | {"ensure_blender", "run_in_blender", "blender_command", "INSIDE_BLENDER"}
)


def _make_stub(name: str):
    """A placeholder returned outside Blender so scripts can import (and even
    subclass) adapter names at module top-level; using them raises."""

    def _raise(self, *args, **kwargs):
        raise RuntimeError(
            f"{name} requires Blender's Python (bpy). Call ensure_blender() "
            "at the start of your script so it relaunches under "
            "`blender --background`."
        )

    return type(name, (), {"__init__": _raise, "__call__": _raise})


def __getattr__(name: str):
    if name in _ADAPTER_NAMES:
        if INSIDE_BLENDER:
            from . import parts

            return getattr(parts, name)
        return _make_stub(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
