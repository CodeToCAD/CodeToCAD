"""
PyBullet configuration management utilities.

This module provides functions for managing PyBullet simulation configurations,
including loading, saving, and validating configuration parameters.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class PyBulletConfig:
    """PyBullet simulation configuration data class."""

    # Simulation parameters
    gui: bool = True
    time_step: float = 1.0 / 240.0
    gravity: tuple[float, float, float] = (0.0, 0.0, -9.81)
    real_time: bool = False

    # Physics parameters
    solver_iterations: int = 50
    contact_erp: float = 0.2
    contact_damping: float = -1.0
    friction_erp: float = 0.2

    # Visualization parameters
    camera_distance: float = 3.0
    camera_yaw: float = 45.0
    camera_pitch: float = -30.0
    camera_target: tuple[float, float, float] = (0.0, 0.0, 0.0)
    enable_shadows: bool = True
    enable_wireframe: bool = False

    # Simulation control
    max_simulation_time: float = 60.0
    auto_step: bool = True
    step_count_limit: int = 100000

    # File paths
    urdf_search_paths: list[str] = None
    output_directory: str = "pybullet_output"
    log_file: Optional[str] = None

    # Performance settings
    enable_file_caching: bool = True
    collision_filter_mode: int = 1
    enable_cone_friction: bool = True

    def __post_init__(self):
        """Initialize default values after creation."""
        if self.urdf_search_paths is None:
            self.urdf_search_paths = [".", "./urdf", "./models"]


# Global configuration instance
_global_config: Optional[PyBulletConfig] = None
_config_file_path: Optional[str] = None


def get_default_config_path() -> str:
    """Get the default configuration file path."""
    home_dir = Path.home()
    config_dir = home_dir / ".codetocad" / "pybullet"
    config_dir.mkdir(parents=True, exist_ok=True)
    return str(config_dir / "config.json")


def load_config_from_dict(config_dict: Dict[str, Any]) -> PyBulletConfig:
    """
    Load configuration from dictionary.

    Args:
        config_dict: Configuration dictionary

    Returns:
        PyBulletConfig instance
    """
    # Filter out unknown keys
    valid_keys = set(PyBulletConfig.__annotations__.keys())
    filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}

    return PyBulletConfig(**filtered_dict)


def save_config_to_dict(config: PyBulletConfig) -> Dict[str, Any]:
    """
    Save configuration to dictionary.

    Args:
        config: PyBulletConfig instance

    Returns:
        Configuration dictionary
    """
    return asdict(config)


def load_config_from_file(file_path: str) -> PyBulletConfig:
    """
    Load configuration from JSON file.

    Args:
        file_path: Path to configuration file

    Returns:
        PyBulletConfig instance

    Raises:
        FileNotFoundError: If configuration file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(file_path, "r") as f:
        config_dict = json.load(f)

    return load_config_from_dict(config_dict)


def save_config_to_file(config: PyBulletConfig, file_path: str) -> None:
    """
    Save configuration to JSON file.

    Args:
        config: PyBulletConfig instance
        file_path: Path to save configuration file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    config_dict = save_config_to_dict(config)

    with open(file_path, "w") as f:
        json.dump(config_dict, f, indent=2)


def get_pybullet_config(config_file: Optional[str] = None) -> PyBulletConfig:
    """
    Get PyBullet configuration.

    Args:
        config_file: Optional path to configuration file

    Returns:
        PyBulletConfig instance
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
    config = PyBulletConfig()
    _global_config = config
    return config


def set_pybullet_config(
    config: Optional[PyBulletConfig] = None,
    config_file: Optional[str] = None,
    save_to_file: bool = False,
    **kwargs,
) -> PyBulletConfig:
    """
    Set PyBullet configuration.

    Args:
        config: PyBulletConfig instance to set
        config_file: Path to configuration file to load
        save_to_file: Whether to save configuration to file
        **kwargs: Configuration parameters to update

    Returns:
        Updated PyBulletConfig instance
    """
    global _global_config, _config_file_path

    # Load from file if specified
    if config_file:
        config = load_config_from_file(config_file)
        _config_file_path = config_file

    # Use provided config or get current config
    if config is None:
        config = get_pybullet_config()

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


