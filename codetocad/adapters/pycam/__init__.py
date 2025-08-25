"""
PyCAM adapter for CodeToCAD.

This adapter provides integration with PyCAM for basic 3-axis CNC toolpath generation.
PyCAM is a pure Python CAM solution that's simpler than FreeCAD but more limited.
"""

# CAM imports
from codetocad.adapters.pycam.cam.toolpath import Toolpath
from codetocad.adapters.pycam.cam.tool import Tool
from codetocad.adapters.pycam.cam.tool_library import ToolLibrary
from codetocad.adapters.pycam.cam.post_processor import PostProcessor
from codetocad.adapters.pycam.cam.cam_job import CAMJob

__all__ = [
    # CAM classes
    "Toolpath",
    "Tool",
    "ToolLibrary",
    "PostProcessor",
    "CAMJob",
]
