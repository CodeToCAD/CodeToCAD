# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *


from codetocad.interfaces.landmark_interface import LandmarkInterface


class LandmarkableInterface(metaclass=ABCMeta):
    """
    An entity that can be use landmarks.
    """

    @abstractmethod
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        """
        Shortcut for creating and assigning a landmark to this entity. Returns a Landmark instance.
        """

        print(
            "create_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        """
        Get the landmark by name
        """

        print(
            "get_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
