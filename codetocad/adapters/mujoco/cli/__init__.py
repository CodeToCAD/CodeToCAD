"""
MuJoCo CLI utilities.

This module contains command-line utilities for working with MuJoCo simulations.
"""

from .run_mujoco import run_mujoco_simulation
from .config import set_mujoco_config, get_mujoco_config

__all__ = [
    "run_mujoco_simulation",
    "set_mujoco_config",
    "get_mujoco_config",
]
