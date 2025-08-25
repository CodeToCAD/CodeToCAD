"""
FreeCAD adapter for CodeToCAD.

This adapter provides integration with FreeCAD's CAD and CAM capabilities,
including the Path Workbench for CNC toolpath generation.
"""

# CAM imports
from codetocad.adapters.freecad.cam.toolpath import Toolpath
from codetocad.adapters.freecad.cam.tool import Tool
from codetocad.adapters.freecad.cam.tool_library import ToolLibrary
from codetocad.adapters.freecad.cam.work_coordinate_system import WorkCoordinateSystem
from codetocad.adapters.freecad.cam.post_processor import PostProcessor
from codetocad.adapters.freecad.cam.simulation import Simulation
from codetocad.adapters.freecad.cam.cam_job import CAMJob

__all__ = [
    # CAM classes
    "Toolpath",
    "Tool",
    "ToolLibrary",
    "WorkCoordinateSystem",
    "PostProcessor",
    "Simulation",
    "CAMJob",
]
