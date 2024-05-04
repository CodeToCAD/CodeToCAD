# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *


class SubdividableInterface(metaclass=ABCMeta):

    """
    An entity that can be broken down or scaled up into more components.
    """

    @abstractmethod
    def remesh(self, strategy: "str", amount: "float"):
        """
        Remeshing changes the shape of an entity.
        """

        print("remesh is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def subdivide(self, amount: "float"):
        """
        Subdivide an entity into more components.
        """

        print("subdivide is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def decimate(self, amount: "float"):
        """
        Decimate an entity into less components.
        """

        print("decimate is called in an abstract method. Please override this method.")

        raise NotImplementedError()
