## `Fusion360.Entity` Additions and Deletions:


- Deleted:
    ```python
    def get_landmark(self, landmark_name: PresetLandmarkOrItsName) -> 'Landmark':
        if isinstance(landmark_name, LandmarkInterface):
            landmark_name = landmark_name.name
        preset: Optional[PresetLandmark] = None
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
                self.create_landmark(landmark_name, presetXYZ[0], presetXYZ[1], presetXYZ[2])
                return landmark
        return landmark
    ```
## `Fusion360.Part` Additions and Deletions:

## `Fusion360.Sketch` Additions and Deletions:

## `Fusion360.Vertex` Additions and Deletions:

## `Fusion360.Edge` Additions and Deletions:

## `Fusion360.Wire` Additions and Deletions:

## `Fusion360.Landmark` Additions and Deletions:

## `Fusion360.Joint` Additions and Deletions:

## `Fusion360.Material` Additions and Deletions:

## `Fusion360.Animation` Additions and Deletions:

## `Fusion360.Light` Additions and Deletions:

## `Fusion360.Camera` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Fusion360.Render` Additions and Deletions:

## `Fusion360.Scene` Additions and Deletions:

## `Fusion360.Analytics` Additions and Deletions:

