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
    from . import LandmarkInterface


class EntityInterface(metaclass=ABCMeta):
    """Capabilities shared between Parts and Sketches."""

    name: str
    description: Optional[str] = None
    native_instance = None

    @abstractmethod
    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def is_exists(self) -> bool:
        """
        Check if an entity exists
        """

        print("is_exists is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def rename(self, new_name: str, renamelinked_entities_and_landmarks: bool = True):
        """
        Rename the entity, with an option to rename linked landmarks and underlying data.
        """

        print("rename is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def delete(self, remove_children: bool = True):
        """
        Delete the entity from the scene. You may need to delete an associated joint or other features.
        """

        print("delete is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def is_visible(self) -> bool:
        """
        Returns whether the entity is visible in the scene.
        """

        print(
            "is_visible is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def set_visible(self, is_visible: bool):
        """
        Toggles visibility of an entity in the scene.
        """

        print(
            "set_visible is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def apply(
        self,
        rotation: bool = True,
        scale: bool = True,
        location: bool = False,
        modifiers: bool = True,
    ):
        """
        Apply any modifications. This is application specific, but a general function is that it finalizes any changes made to an entity.
        """

        print("apply is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def get_native_instance(self) -> object:
        """
        Get the native API's object instance. For example, in Blender API, this would return a bpy.object instance.
        """

        print(
            "get_native_instance is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_location_world(self) -> "Point":
        """
        Get the entities XYZ location relative to World Space.
        """

        print(
            "get_location_world is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_location_local(self) -> "Point":
        """
        Get the entities XYZ location relative to Local Space.
        """

        print(
            "get_location_local is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def select(self):
        """
        Select the entity (in UI).
        """

        print("select is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        """
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        """

        print(
            "translate_xyz is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def translate_x(self, amount: DimensionOrItsFloatOrStringValue):
        """
        Translate in the X direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        """

        print(
            "translate_x is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def translate_y(self, amount: DimensionOrItsFloatOrStringValue):
        """
        Translate in the Y direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        """

        print(
            "translate_y is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def translate_z(self, amount: DimensionOrItsFloatOrStringValue):
        """
        Translate in the z direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        """

        print(
            "translate_z is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        """
        Rotate in the XYZ direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        """

        print(
            "rotate_xyz is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def rotate_x(self, rotation: AngleOrItsFloatOrStringValue):
        """
        Rotate in the X direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        """

        print("rotate_x is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        """
        Rotate in the Y direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        """

        print("rotate_y is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        """
        Rotate in the Z direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        """

        print("rotate_z is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def get_bounding_box(self) -> "BoundaryBox":
        """
        Get the Boundary Box around the entity.
        """

        print(
            "get_bounding_box is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_dimensions(self) -> "Dimensions":
        """
        Get the length span in each point axis (X,Y,Z).
        """

        print(
            "get_dimensions is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def create_landmark(
        self,
        landmark_name: str,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "LandmarkInterface":
        """
        Shortcut for creating and assigning a landmark to this entity. Returns a Landmark instance.
        """

        print(
            "create_landmark is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def get_landmark(
        self, landmark_name: PresetLandmarkOrItsName
    ) -> "LandmarkInterface":
        """
        Get the landmark by name
        """

        print(
            "get_landmark is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()
