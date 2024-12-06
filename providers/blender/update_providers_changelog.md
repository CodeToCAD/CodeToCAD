## `Blender.Entity` Additions and Deletions:

- Added: `from codetocad.interfaces.native_instance_interface import NativeInstanceInterface`

## `Blender.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.proxy.wire import Wire`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Vertex` Additions and Deletions:

## `Blender.Edge` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Blender.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

## `Blender.Landmark` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @supported(SupportLevel.SUPPORTED)
def get_parent_entity(self) -> 'EntityInterface':
    if isinstance(self.parent_entity, str):
        return Entity(self.parent_entity)
    return self.parent_entity
    ```
## `Blender.Joint` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Blender.Material` Additions and Deletions:


- Added:
    ```python
    @staticmethod
@supported(SupportLevel.SUPPORTED, notes='')
def get_preset(parameter: 'PresetMaterial') -> 'MaterialInterface':
    print('get_preset called', f': {parameter}')
    return self
    ```
- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

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

