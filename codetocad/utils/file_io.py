import os
from pathlib import Path
import sys


def get_filename(relative_file_path: str):
    path = Path(relative_file_path)
    return path.stem


def get_filenameWithExtension(relative_file_path: str):
    path = Path(relative_file_path)
    return path.name


def get_file_extension(file_path: str):
    path = Path(file_path)
    return path.suffix.replace(".", "")


def get_absolute_filepath(relative_file_path: str, use_pwd=False):
    path = Path(relative_file_path)
    absoluteFilePath = relative_file_path
    if not path.is_absolute():
        base_path = Path(sys.argv[0]).parent

        if use_pwd:
            base_path = Path(os.getcwd())

        absoluteFilePath = str(base_path.joinpath(path).resolve())

    return absoluteFilePath
