"""
PyBullet simulation setup and management functions.

This module contains functions for initializing, configuring, and managing
PyBullet physics simulations.
"""

from typing import Optional, Tuple
import pybullet as p
from codetocad.core.dimensions.point import Point


def initialize_physics_client(gui: bool = False, **kwargs) -> int:
    """
    Initialize PyBullet physics client.

    Args:
        gui: Whether to enable GUI mode
        **kwargs: Additional PyBullet connection parameters

    Returns:
        Physics client ID
    """
    if gui:
        client_id = p.connect(p.GUI, **kwargs)
        # Configure GUI settings
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
    else:
        client_id = p.connect(p.DIRECT, **kwargs)

    return client_id


def disconnect_physics_client(client_id: Optional[int] = None) -> None:
    """
    Disconnect from PyBullet physics client.

    Args:
        client_id: Physics client ID (None for current client)
    """
    if client_id is not None:
        p.disconnect(physicsClientId=client_id)
    else:
        p.disconnect()


def set_gravity(gravity: Point | Tuple[float, float, float]) -> None:
    """
    Set gravity vector for the simulation.

    Args:
        gravity: Gravity vector as Point or (x, y, z) tuple
    """
    if isinstance(gravity, Point):
        gravity_vec = (gravity.x, gravity.y, gravity.z)
    else:
        gravity_vec = gravity

    p.setGravity(*gravity_vec)


def set_time_step(time_step: float) -> None:
    """
    Set simulation time step.

    Args:
        time_step: Time step in seconds
    """
    p.setTimeStep(time_step)


def step_simulation(num_steps: int = 1) -> None:
    """
    Step the simulation forward.

    Args:
        num_steps: Number of simulation steps to execute
    """
    for _ in range(num_steps):
        p.stepSimulation()


def reset_simulation() -> None:
    """Reset the simulation to initial state."""
    p.resetSimulation()


def set_real_time_simulation(enable: bool) -> None:
    """
    Enable or disable real-time simulation.

    Args:
        enable: True to enable real-time simulation
    """
    p.setRealTimeSimulation(enable)


def get_simulation_time() -> float:
    """
    Get current simulation time.

    Returns:
        Current simulation time in seconds
    """
    # PyBullet doesn't have a direct time getter, so we calculate it
    # This would need to be tracked externally in a real implementation
    return 0.0


def configure_debug_visualizer(
    enable_gui: bool = True,
    enable_shadows: bool = True,
    enable_wireframe: bool = False,
    camera_distance: float = 3.0,
    camera_yaw: float = 45.0,
    camera_pitch: float = -30.0,
    camera_target: Tuple[float, float, float] = (0, 0, 0),
) -> None:
    """
    Configure debug visualizer settings.

    Args:
        enable_gui: Enable GUI elements
        enable_shadows: Enable shadow rendering
        enable_wireframe: Enable wireframe rendering
        camera_distance: Camera distance from target
        camera_yaw: Camera yaw angle in degrees
        camera_pitch: Camera pitch angle in degrees
        camera_target: Camera target position
    """
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, enable_gui)
    p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, enable_shadows)
    p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, enable_wireframe)

    p.resetDebugVisualizerCamera(
        cameraDistance=camera_distance,
        cameraYaw=camera_yaw,
        cameraPitch=camera_pitch,
        cameraTargetPosition=camera_target,
    )


def add_debug_text(
    text: str,
    position: Point | Tuple[float, float, float],
    color: Tuple[float, float, float] = (1, 1, 1),
    size: float = 1.0,
    life_time: float = 0.0,
) -> int:
    """
    Add debug text to the simulation.

    Args:
        text: Text to display
        position: Position to display text
        color: Text color as RGB tuple
        size: Text size
        life_time: How long to display text (0 = permanent)

    Returns:
        Debug text ID
    """
    if isinstance(position, Point):
        pos = (position.x, position.y, position.z)
    else:
        pos = position

    return p.addUserDebugText(
        text=text,
        textPosition=pos,
        textColorRGB=color,
        textSize=size,
        lifeTime=life_time,
    )


def remove_debug_text(text_id: int) -> None:
    """
    Remove debug text from the simulation.

    Args:
        text_id: Debug text ID to remove
    """
    p.removeUserDebugItem(text_id)


def add_debug_line(
    start_pos: Point | Tuple[float, float, float],
    end_pos: Point | Tuple[float, float, float],
    color: Tuple[float, float, float] = (1, 0, 0),
    width: float = 1.0,
    life_time: float = 0.0,
) -> int:
    """
    Add debug line to the simulation.

    Args:
        start_pos: Line start position
        end_pos: Line end position
        color: Line color as RGB tuple
        width: Line width
        life_time: How long to display line (0 = permanent)

    Returns:
        Debug line ID
    """
    if isinstance(start_pos, Point):
        start = (start_pos.x, start_pos.y, start_pos.z)
    else:
        start = start_pos

    if isinstance(end_pos, Point):
        end = (end_pos.x, end_pos.y, end_pos.z)
    else:
        end = end_pos

    return p.addUserDebugLine(
        lineFromXYZ=start,
        lineToXYZ=end,
        lineColorRGB=color,
        lineWidth=width,
        lifeTime=life_time,
    )


def save_world_state(filename: str) -> None:
    """
    Save the current world state to a file.

    Args:
        filename: Path to save the world state
    """
    p.saveWorld(filename)


def restore_world_state(filename: str) -> None:
    """
    Restore world state from a file.

    Args:
        filename: Path to the world state file
    """
    p.restoreState(fileName=filename)
