## `Onshape.Entity` Additions and Deletions:


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
    @supported(SupportLevel.UNSUPPORTED)
def rename(self, new_name: 'str', renamelinked_entities_and_landmarks: 'bool'=True):
    return self
    ```
## `Onshape.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.proxy.material import Material`

- Added: `from codetocad.proxy.sketch import Sketch`

## `Onshape.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

## `Onshape.Vertex` Additions and Deletions:

## `Onshape.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

## `Onshape.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.proxy.sketch import Sketch`

## `Onshape.Landmark` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @supported(SupportLevel.UNSUPPORTED)
def get_landmark_entity_name(self) -> str:
    raise NotImplementedError()
    ```
## `Onshape.Joint` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Material` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @staticmethod
@supported(SupportLevel.UNSUPPORTED)
def get_preset(material_name: 'PresetMaterial') -> 'MaterialInterface':
    print('get_preset called', f': {parameter}')
    return Material('mat')
    ```
## `Onshape.Animation` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Onshape.Light` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Onshape.Camera` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

## `Onshape.Render` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

- Added: `from codetocad.proxy.camera import Camera`

## `Onshape.Scene` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Analytics` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

