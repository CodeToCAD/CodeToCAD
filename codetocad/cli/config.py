from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path

import click


@dataclass
class ConfigProvider:
    name: str
    path: str


@dataclass
class AssetConfig:
    """Configuration for asset management."""

    material_cache_dir: str = ""
    model_cache_dir: str = ""
    thingiverse_api_key: str = ""
    poliigon_api_key: str = ""
    auto_download_materials: bool = True
    auto_download_models: bool = False
    max_cache_size_mb: int = 1000

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            material_cache_dir=data.get(
                "material_cache_dir", f"{get_codetocad_home() / 'material_cache'}"
            ),
            model_cache_dir=data.get(
                "model_cache_dir", f"{get_codetocad_home() / 'model_cache'}"
            ),
            thingiverse_api_key=data.get("thingiverse_api_key", ""),
            poliigon_api_key=data.get("poliigon_api_key", ""),
            auto_download_materials=data.get("auto_download_materials", True),
            auto_download_models=data.get("auto_download_models", False),
            max_cache_size_mb=data.get("max_cache_size_mb", 1000),
        )


@dataclass
class PyBulletConfig:
    """Configuration for PyBullet adapter."""

    default_gui: bool = True
    default_time_step: float = 0.004166667
    default_gravity: tuple[float, float, float] = (0, 0, -9.81)
    enable_debug_visualizer: bool = False

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            default_gui=data.get("default_gui", True),
            default_time_step=data.get("default_time_step", 0.004166667),
            default_gravity=tuple(data.get("default_gravity", [0, 0, -9.81])),
            enable_debug_visualizer=data.get("enable_debug_visualizer", False),
        )


@dataclass
class MuJoCoConfig:
    """Configuration for MuJoCo adapter."""

    default_viewer: bool = True
    default_time_step: float = 0.002
    default_gravity: tuple[float, float, float] = (0, 0, -9.81)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            default_viewer=data.get("default_viewer", True),
            default_time_step=data.get("default_time_step", 0.002),
            default_gravity=tuple(data.get("default_gravity", [0, 0, -9.81])),
        )


@dataclass
class BlenderConfig:
    """Configuration for Blender adapter."""

    executable_path: str = ""
    default_scene_cleanup: bool = True
    enable_gpu_rendering: bool = False

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            executable_path=data.get("executable_path", ""),
            default_scene_cleanup=data.get("default_scene_cleanup", True),
            enable_gpu_rendering=data.get("enable_gpu_rendering", False),
        )


@dataclass
class Build123dConfig:
    """Configuration for Build123d adapter."""

    installation_path: str = ""
    default_units: str = "mm"
    precision: float = 1e-6

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            installation_path=data.get("installation_path", ""),
            default_units=data.get("default_units", "mm"),
            precision=data.get("precision", 1e-6),
        )


@dataclass
class ExportConfig:
    """Configuration for export settings."""

    stl_quality: str = "medium"
    default_units: str = "mm"
    auto_cleanup_temp_files: bool = True

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            stl_quality=data.get("stl_quality", "medium"),
            default_units=data.get("default_units", "mm"),
            auto_cleanup_temp_files=data.get("auto_cleanup_temp_files", True),
        )


@dataclass
class Config:
    providers: dict[str, ConfigProvider]
    assets: AssetConfig
    pybullet: PyBulletConfig
    mujoco: MuJoCoConfig
    blender: BlenderConfig
    build123d: Build123dConfig
    export: ExportConfig

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            providers={
                k: ConfigProvider(name=k, path=v["path"])
                for k, v in data.get("providers", {}).items()
            },
            assets=AssetConfig.from_dict(data.get("assets", {})),
            pybullet=PyBulletConfig.from_dict(data.get("pybullet", {})),
            mujoco=MuJoCoConfig.from_dict(data.get("mujoco", {})),
            blender=BlenderConfig.from_dict(data.get("blender", {})),
            build123d=Build123dConfig.from_dict(data.get("build123d", {})),
            export=ExportConfig.from_dict(data.get("export", {})),
        )


