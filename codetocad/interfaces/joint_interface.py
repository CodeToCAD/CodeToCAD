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


class JointInterface(metaclass=ABCMeta):
    """Joints define the relationships and constraints between entities."""

    entity1: EntityOrItsName
    entity2: EntityOrItsName

    @abstractmethod
    def __init__(self, entity1: EntityOrItsName, entity2: EntityOrItsName):
        self.entity1 = entity1
        self.entity2 = entity2

    @abstractmethod
    def translate_landmark_onto_another(self):
        """
        Transforms one landmark onto another
        """

        print(
            "translate_landmark_onto_another is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def pivot(self):
        """
        Constraint the rotation origin of entity B to entity A's landmark.
        """

        print("pivot is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def gear_ratio(self, ratio: float):
        """
        Constraint the rotation of entity B to be a percentage of entity A's
        """

        print(
            "gear_ratio is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_location_xyz(
        self,
        x: Optional[DimensionOrItsFloatOrStringValue] = None,
        y: Optional[DimensionOrItsFloatOrStringValue] = None,
        z: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_xyz is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_location_x(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_x is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_location_y(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_y is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_location_z(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_z is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_rotation_xyz(
        self,
        x: Optional[AngleOrItsFloatOrStringValue] = None,
        y: Optional[AngleOrItsFloatOrStringValue] = None,
        z: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_xyz is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_rotation_x(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_x is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_rotation_y(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_y is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def limit_rotation_z(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_z is called in an abstract method. Please override this method."
        )
        return self
