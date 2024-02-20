# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.material_interface import MaterialInterface


class MaterialableInterface(metaclass=ABCMeta):

    """
    An entity that accepts a material or texture.
    """

    @abstractmethod
    def set_material(self, material_name: "MaterialOrItsName"):
        """
        Assign a known material to this part.
        """

        print(
            "set_material is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
