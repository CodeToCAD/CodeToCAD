## `Fusion360.Entity` Additions and Deletions:

## `Fusion360.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.material_interface import MaterialInterface`

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

## `Fusion360.Sketch` Additions and Deletions:

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.wire_interface import WireInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.importable_interface import ImportableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.scalable_interface import ScalableInterface`

- Added: `from codetocad.interfaces.projectable_interface import ProjectableInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.wire import Wire`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Fusion360.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.projectable_interface import ProjectableInterface`

## `Fusion360.Edge` Additions and Deletions:

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.projectable_interface import ProjectableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Fusion360.Wire` Additions and Deletions:


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

- Added: `from codetocad.interfaces.part_interface import PartInterface`

- Added: `from codetocad.interfaces.patternable_interface import PatternableInterface`

- Added: `from codetocad.interfaces.mirrorable_interface import MirrorableInterface`

- Added: `from codetocad.interfaces.subdividable_interface import SubdividableInterface`

- Added: `from codetocad.interfaces.projectable_interface import ProjectableInterface`

- Added: `from codetocad.interfaces.booleanable_interface import BooleanableInterface`

- Added: `from codetocad.interfaces.landmarkable_interface import LandmarkableInterface`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.landmark import Landmark`

- Added: `from codetocad.proxy.part import Part`

## `Fusion360.Landmark` Additions and Deletions:

## `Fusion360.Joint` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.proxy.entity import Entity`

## `Fusion360.Material` Additions and Deletions:

## `Fusion360.Animation` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.proxy.entity import Entity`

## `Fusion360.Light` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

## `Fusion360.Camera` Additions and Deletions:

## `Fusion360.Render` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from codetocad.interfaces.camera_interface import CameraInterface`

- Added: `from codetocad.proxy.camera import Camera`

## `Fusion360.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.exportable_interface import ExportableInterface`

- Added: `from codetocad.proxy.entity import Entity`

## `Fusion360.Analytics` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.proxy.entity import Entity`

