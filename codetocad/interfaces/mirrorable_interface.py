# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class MirrorableInterface(metaclass=ABCMeta):
    """
    An entity that can be mirrored.
    """

    @abstractmethod
    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ) -> Self:
        """
        Mirror an existing entity with respect to a landmark. If a name is provided, the mirror becomes a separate entity.
        """

        print("mirror is called in an abstract method. Please override this method.")

        raise NotImplementedError()
