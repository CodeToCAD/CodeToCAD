import os
from codetocad.cli.config import (
    ConfigProvider,
    read_config,
    write_config,
)


def set_blender_executable_path(blender_path: str):
    """
    Sets the Blender executable path in the configuration file.

    Usage: `set_blender_executable_path("/Applications/Blender.app/Contents/MacOS/Blender")`
    """
    if not os.path.exists(blender_path):
        raise FileNotFoundError(f"Blender executable not found at {blender_path}")

    blender_config = ConfigProvider(name="blender", path=blender_path)

    config = read_config()

    if "blender" in config.providers:
        blender_config = config.providers["blender"]

    blender_config.path = blender_path

    config.providers["blender"] = blender_config

    write_config(config)


def get_blender_executable_path() -> str | None:
    """
    Retrieves the Blender executable path from the configuration file.
    """
    config = read_config()
    blender_config = config.providers.get("blender", None)
    return blender_config.path if blender_config else None
