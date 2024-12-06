## `Blender.Entity` Additions and Deletions:


- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def set_name(self, new_name: 'str', rename_linked_entities_and_landmarks: 'bool'=True) -> Self:
    print('set_name called', f': {new_name}, {rename_linked_entities_and_landmarks}')
    return self
    ```

- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def get_name(self) -> 'str':
    print('get_name called')
    return 'String'
    ```

- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def update_native_instance(self) -> 'object':
    print('update_native_instance called')
    return self
    ```
- Added: `from typing import Self`

- Added: `from codetocad.interfaces.native_instance_interface import NativeInstanceInterface`


- Deleted:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='Renames an object and its underlying data with the same name.')
def rename(self, new_name: 'str', renamelinked_entities_and_landmarks: 'bool'=True):
    assert Entity(new_name).is_exists() is False, f'{new_name} already exists.'
    update_object_name(self.name, new_name)
    if renamelinked_entities_and_landmarks:
        update_object_data_name(new_name, new_name)
        update_object_landmark_names(new_name, self.name, new_name)
    self.name = new_name
    return self
    ```
## `Blender.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.proxy.landmark import Landmark`

- Added: `from codetocad.proxy.wire import Wire`

## `Blender.Vertex` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Edge` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Blender.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

## `Blender.Landmark` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @supported(SupportLevel.SUPPORTED)
def get_landmark_entity_name(self) -> str:
    parent_entityName = self.parent_entity
    if isinstance(parent_entityName, EntityInterface):
        parent_entityName = parent_entityName.name
    entityName = format_landmark_entity_name(parent_entityName, self.name)
    return entityName
    ```
## `Blender.Joint` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Blender.Material` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @staticmethod
@supported(SupportLevel.SUPPORTED)
def get_preset(material_name: 'PresetMaterial'):
    if isinstance(material_name, str):
        try:
            material_name = getattr(PresetMaterial, material_name)
        except:  # noqa
            material = Material(material_name)
    if isinstance(material_name, PresetMaterial):
        material = Material(material_name.name)
        material.set_color(*material_name.color)
        material.set_reflectivity(material_name.reflectivity)
        material.set_roughness(material_name.roughness)
    return material
    ```
## `Blender.Animation` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Blender.Light` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Blender.Camera` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Blender.Render` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.camera import Camera`

## `Blender.Scene` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Analytics` Additions and Deletions:

- Added: `from typing import Self`

