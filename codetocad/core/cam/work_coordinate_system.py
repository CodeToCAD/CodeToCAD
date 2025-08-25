"""
Concrete implementation of Work Coordinate System interface.
"""

import copy
from typing import Tuple

from codetocad.interfaces.cam.work_coordinate_system_interface import (
    WorkCoordinateSystemInterface,
)


class WorkCoordinateSystem(WorkCoordinateSystemInterface):
    """Concrete implementation of WorkCoordinateSystemInterface."""

    def copy(self) -> "WorkCoordinateSystem":
        """Create a copy of the WCS."""
        new_wcs = WorkCoordinateSystem()

        # Copy basic properties
        new_wcs.name = self.name
        new_wcs.active = self.active
        new_wcs.description = self.description

        # Deep copy coordinate system and workpiece setup
        if self.coordinate_system:
            new_wcs.coordinate_system = copy.deepcopy(self.coordinate_system)
        if self.workpiece_setup:
            new_wcs.workpiece_setup = copy.deepcopy(self.workpiece_setup)

        new_wcs.custom_properties = copy.deepcopy(self.custom_properties)

        return new_wcs
