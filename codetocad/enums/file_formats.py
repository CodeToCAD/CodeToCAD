from enum import Enum


class FileFormats(Enum):
    PNG = 0
    JPEG = 1
    OPEN_EXR = 2
    MP4 = 3

    @staticmethod
    def from_string(name: str):
        name = name.lower()
        if name == "png":
            return FileFormats.PNG
        if name == "jpg" or name == "jpeg":
            return FileFormats.JPEG
        if name == "exr" or name == "openexr":
            return FileFormats.OPEN_EXR
        if name == "mp4" or "ffmpeg":
            return FileFormats.MP4

        raise TypeError(f"{name} is not a supported file type.")
