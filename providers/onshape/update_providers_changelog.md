## `Onshape.Entity` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Part` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.material import Material`

## `Onshape.Sketch` Additions and Deletions:


- Added:
    ```python
    def get_wires(self) -> 'list[WireInterface]':
    print('get_wires called')
    return [Wire('a wire', [Edge(v1=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), v2=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), name='an edge')])]
    ```
- Added: `from typing import Self`

- Added: `from codetocad.interfaces.wire_interface import WireInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

## `Onshape.Vertex` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

## `Onshape.Wire` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

## `Onshape.Landmark` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Joint` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Material` Additions and Deletions:

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

