## `Fusion360.Entity` Additions and Deletions:


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
    @supported(SupportLevel.PARTIAL, 'Does not support the rename_linked_entities_and_landmarks parameter yet.')
def rename(self, new_name: 'str', renamelinked_entities_and_landmarks: 'bool'=True):
    if isinstance(self, PartInterface):
        FusionBody(self.name).rename(new_name)
    if isinstance(self, SketchInterface):
        FusionSketch(self.name).rename(new_name)
    if isinstance(self, LandmarkInterface):
        FusionLandmark(self.name, self.get_parent_entity().get_native_instance()).rename(new_name)
    self.name = new_name
    return self
    ```
## `Fusion360.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.proxy.material import Material`

## `Fusion360.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

## `Fusion360.Vertex` Additions and Deletions:

## `Fusion360.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Fusion360.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.sketch import Sketch`

## `Fusion360.Landmark` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @supported(SupportLevel.SUPPORTED)
def get_landmark_entity_name(self) -> str:
    return self._fusion_landmark.instance.name
    ```
## `Fusion360.Joint` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Fusion360.Material` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @staticmethod
@supported(SupportLevel.SUPPORTED)
def get_preset(material_name: 'PresetMaterial'):
    if isinstance(material_name, str):
        try:
            material_name = getattr(PresetMaterial, material_name)
        except:
            raise Exception(f'Preset {material_name} not found!')
    if isinstance(material_name, PresetMaterial):
        material = Material(material_name.name)
        material.set_color(*material_name.color)
        material.set_reflectivity(material_name.reflectivity)
        material.set_roughness(material_name.roughness)
    return material
    ```
## `Fusion360.Animation` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Fusion360.Light` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Fusion360.Camera` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Fusion360.Render` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.proxy.camera import Camera`

## `Fusion360.Scene` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Analytics` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

