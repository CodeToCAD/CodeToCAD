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
            material_cache_dir=data.get("material_cache_dir", ""),
            model_cache_dir=data.get("model_cache_dir", ""),
            thingiverse_api_key=data.get("thingiverse_api_key", ""),
            poliigon_api_key=data.get("poliigon_api_key", ""),
            auto_download_materials=data.get("auto_download_materials", True),
            auto_download_models=data.get("auto_download_models", False),
            max_cache_size_mb=data.get("max_cache_size_mb", 1000),
        )


@dataclass
class Config:
    providers: dict[str, ConfigProvider]
    assets: AssetConfig

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            providers={
                k: ConfigProvider(name=k, path=v["path"])
                for k, v in data.get("providers", {}).items()
            },
            assets=AssetConfig.from_dict(data.get("assets", {})),
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
    write_config(Config(providers={}, assets=AssetConfig()))

    return read_config()


def write_config(config: Config):
    click.secho(f"Writing configuration file at {get_config_path()} .", fg="yellow")

    os.makedirs(get_codetocad_home(), exist_ok=True)
    config_path = get_config_path()
    with config_path.open("w") as file:
        json.dump(asdict(config), file, indent=4)
