# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class ExportableInterface(metaclass=ABCMeta):
    """An enttiy that can be exported."""

    @abstractmethod
    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        """
        Export Entity. Use the filePath to control the export type, e.g. '/path/to/cube.obj' or '/path/to/curve.svg'
        """

        print("export is called in an abstract method. Please override this method.")
        return self