def get_codetocad_home() -> Path:
    """
    Returns the home directory for CodeToCAD.
    """
    return Path.home() / ".codetocad"


def get_config_path():
    return get_codetocad_home() / "config.json"


def get_temp_script_path():
    return get_codetocad_home() / "temp_script.py"


def get_temp_stl_export_path():
    return get_codetocad_home() / "temp_export.stl"


def get_material_cache_dir() -> Path:
    """Get the material cache directory."""
    config = read_config()
    if config.assets.material_cache_dir:
        return Path(config.assets.material_cache_dir)
    return get_codetocad_home() / "material_cache"


def get_model_cache_dir() -> Path:
    """Get the model cache directory."""
    config = read_config()
    if config.assets.model_cache_dir:
        return Path(config.assets.model_cache_dir)
    return get_codetocad_home() / "model_cache"


def get_asset_config() -> AssetConfig:
    """Get the asset configuration."""
    return read_config().assets


def read_config() -> Config:
    config_path = get_config_path()
    if config_path.exists():
        with config_path.open("r") as file:
            click.secho(f"Reading configuration from {config_path} .", fg="green")
            try:
                return Config.from_dict(json.load(file))
            except Exception as e:
                click.secho(
                    f"Configuration file found at  {get_config_path()} but it appears to be corrupted. Please remove this file manually to auto-recreate it.",
                    fg="red",
                )
                raise e

    click.secho(
        f"Configuration file not found. Creating a new one at {get_config_path()} .",
        fg="yellow",
    )
    write_config(
        Config(
            providers={},
            assets=AssetConfig(),
            pybullet=PyBulletConfig(),
            mujoco=MuJoCoConfig(),
            blender=BlenderConfig(),
            build123d=Build123dConfig(),
            export=ExportConfig(),
        )
    )

    return read_config()


def write_config(config: Config):
    click.secho(f"Writing configuration file at {get_config_path()} .", fg="yellow")

    os.makedirs(get_codetocad_home(), exist_ok=True)
    config_path = get_config_path()
    with config_path.open("w") as file:
        json.dump(asdict(config), file, indent=4)


# =============================================================================
# Programmatic Configuration Methods
# =============================================================================


def set_blender_executable_path(path: str) -> None:
    """Set the path to the Blender executable."""
    config = read_config()
    config.blender.executable_path = path
    write_config(config)
    click.secho(f"Blender executable path set to: {path}", fg="green")


def set_blender_gpu_rendering(enabled: bool) -> None:
    """Enable or disable GPU rendering in Blender."""
    config = read_config()
    config.blender.enable_gpu_rendering = enabled
    write_config(config)
    click.secho(
        f"Blender GPU rendering {'enabled' if enabled else 'disabled'}", fg="green"
    )


def set_pybullet_gui_enabled(enabled: bool) -> None:
    """Set default GUI mode for PyBullet simulations."""
    config = read_config()
    config.pybullet.default_gui = enabled
    write_config(config)
    click.secho(
        f"PyBullet GUI {'enabled' if enabled else 'disabled'} by default", fg="green"
    )


def set_pybullet_time_step(time_step: float) -> None:
    """Set default time step for PyBullet simulations."""
    config = read_config()
    config.pybullet.default_time_step = time_step
    write_config(config)
    click.secho(f"PyBullet time step set to: {time_step}s", fg="green")


def set_pybullet_gravity(x: float, y: float, z: float) -> None:
    """Set default gravity for PyBullet simulations."""
    config = read_config()
    config.pybullet.default_gravity = (x, y, z)
    write_config(config)
    click.secho(f"PyBullet gravity set to: ({x}, {y}, {z})", fg="green")


def set_mujoco_viewer_enabled(enabled: bool) -> None:
    """Set default viewer mode for MuJoCo simulations."""
    config = read_config()
    config.mujoco.default_viewer = enabled
    write_config(config)
    click.secho(
        f"MuJoCo viewer {'enabled' if enabled else 'disabled'} by default", fg="green"
    )