def reset_pybullet_config() -> PyBulletConfig:
    """
    Reset PyBullet configuration to defaults.

    Returns:
        Default PyBulletConfig instance
    """
    global _global_config, _config_file_path

    _global_config = PyBulletConfig()
    _config_file_path = None

    return _global_config


def validate_config(config: PyBulletConfig) -> list[str]:
    """
    Validate PyBullet configuration.

    Args:
        config: Configuration to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Validate time step
    if config.time_step <= 0:
        errors.append("time_step must be positive")
    if config.time_step > 0.1:
        errors.append("time_step should be <= 0.1 for stability")

    # Validate gravity
    if len(config.gravity) != 3:
        errors.append("gravity must be a 3-element tuple")

    # Validate camera parameters
    if config.camera_distance <= 0:
        errors.append("camera_distance must be positive")

    # Validate simulation limits
    if config.max_simulation_time <= 0:
        errors.append("max_simulation_time must be positive")
    if config.step_count_limit <= 0:
        errors.append("step_count_limit must be positive")

    # Validate solver parameters
    if config.solver_iterations <= 0:
        errors.append("solver_iterations must be positive")

    # Validate file paths
    if config.output_directory and not os.path.isabs(config.output_directory):
        # Check if relative path is valid
        try:
            os.makedirs(config.output_directory, exist_ok=True)
        except OSError:
            errors.append(f"Invalid output_directory: {config.output_directory}")

    return errors


def print_config(config: Optional[PyBulletConfig] = None) -> None:
    """
    Print configuration in a readable format.

    Args:
        config: Configuration to print (uses current config if None)
    """
    if config is None:
        config = get_pybullet_config()

    print("PyBullet Configuration:")
    print("=" * 40)

    print(f"GUI Enabled: {config.gui}")
    print(f"Time Step: {config.time_step}s")
    print(f"Gravity: {config.gravity}")
    print(f"Real Time: {config.real_time}")
    print()

    print("Physics Parameters:")
    print(f"  Solver Iterations: {config.solver_iterations}")
    print(f"  Contact ERP: {config.contact_erp}")
    print(f"  Contact Damping: {config.contact_damping}")
    print(f"  Friction ERP: {config.friction_erp}")
    print()

    print("Visualization:")
    print(f"  Camera Distance: {config.camera_distance}")
    print(f"  Camera Yaw: {config.camera_yaw}°")
    print(f"  Camera Pitch: {config.camera_pitch}°")
    print(f"  Camera Target: {config.camera_target}")
    print(f"  Shadows: {config.enable_shadows}")
    print(f"  Wireframe: {config.enable_wireframe}")
    print()

    print("Simulation Control:")
    print(f"  Max Time: {config.max_simulation_time}s")
    print(f"  Auto Step: {config.auto_step}")
    print(f"  Step Limit: {config.step_count_limit}")
    print()

    print("File Paths:")
    print(f"  URDF Search Paths: {config.urdf_search_paths}")
    print(f"  Output Directory: {config.output_directory}")
    print(f"  Log File: {config.log_file or 'None'}")


def create_example_config(file_path: str) -> None:
    """
    Create an example configuration file.

    Args:
        file_path: Path where to save the example configuration
    """
    config = PyBulletConfig()

    # Add some example customizations
    config.gui = True
    config.time_step = 1.0 / 240.0
    config.gravity = (0.0, 0.0, -9.81)
    config.camera_distance = 5.0
    config.enable_shadows = True
    config.output_directory = "./simulation_results"

    save_config_to_file(config, file_path)
    print(f"Example configuration saved to: {file_path}")


if __name__ == "__main__":
    # CLI for configuration management
    import argparse

    parser = argparse.ArgumentParser(description="PyBullet configuration management")
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
        reset_pybullet_config()
        print("Configuration reset to defaults")
    else:
        parser.print_help()
