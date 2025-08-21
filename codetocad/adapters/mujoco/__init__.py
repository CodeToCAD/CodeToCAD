"""
MuJoCo adapter for CodeToCAD physics simulation.

This adapter provides MuJoCo-specific implementations of the simulation interfaces,
enabling high-performance physics simulation with MuJoCo's physics engine.
"""

from codetocad.core import *

# Import simulation implementations
from codetocad.adapters.mujoco.simulation.simulation import Simulation
from codetocad.adapters.mujoco.simulation.simulation_body import SimulationBody
from codetocad.adapters.mujoco.simulation.simulation_joint import SimulationJoint
from codetocad.adapters.mujoco.simulation.simulation_sensor import SimulationSensor
from codetocad.adapters.mujoco.simulation.simulation_controller import (
    SimulationController,
)

__all__ = [
    "Simulation",
    "SimulationBody",
    "SimulationJoint",
    "SimulationSensor",
    "SimulationController",
]
