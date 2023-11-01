# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class SubdividableInterface(metaclass=ABCMeta):
    """An entity that can be broken down or scaled up into more components."""

    @abstractmethod
    def remesh(self, strategy: str, amount: float):
        """
        Remeshing changes the shape of an entity.
        """

        print("remesh is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def subdivide(self, amount: float):
        """
        Subdivide an entity into more components.
        """

        print("subdivide is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def decimate(self, amount: float):
        """
        Decimate an entity into less components.
        """

        print("decimate is called in an abstract method. Please override this method.")
        return self
