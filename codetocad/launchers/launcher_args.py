from dataclasses import asdict, dataclass
import argparse
from typing import Optional

from codetocad.utilities import get_absolute_filepath


@dataclass
class LauncherArgs:
    script_file_path: str
    launcher: str
    launcher_location: Optional[str] = None
    background: Optional[bool] = None
    document_name: Optional[str] = None
    config_file_path: Optional[str] = None

    @staticmethod
    def get_sample_launcher_name():
        return "providers_sample"

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

        args_list = [self.launcher_location or self.launcher]

        for key, value in args.items():
            args_list.append(f"--{key}")
            args_list.append(str(value))

        return args_list

    @staticmethod
    def from_cli_args():
        parser = argparse.ArgumentParser(
            description="Welcome to the CodeToCAD cli tool. Visit https://github.com/CodeToCAD/CodeToCAD for help or information."
        )

        parser.add_argument(
            "script_file_path", type=str, help="CodeToCAD script to execute"
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

        args = parser.parse_args()

        return LauncherArgs(
            script_file_path=get_absolute_filepath(args.script_file_path, True),
            launcher=args.launcher,
            launcher_location=args.launcher_location,
            background=args.background,
            document_name=args.document_name,
            config_file_path=args.config_file_path,
        )
