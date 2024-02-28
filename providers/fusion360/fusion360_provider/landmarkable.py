from codetocad.codetocad_types import (
    DimensionOrItsFloatOrStringValue,
    PresetLandmarkOrItsName,
)
from codetocad.core.dimension import Dimension
from codetocad.enums.preset_landmark import PresetLandmark
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.landmarkable_interface import LandmarkableInterface
from providers.fusion360.fusion360_provider.fusion_actions.base import get_component
from providers.fusion360.fusion360_provider.landmark import Landmark


class Landmarkable(LandmarkableInterface):
    def get_landmark(self, landmark_name: PresetLandmarkOrItsName) -> "Landmark":
        if isinstance(landmark_name, LandmarkInterface):
            landmark_name = landmark_name.name
        preset: PresetLandmark | None = None
        if isinstance(landmark_name, str):
            preset = PresetLandmark.from_string(landmark_name)
        if isinstance(landmark_name, PresetLandmark):
            preset = landmark_name
            landmark_name = preset.name
        landmark = Landmark(landmark_name, self.name)
        if preset is not None:
            component = get_component(landmark.get_landmark_entity_name())
            if component is None:
                presetXYZ = preset.get_xyz()
                self.create_landmark(
                    landmark_name, presetXYZ[0], presetXYZ[1], presetXYZ[2]
                )
                return landmark
        return landmark

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
