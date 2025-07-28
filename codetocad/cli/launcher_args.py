from dataclasses import dataclass, asdict
from typing import Optional

from codetocad.cli.config import read_config


@dataclass
class LauncherArgs:
    script_file_path_or_action: str
    launcher: str
    launcher_location: Optional[str] = None
    background: Optional[bool] = False
    document_name: Optional[str] = None
    config_file_path: Optional[str] = None
    debug: Optional[bool] = False

    @staticmethod
    def get_sample_launcher_name():
        return "sample"

    def is_sample_launcher(self):
        return self.launcher == LauncherArgs.get_sample_launcher_name()

    def to_subprocess_args(self):
        args = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )

        args_list = [self.launcher_location or self.launcher]

        del args["launcher"]
        del args["launcher_location"]

        for key, value in args.items():
            args_list.append(f"--{key}")
            args_list.append(str(value))

        return args_list
