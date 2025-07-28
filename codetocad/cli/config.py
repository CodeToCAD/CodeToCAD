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
class Config:
    providers: dict[str, ConfigProvider]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            providers={
                k: ConfigProvider(name=k, path=v["path"])
                for k, v in data.get("providers", {}).items()
            }
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
    write_config(Config(providers={}))

    return read_config()


def write_config(config: Config):
    click.secho(f"Writing configuration file at {get_config_path()} .", fg="yellow")

    os.makedirs(get_codetocad_home(), exist_ok=True)
    config_path = get_config_path()
    with config_path.open("w") as file:
        json.dump(asdict(config), file, indent=4)
