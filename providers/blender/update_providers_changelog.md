## `Blender.Entity` Additions and Deletions:

## `Blender.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.booleanable_interface import BooleanableInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.landmark import Landmark`

- Added: `from codetocad.proxy.material import Material`

## `Blender.Sketch` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.wire import Wire`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Vertex` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

## `Blender.Edge` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Wire` Additions and Deletions:


- Added:
    ```python
    def get_edges(self) -> 'list[EdgeInterface]':
    print('get_edges called')
    return [Edge(v1=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), v2=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), name='an edge')]
    ```

- Added:
    ```python
    def remesh(self, strategy: 'str', amount: 'float'):
    print('remesh called', f': {strategy}, {amount}')
    return self
    ```

- Added:
    ```python
    def subdivide(self, amount: 'float'):
    print('subdivide called', f': {amount}')
    return self
    ```

- Added:
    ```python
    def decimate(self, amount: 'float'):
    print('decimate called', f': {amount}')
    return self
    ```
- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.booleanable_interface import BooleanableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.landmark import Landmark`

- Added: `from codetocad.proxy.part import Part`

## `Blender.Landmark` Additions and Deletions:

## `Blender.Joint` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from codetocad.proxy.entity import Entity`

## `Blender.Material` Additions and Deletions:

## `Blender.Animation` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from codetocad.proxy.entity import Entity`

## `Blender.Light` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

## `Blender.Camera` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

## `Blender.Render` Additions and Deletions:

- Added: `from codetocad.proxy.camera import Camera`

## `Blender.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.proxy.entity import Entity`

## `Blender.Analytics` Additions and Deletions:

- Added: `from codetocad.proxy.entity import Entity`

