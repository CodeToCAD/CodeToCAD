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
    from . import EntityInterface


class PatternableInterface(metaclass=ABCMeta):
    """An entity that can be patterned."""

    @abstractmethod
    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        """
        Pattern in a uniform direction.
        """

        print(
            "linear_pattern is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        """
        Pattern in a circular direction.
        """

        print(
            "circular_pattern is called in an abstract method. Please override this method."
        )
        return self
