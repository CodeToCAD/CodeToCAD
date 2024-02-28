## `Blender.Entity` Additions and Deletions:


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
        # if preset does not exist, create it.
        try:
            get_object(landmark.get_landmark_entity_name())
        except:  # noqa: E722
            presetXYZ = preset.get_xyz()
            self.create_landmark(landmark_name, presetXYZ[0], presetXYZ[1], presetXYZ[2])
            return landmark
    assert get_object(landmark.get_landmark_entity_name()) is not None, f'Landmark {landmark_name} does not exist for {self.name}.'
    return landmark
    ```
## `Blender.Part` Additions and Deletions:

- Added: `from providers.blender.blender_provider.landmark import Landmark`

## `Blender.Sketch` Additions and Deletions:

- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

- Added: `from codetocad.interfaces.wire_interface import WireInterface`

## `Blender.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Blender.Edge` Additions and Deletions:

- Added: `from codetocad.enums import *`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Blender.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.part_interface import PartInterface`

## `Blender.Landmark` Additions and Deletions:


- Deleted:
    ```python
    def rename(self, new_name: str):
    assert Landmark(new_name, self.parent_entity).is_exists() is False, f'{new_name} already exists.'
    parent_entityName = self.parent_entity
    if isinstance(parent_entityName, EntityInterface):
        parent_entityName = parent_entityName.name
    update_object_name(self.get_landmark_entity_name(), format_landmark_entity_name(parent_entityName, new_name))
    self.name = new_name
    return self
    ```

- Deleted:
    ```python
    def get_native_instance(self):
    return get_object(self.get_landmark_entity_name())
    ```
## `Blender.Joint` Additions and Deletions:

- Added: `from providers.blender.blender_provider.entity import Entity`

## `Blender.Material` Additions and Deletions:

## `Blender.Animation` Additions and Deletions:

- Added: `from providers.blender.blender_provider.entity import Entity`

## `Blender.Light` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Blender.Camera` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from codetocad.utilities import *`

- Added: `from codetocad.core import *`

- Added: `from codetocad.enums import *`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Blender.Render` Additions and Deletions:

## `Blender.Scene` Additions and Deletions:

## `Blender.Analytics` Additions and Deletions:

