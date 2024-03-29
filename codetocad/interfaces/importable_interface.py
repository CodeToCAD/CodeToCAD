# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class ImportableInterface(metaclass=ABCMeta):
    """An entity that can be imported from a file."""

    @abstractmethod
    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        """
        Imports geometry from a file.
        """

        print(
            "create_from_file is called in an abstract method. Please override this method."
        )
        return self
