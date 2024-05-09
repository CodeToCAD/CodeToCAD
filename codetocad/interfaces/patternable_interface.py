# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class PatternableInterface(metaclass=ABCMeta):
    """
    An entity that can be patterned.
    """

    @abstractmethod
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ) -> Self:
        """
        Pattern in a uniform direction.
        """

        print(
            "linear_pattern is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ) -> Self:
        """
        Pattern in a circular direction.
        """

        print(
            "circular_pattern is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
