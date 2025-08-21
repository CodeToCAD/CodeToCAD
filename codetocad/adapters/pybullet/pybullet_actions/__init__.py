"""
PyBullet action functions for physics simulation.

This module contains utility functions that wrap PyBullet's native API
for use in the CodeToCAD simulation system.
"""

from codetocad.adapters.pybullet.pybullet_actions.simulation_setup import *
from codetocad.adapters.pybullet.pybullet_actions.body_management import *
from codetocad.adapters.pybullet.pybullet_actions.joint_management import *
from codetocad.adapters.pybullet.pybullet_actions.sensor_management import *
from codetocad.adapters.pybullet.pybullet_actions.controller_management import *
from codetocad.adapters.pybullet.pybullet_actions.file_loading import *

__all__ = [
    # Simulation setup
    "initialize_physics_client",
    "disconnect_physics_client",
    "set_gravity",
    "set_time_step",
    "step_simulation",
    "reset_simulation",
    # Body management
    "create_body_from_urdf",
    "create_body_from_stl",
    "create_body_from_part",
    "create_ground_plane",
    "remove_body",
    "set_body_position",
    "get_body_position",
    "set_body_velocity",
    "get_body_velocity",
    "apply_force_to_body",
    "apply_torque_to_body",
    # Joint management
    "create_joint",
    "set_joint_position",
    "get_joint_position",
    "set_joint_velocity",
    "get_joint_velocity",
    "apply_joint_force",
    "get_joint_limits",
    "set_joint_limits",
    # Sensor management
    "create_force_sensor",
    "create_contact_sensor",
    "read_sensor_data",
    "get_contact_points",
    # Controller management
    "create_position_controller",
    "create_velocity_controller",
    "update_controller",
    # File loading
    "load_urdf_file",
    "load_stl_file",
    "export_simulation_state",
]
