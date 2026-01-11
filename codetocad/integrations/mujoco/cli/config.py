"""
MuJoCo configuration management utilities.

This module provides functions for managing MuJoCo simulation configurations,
including loading, saving, and validating configuration parameters.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class MuJoCoConfig:
    """MuJoCo simulation configuration data class."""

    # Simulation parameters
    gui: bool = True
    time_step: float = 0.002
    gravity: tuple[float, float, float] = (0.0, 0.0, -9.81)
    integrator: str = "euler"  # euler, rk4, implicit

    # Solver parameters
    solver_iterations: int = 100
    solver_tolerance: float = 1e-6
    solver_noslip_iterations: int = 0
    solver_mpr_iterations: int = 0

    # Contact parameters
    contact_margin: float = 0.0
    contact_solref: tuple[float, float] = (0.02, 1.0)
    contact_solimp: tuple[float, float, float] = (0.9, 0.95, 0.001)

    # Visualization parameters
    camera_fovy: float = 45.0
    camera_distance: float = 3.0
    camera_azimuth: float = 90.0
    camera_elevation: float = -30.0
    camera_lookat: tuple[float, float, float] = (0.0, 0.0, 0.0)

    # Rendering options
    shadow_size: int = 4096
    off_samples: int = 4
    enable_shadows: bool = True
    enable_reflections: bool = False
    enable_fog: bool = False

    # Simulation control
    max_simulation_time: float = 60.0
    auto_step: bool = True
    step_count_limit: int = 1000000
    real_time_factor: float = 1.0

    # File paths
    model_search_paths: list[str] = None
    mesh_search_paths: list[str] = None
    texture_search_paths: list[str] = None
    output_directory: str = "mujoco_output"
    log_file: str | None = None

    # Performance settings
    enable_multithreading: bool = True
    thread_count: int = 0  # 0 = auto-detect
    enable_warmstart: bool = True
    enable_energy_conservation: bool = True

    # Advanced physics
    enable_cone_friction: bool = True
    enable_fluid_dynamics: bool = False
    magnetic_field: tuple[float, float, float] = (0.0, 0.0, 0.0)
    wind_velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def __post_init__(self):
        """Initialize default values after creation."""
        if self.model_search_paths is None:
            self.model_search_paths = [".", "./models", "./xml"]
        if self.mesh_search_paths is None:
            self.mesh_search_paths = [".", "./meshes", "./stl"]
        if self.texture_search_paths is None:
            self.texture_search_paths = [".", "./textures"]


# Global configuration instance
_global_config: MuJoCoConfig | None = None
_config_file_path: str | None = None


def get_default_config_path() -> str:
    """Get the default configuration file path."""
    home_dir = Path.home()
    config_dir = home_dir / ".codetocad" / "mujoco"
    config_dir.mkdir(parents=True, exist_ok=True)
    return str(config_dir / "config.json")


def load_config_from_dict(config_dict: dict[str, Any]) -> MuJoCoConfig:
    """
    Load configuration from dictionary.

    Args:
        config_dict: Configuration dictionary

    Returns:
        MuJoCoConfig instance
    """
    # Filter out unknown keys
    valid_keys = set(MuJoCoConfig.__annotations__.keys())
    filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}

    return MuJoCoConfig(**filtered_dict)


def save_config_to_dict(config: MuJoCoConfig) -> dict[str, Any]:
    """
    Save configuration to dictionary.

    Args:
        config: MuJoCoConfig instance

    Returns:
        Configuration dictionary
    """
    return asdict(config)


def load_config_from_file(file_path: str) -> MuJoCoConfig:
    """
    Load configuration from JSON file.

    Args:
        file_path: Path to configuration file

    Returns:
        MuJoCoConfig instance

    Raises:
        FileNotFoundError: If configuration file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(file_path, "r") as f:
        config_dict = json.load(f)

    return load_config_from_dict(config_dict)


