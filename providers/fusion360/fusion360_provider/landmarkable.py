from codetocad.codetocad_types import (
    DimensionOrItsFloatOrStringValue,
    PresetLandmarkOrItsName,
)
from codetocad.core.dimension import Dimension
from codetocad.interfaces.landmarkable_interface import LandmarkableInterface
from providers.fusion360.fusion360_provider.landmark import Landmark


class Landmarkable(LandmarkableInterface):
    def get_landmark(
        self, landmark_name: "PresetLandmarkOrItsName"
    ) -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    def create_landmark(
        self,
        landmark_name: "str",
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "Landmark":
        boundingBox = self.fusion_body.get_bounding_box()
        localPositions = [
            Dimension.from_dimension_or_its_float_or_string_value(x, boundingBox.x),
            Dimension.from_dimension_or_its_float_or_string_value(y, boundingBox.y),
            Dimension.from_dimension_or_its_float_or_string_value(z, boundingBox.z),
        ]
        landmark = Landmark(landmark_name, self)
        landmark.fusion_landmark.create_landmark(
            localPositions[0].value, localPositions[1].value, localPositions[2].value
        )
        return landmark
