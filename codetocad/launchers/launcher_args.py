from dataclasses import asdict, dataclass
import argparse
from enum import Enum
from typing import Optional
import json
from pathlib import Path

from codetocad.utilities import get_absolute_filepath


class CliActions(Enum):
    VERSION = 0
    UPDATE = 1
    UNINSTALL = 2

    @staticmethod
    def get_action_from_string(action: str) -> "CliActions|None":
        try:
            action = action.upper()
            return CliActions[action]
        except KeyError as e:
            return None

    @staticmethod
    def isAction(action: str):
        return CliActions.get_action_from_string(action) != None


@dataclass
class LauncherArgs:
    script_file_path_or_action: str
    launcher: str
    launcher_location: Optional[str] = None
    background: Optional[bool] = None
    document_name: Optional[str] = None
    config_file_path: Optional[str] = None
    debug: Optional[bool] = False  # Add debug field

    @staticmethod
    def get_sample_launcher_name():
        return "sample"

    def is_sample_launcher(self):
        return self.launcher == LauncherArgs.get_sample_launcher_name()

    def to_subprocess_args(self):
        """
        Produces an array that could be passed as an argument to `subprocess.run` (https://docs.python.org/3/library/subprocess.html#subprocess.run)

        NOTE: LauncherArgs with None values will be excluded from the output.

        Sample output:
        ['/path/to/launcher', '--background', 'true', '--document_name', 'myDocument', '--config_file_path', '/path/to/config']
        """
        args = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        del args["launcher"]
        del args["launcher_location"]

        # Read config to get launcher path if not explicitly provided
        if not self.launcher_location:
            config = self.read_config()
            launcher_config = config.get(self.launcher.lower(), {})
            launcher_path = launcher_config.get("path")
            args_list = [launcher_path or self.launcher]
        else:
            args_list = [self.launcher_location]

        for key, value in args.items():
            args_list.append(f"--{key}")
            args_list.append(str(value))

        return args_list

    @staticmethod
    def from_cli_args():
        parser = argparse.ArgumentParser(
            description="Welcome to the CodeToCAD cli tool. Visit https://github.com/CodeToCAD/CodeToCAD for help or information",
            usage="""
codetocad --help => displays help
codetocad version => displays pip package version
codetocad update => updates pip package
codetocad uninstall => uninstalls pip package
codetocad /path/to/script ...args => runs a codetocad script
""",
        )

        parser.add_argument(
            "script_file_path_or_action",
            type=str,
            help="CodeToCAD script to execute, or action like version, update, uninstall.",
        )

        parser.add_argument(
            "launcher",
            type=str,
            nargs="?",
            const=LauncherArgs.get_sample_launcher_name(),
            default=LauncherArgs.get_sample_launcher_name(),
            help="name of the launcher to execute. You can specify a location using the --launcher_location argument.",
        )

        parser.add_argument(
            "--launcher_location", type=str, help="Path or URL of the launcher"
        )

        parser.add_argument(
            "--background",
            action="store_true",
            help="specify if the process should run in the background",
        )

        parser.add_argument(
            "--document_name",
            type=str,
            help="specify the document name or path to save the output file to",
        )

        parser.add_argument(
            "--config_file_path",
            type=str,
            help="specify the path to a config file to be read by the launcher",
        )

        parser.add_argument(
            "--debug",
            action="store_true",
            help="enable debug mode for additional logging and information",
        )

        args = parser.parse_args()

        return LauncherArgs(
            script_file_path_or_action=(
                get_absolute_filepath(args.script_file_path_or_action, True)
                if not CliActions.isAction(args.script_file_path_or_action)
                else args.script_file_path_or_action
            ),
            launcher=args.launcher,
            launcher_location=args.launcher_location,
            background=args.background,
            document_name=args.document_name,
            config_file_path=args.config_file_path,
            debug=args.debug,
        )

    def get_config_path(self):
        return Path.home() / ".codetocad/config.json"

    def read_config(self):
        config_path = self.get_config_path()
        if config_path.exists():
            with config_path.open("r") as file:
                config = json.load(file)
        else:
            config = {}

        return config

    def write_config(self, config):
        config_path = self.get_config_path()
        with config_path.open("w") as file:
            json.dump(config, file, indent=4)