def save_config_to_file(config: MuJoCoConfig, file_path: str) -> None:
    """
    Save configuration to JSON file.

    Args:
        config: MuJoCoConfig instance
        file_path: Path to save configuration file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    config_dict = save_config_to_dict(config)

    with open(file_path, "w") as f:
        json.dump(config_dict, f, indent=2)


def get_mujoco_config(config_file: str | None = None) -> MuJoCoConfig:
    """
    Get MuJoCo configuration.

    Args:
        config_file: Optional path to configuration file

    Returns:
        MuJoCoConfig instance
    """
    global _global_config, _config_file_path

    # If config file specified, load from it
    if config_file:
        try:
            config = load_config_from_file(config_file)
            _global_config = config
            _config_file_path = config_file
            return config
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config from {config_file}: {e}")
            print("Using default configuration")

    # If global config exists, return it
    if _global_config is not None:
        return _global_config

    # Try to load from default location
    default_path = get_default_config_path()
    if os.path.exists(default_path):
        try:
            config = load_config_from_file(default_path)
            _global_config = config
            _config_file_path = default_path
            return config
        except json.JSONDecodeError as e:
            print(f"Warning: Could not load default config: {e}")
            print("Using default configuration")

    # Create default configuration
    config = MuJoCoConfig()
    _global_config = config
    return config


def set_mujoco_config(
    config: MuJoCoConfig | None = None,
    config_file: str | None = None,
    save_to_file: bool = False,
    **kwargs,
) -> MuJoCoConfig:
    """
    Set MuJoCo configuration.

    Args:
        config: MuJoCoConfig instance to set
        config_file: Path to configuration file to load
        save_to_file: Whether to save configuration to file
        **kwargs: Configuration parameters to update

    Returns:
        Updated MuJoCoConfig instance
    """
    global _global_config, _config_file_path

    # Load from file if specified
    if config_file:
        config = load_config_from_file(config_file)
        _config_file_path = config_file

    # Use provided config or get current config
    if config is None:
        config = get_mujoco_config()

    # Update with kwargs
    if kwargs:
        config_dict = save_config_to_dict(config)
        config_dict.update(kwargs)
        config = load_config_from_dict(config_dict)

    # Set as global config
    _global_config = config

    # Save to file if requested
    if save_to_file:
        save_path = _config_file_path or get_default_config_path()
        save_config_to_file(config, save_path)
        _config_file_path = save_path

    return config


def reset_mujoco_config() -> MuJoCoConfig:
    """
    Reset MuJoCo configuration to defaults.

    Returns:
        Default MuJoCoConfig instance
    """
    global _global_config, _config_file_path

    _global_config = MuJoCoConfig()
    _config_file_path = None

    return _global_config


def validate_config(config: MuJoCoConfig) -> list[str]:
    """
    Validate MuJoCo configuration.

    Args:
        config: Configuration to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Validate time step
    if config.time_step <= 0:
        errors.append("time_step must be positive")
    if config.time_step > 0.01:
        errors.append("time_step should be <= 0.01 for stability")

    # Validate integrator
    valid_integrators = ["euler", "rk4", "implicit"]
    if config.integrator not in valid_integrators:
        errors.append(f"integrator must be one of: {valid_integrators}")

    # Validate gravity
    if len(config.gravity) != 3:
        errors.append("gravity must be a 3-element tuple")

    # Validate solver parameters
    if config.solver_iterations <= 0:
        errors.append("solver_iterations must be positive")
    if config.solver_tolerance <= 0:
        errors.append("solver_tolerance must be positive")

    # Validate contact parameters
    if len(config.contact_solref) != 2:
        errors.append("contact_solref must be a 2-element tuple")
    if len(config.contact_solimp) != 3:
        errors.append("contact_solimp must be a 3-element tuple")

    # Validate camera parameters
    if config.camera_fovy <= 0 or config.camera_fovy >= 180:
        errors.append("camera_fovy must be between 0 and 180 degrees")
    if config.camera_distance <= 0:
        errors.append("camera_distance must be positive")

    # Validate simulation limits
    if config.max_simulation_time <= 0:
        errors.append("max_simulation_time must be positive")
    if config.step_count_limit <= 0:
        errors.append("step_count_limit must be positive")
    if config.real_time_factor <= 0:
        errors.append("real_time_factor must be positive")

    # Validate rendering parameters
    if config.shadow_size <= 0 or (config.shadow_size & (config.shadow_size - 1)) != 0:
        errors.append("shadow_size must be a positive power of 2")
    if config.off_samples <= 0:
        errors.append("off_samples must be positive")

    # Validate thread count
    if config.thread_count < 0:
        errors.append("thread_count must be non-negative (0 = auto)")

    return errors


