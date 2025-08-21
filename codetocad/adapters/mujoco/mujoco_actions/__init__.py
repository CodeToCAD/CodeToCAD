"""
MuJoCo action functions for physics simulation.

This module contains utility functions that wrap MuJoCo's native API
for use in the CodeToCAD simulation system.
"""

from codetocad.adapters.mujoco.mujoco_actions.simulation_setup import *
from .body_management import *
from .joint_management import *
from .sensor_management import *
from .controller_management import *
from .file_loading import *
from codetocad.adapters.mujoco.mujoco_actions.xml_generation import *

__all__ = [
    # Simulation setup
    "initialize_mujoco_model",
    "create_mujoco_data",
    "step_mujoco_simulation",
    "reset_mujoco_simulation",
    "set_mujoco_gravity",
    "set_mujoco_timestep",
    # Body management
    "create_body_from_xml",
    "create_body_from_stl",
    "create_body_from_part",
    "create_ground_plane",
    "set_body_position",
    "get_body_position",
    "set_body_velocity",
    "get_body_velocity",
    "apply_force_to_body",
    "get_body_mass",
    "set_body_mass",
    # Joint management
    "create_joint_xml",
    "set_joint_position",
    "get_joint_position",
    "set_joint_velocity",
    "get_joint_velocity",
    "apply_joint_force",
    "get_joint_limits",
    "set_joint_limits",
    "get_joint_range",
    # Sensor management
    "create_force_sensor_xml",
    "create_position_sensor_xml",
    "create_accelerometer_xml",
    "create_gyro_xml",
    "read_sensor_data",
    "get_contact_forces",
    # Controller management
    "create_position_controller",
    "create_velocity_controller",
    "create_actuator_xml",
    "update_controller",
    "set_actuator_control",
    # File loading and XML generation
    "load_mujoco_xml",
    "save_mujoco_xml",
    "generate_body_xml",
    "generate_joint_xml",
    "generate_sensor_xml",
    "generate_actuator_xml",
    "convert_stl_to_mesh",
    "convert_part_to_xml",
]
