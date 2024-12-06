## `Fusion360.Entity` Additions and Deletions:

- Added: `from codetocad.interfaces.native_instance_interface import NativeInstanceInterface`

## `Fusion360.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.material import Material`

## `Fusion360.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

## `Fusion360.Vertex` Additions and Deletions:

## `Fusion360.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Fusion360.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.sketch import Sketch`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Fusion360.Landmark` Additions and Deletions:

- Added: `from typing import Self`


- Deleted:
    ```python
    @supported(SupportLevel.SUPPORTED)
def get_parent_entity(self) -> 'EntityInterface':
    if isinstance(self.parent_entity, str):
        return Entity(self.parent_entity)
    return self.parent_entity
    ```
## `Fusion360.Joint` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Fusion360.Material` Additions and Deletions:


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

