# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class JointInterface(metaclass=ABCMeta):
    """
    Joints define the relationships and constraints between entities.
    """

    @abstractmethod
    def __init__(self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"):

        self.entity1 = entity1
        self.entity2 = entity2

    @abstractmethod
    def translate_landmark_onto_another(
        self,
    ) -> Self:
        """
        Transforms one landmark onto another
        """

        print(
            "translate_landmark_onto_another is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def pivot(
        self,
    ) -> Self:
        """
        Constraint the rotation origin of entity B to entity A's landmark.
        """

        print("pivot is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def gear_ratio(self, ratio: "float") -> Self:
        """
        Constraint the rotation of entity B to be a percentage of entity A's
        """

        print(
            "gear_ratio is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_location_xyz(
        self,
        x: "str|float|Dimension| None" = None,
        y: "str|float|Dimension| None" = None,
        z: "str|float|Dimension| None" = None,
    ) -> Self:
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_xyz is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_location_x(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_x is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_location_y(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_y is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_location_z(
        self,
        min: "str|float|Dimension| None" = None,
        max: "str|float|Dimension| None" = None,
    ) -> Self:
        """
        Constraint the translation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_location_z is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_rotation_xyz(
        self,
        x: "str|float|Angle| None" = None,
        y: "str|float|Angle| None" = None,
        z: "str|float|Angle| None" = None,
    ) -> Self:
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_xyz is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_rotation_x(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_x is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_rotation_y(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_y is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def limit_rotation_z(
        self, min: "str|float|Angle| None" = None, max: "str|float|Angle| None" = None
    ) -> Self:
        """
        Constraint the rotation of entity B, relative to entity A's landmark.
        """

        print(
            "limit_rotation_z is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
