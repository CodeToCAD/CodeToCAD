"""
CAM (Computer-Aided Manufacturing) interfaces for CodeToCAD.

This module provides abstract interfaces for CNC machining operations including:
- Toolpath generation (2D/3D milling, drilling, contouring, pocketing)
- Tool library management (definition of mills, drills, endmills, cutters, etc.)
- Work coordinate system (WCS) setup and origin management
- Post-processing/export (G-code, CNC machine-specific dialects)
- Simulation and verification (basic collision checks, material removal preview)
"""

from codetocad.interfaces.cam.toolpath_interface import (
    ToolpathInterface,
    ToolpathOperation,
    ToolpathStrategy,
    CuttingParameters,
)
from codetocad.interfaces.cam.tool_interface import (
    ToolInterface,
    ToolType,
    ToolGeometry,
    CuttingData,
)
from codetocad.interfaces.cam.tool_library_interface import (
    ToolLibraryInterface,
)
from codetocad.interfaces.cam.work_coordinate_system_interface import (
    WorkCoordinateSystemInterface,
    WCSOrigin,
    CoordinateSystem,
)
from codetocad.interfaces.cam.post_processor_interface import (
    PostProcessorInterface,
    GCodeDialect,
    MachineConfiguration,
)
from codetocad.interfaces.cam.simulation_interface import (
    SimulationInterface,
    CollisionResult,
    MaterialRemovalPreview,
)
from codetocad.interfaces.cam.cam_job_interface import (
    CAMJobInterface,
    JobSetup,
    MachiningSequence,
)

__all__ = [
    # Core interfaces
    "ToolpathInterface",
    "ToolInterface",
    "ToolLibraryInterface",
    "WorkCoordinateSystemInterface",
    "PostProcessorInterface",
    "SimulationInterface",
    "CAMJobInterface",
    # Data classes and enums
    "ToolpathOperation",
    "ToolpathStrategy",
    "CuttingParameters",
    "ToolType",
    "ToolGeometry",
    "CuttingData",
    "WCSOrigin",
    "CoordinateSystem",
    "GCodeDialect",
    "MachineConfiguration",
    "CollisionResult",
    "MaterialRemovalPreview",
    "JobSetup",
    "MachiningSequence",
]
