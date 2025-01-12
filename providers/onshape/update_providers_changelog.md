## `Onshape.Entity` Additions and Deletions:

- Added: `from codetocad.interfaces.native_instance_interface import NativeInstanceInterface`

## `Onshape.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.proxy.sketch import Sketch`

- Added: `from codetocad.proxy.material import Material`

## `Onshape.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

## `Onshape.Vertex` Additions and Deletions:


- Deleted:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def get_parent_edge(self) -> 'object':
    print('get_parent_edge called')
    return 'instance'
    ```
## `Onshape.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

## `Onshape.Wire` Additions and Deletions:


- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def get_parent(self) -> 'EntityInterface':
    print('get_parent called')
    return __import__('codetocad').Part('an entity')
    ```
- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.sketch import Sketch`

## `Onshape.Landmark` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Joint` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.entity import Entity`

## `Onshape.Material` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

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

