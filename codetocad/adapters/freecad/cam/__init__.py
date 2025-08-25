"""
FreeCAD CAM adapter implementations.

This module provides FreeCAD-specific implementations of the CAM interfaces
using FreeCAD's Path Workbench functionality.
"""

from codetocad.adapters.freecad.cam.toolpath import Toolpath
from codetocad.adapters.freecad.cam.tool import Tool
from codetocad.adapters.freecad.cam.tool_library import ToolLibrary
from codetocad.adapters.freecad.cam.work_coordinate_system import WorkCoordinateSystem
from codetocad.adapters.freecad.cam.post_processor import PostProcessor
from codetocad.adapters.freecad.cam.simulation import Simulation
from codetocad.adapters.freecad.cam.cam_job import CAMJob

__all__ = [
    "Toolpath",
    "Tool",
    "ToolLibrary",
    "WorkCoordinateSystem",
    "PostProcessor",
    "Simulation",
    "CAMJob",
]
