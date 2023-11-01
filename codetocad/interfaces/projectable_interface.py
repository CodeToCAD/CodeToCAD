# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SketchInterface


class ProjectableInterface(metaclass=ABCMeta):
    """This entity can be projected onto a surface"""

    @abstractmethod
    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        """
        Project this entity onto another
        """

        print("project is called in an abstract method. Please override this method.")
        raise NotImplementedError()