def print_config(config: MuJoCoConfig | None = None) -> None:
    """
    Print configuration in a readable format.

    Args:
        config: Configuration to print (uses current config if None)
    """
    if config is None:
        config = get_mujoco_config()

    print("MuJoCo Configuration:")
    print("=" * 40)

    print(f"Viewer Enabled: {config.gui}")
    print(f"Time Step: {config.time_step}s")
    print(f"Gravity: {config.gravity}")
    print(f"Integrator: {config.integrator}")
    print()

    print("Solver Parameters:")
    print(f"  Iterations: {config.solver_iterations}")
    print(f"  Tolerance: {config.solver_tolerance}")
    print(f"  No-slip Iterations: {config.solver_noslip_iterations}")
    print(f"  MPR Iterations: {config.solver_mpr_iterations}")
    print()

    print("Contact Parameters:")
    print(f"  Margin: {config.contact_margin}")
    print(f"  Solref: {config.contact_solref}")
    print(f"  Solimp: {config.contact_solimp}")
    print()

    print("Visualization:")
    print(f"  Camera FOV: {config.camera_fovy}°")
    print(f"  Camera Distance: {config.camera_distance}")
    print(f"  Camera Azimuth: {config.camera_azimuth}°")
    print(f"  Camera Elevation: {config.camera_elevation}°")
    print(f"  Camera Lookat: {config.camera_lookat}")
    print()

    print("Rendering:")
    print(f"  Shadow Size: {config.shadow_size}")
    print(f"  Off Samples: {config.off_samples}")
    print(f"  Shadows: {config.enable_shadows}")
    print(f"  Reflections: {config.enable_reflections}")
    print(f"  Fog: {config.enable_fog}")
    print()

    print("Performance:")
    print(f"  Multithreading: {config.enable_multithreading}")
    print(f"  Thread Count: {config.thread_count}")
    print(f"  Warmstart: {config.enable_warmstart}")
    print(f"  Energy Conservation: {config.enable_energy_conservation}")
    print()

    print("File Paths:")
    print(f"  Model Search: {config.model_search_paths}")
    print(f"  Mesh Search: {config.mesh_search_paths}")
    print(f"  Texture Search: {config.texture_search_paths}")
    print(f"  Output Directory: {config.output_directory}")


def create_example_config(file_path: str) -> None:
    """
    Create an example configuration file.

    Args:
        file_path: Path where to save the example configuration
    """
    config = MuJoCoConfig()

    # Add some example customizations
    config.gui = True
    config.time_step = 0.002
    config.gravity = (0.0, 0.0, -9.81)
    config.integrator = "rk4"
    config.solver_iterations = 150
    config.camera_distance = 4.0
    config.enable_shadows = True
    config.output_directory = "./mujoco_results"

    save_config_to_file(config, file_path)
    print(f"Example configuration saved to: {file_path}")


if __name__ == "__main__":
    # CLI for configuration management
    import argparse

    parser = argparse.ArgumentParser(description="MuJoCo configuration management")
    parser.add_argument(
        "--print", action="store_true", help="Print current configuration"
    )
    parser.add_argument("--create-example", help="Create example configuration file")
    parser.add_argument("--validate", help="Validate configuration file")
    parser.add_argument(
        "--reset", action="store_true", help="Reset to default configuration"
    )

    args = parser.parse_args()

    if args.print:
        print_config()
    elif args.create_example:
        create_example_config(args.create_example)
    elif args.validate:
        try:
            config = load_config_from_file(args.validate)
            errors = validate_config(config)
            if errors:
                print("Configuration validation errors:")
                for error in errors:
                    print(f"  - {error}")
            else:
                print("Configuration is valid!")
        except Exception as e:
            print(f"Error loading configuration: {e}")
    elif args.reset:
        reset_mujoco_config()
        print("Configuration reset to defaults")
    else:
        parser.print_help()
