"""Open3D integration: visualize any CodeToCAD Part3D.

Usage::

    from codetocad_integrations.build123d import make_cube
    from codetocad_integrations.open3d import show

    cube = make_cube("10cm", "10cm", "5cm")
    show(cube)  # opens an interactive Open3D window

Any Part3D works here - a plain core part or one federated by the
Build123D/Blender integrations - since it's exported (``part.export()``)
to a temporary mesh file and loaded into Open3D rather than replayed
feature-by-feature. Use ``render()`` to save a screenshot instead of
opening a window (docs, CI, headless scripts).
"""

from .viewer import render, show, to_mesh

__all__ = ["to_mesh", "show", "render"]