def set_mujoco_time_step(time_step: float) -> None:
    """Set default time step for MuJoCo simulations."""
    config = read_config()
    config.mujoco.default_time_step = time_step
    write_config(config)
    click.secho(f"MuJoCo time step set to: {time_step}s", fg="green")


def set_build123d_installation_path(path: str) -> None:
    """Set the path to Build123d installation."""
    config = read_config()
    config.build123d.installation_path = path
    write_config(config)
    click.secho(f"Build123d installation path set to: {path}", fg="green")


def set_build123d_default_units(units: str) -> None:
    """Set default units for Build123d operations."""
    valid_units = ["mm", "cm", "m", "in", "ft"]
    if units not in valid_units:
        click.secho(
            f"Invalid units '{units}'. Valid options: {', '.join(valid_units)}",
            fg="red",
        )
        return

    config = read_config()
    config.build123d.default_units = units
    write_config(config)
    click.secho(f"Build123d default units set to: {units}", fg="green")


def set_material_cache_dir(path: str) -> None:
    """Set the directory for caching downloaded materials."""
    config = read_config()
    config.assets.material_cache_dir = path
    write_config(config)
    click.secho(f"Material cache directory set to: {path}", fg="green")


def set_model_cache_dir(path: str) -> None:
    """Set the directory for caching downloaded 3D models."""
    config = read_config()
    config.assets.model_cache_dir = path
    write_config(config)
    click.secho(f"Model cache directory set to: {path}", fg="green")


def set_thingiverse_api_key(api_key: str) -> None:
    """Set the Thingiverse API key for 3D model downloads."""
    config = read_config()
    config.assets.thingiverse_api_key = api_key
    write_config(config)
    click.secho("Thingiverse API key configured", fg="green")


def set_poliigon_api_key(api_key: str) -> None:
    """Set the Poliigon API key for premium material downloads."""
    config = read_config()
    config.assets.poliigon_api_key = api_key
    write_config(config)
    click.secho("Poliigon API key configured", fg="green")


def set_auto_download_materials(enabled: bool) -> None:
    """Enable or disable automatic material downloads."""
    config = read_config()
    config.assets.auto_download_materials = enabled
    write_config(config)
    click.secho(
        f"Automatic material downloads {'enabled' if enabled else 'disabled'}",
        fg="green",
    )


def set_stl_export_quality(quality: str) -> None:
    """Set the default STL export quality."""
    valid_qualities = ["low", "medium", "high"]
    if quality not in valid_qualities:
        click.secho(
            f"Invalid quality '{quality}'. Valid options: {', '.join(valid_qualities)}",
            fg="red",
        )
        return

    config = read_config()
    config.export.stl_quality = quality
    write_config(config)
    click.secho(f"STL export quality set to: {quality}", fg="green")


def set_default_export_units(units: str) -> None:
    """Set default units for exports."""
    valid_units = ["mm", "cm", "m", "in", "ft"]
    if units not in valid_units:
        click.secho(
            f"Invalid units '{units}'. Valid options: {', '.join(valid_units)}",
            fg="red",
        )
        return

    config = read_config()
    config.export.default_units = units
    write_config(config)
    click.secho(f"Default export units set to: {units}", fg="green")


# =============================================================================
# Configuration Getters
# =============================================================================


def get_pybullet_config() -> PyBulletConfig:
    """Get PyBullet configuration."""
    return read_config().pybullet


def get_mujoco_config() -> MuJoCoConfig:
    """Get MuJoCo configuration."""
    return read_config().mujoco


def get_blender_config() -> BlenderConfig:
    """Get Blender configuration."""
    return read_config().blender


def get_build123d_config() -> Build123dConfig:
    """Get Build123d configuration."""
    return read_config().build123d


def get_export_config() -> ExportConfig:
    """Get export configuration."""
    return read_config().export
