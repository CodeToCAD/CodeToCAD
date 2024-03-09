## `Fusion360.Entity` Additions and Deletions:

## `Fusion360.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.part_interface import PartInterface`

## `Fusion360.Sketch` Additions and Deletions:

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

## `Fusion360.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

## `Fusion360.Edge` Additions and Deletions:

- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

## `Fusion360.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.wire_interface import WireInterface`

## `Fusion360.Landmark` Additions and Deletions:

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`


- Deleted:
    ```python
    def get_location_local(self) -> 'Point':
    print('get_location_local called')
    return Point.from_list_of_float_or_string([0, 0, 0])
    ```
## `Fusion360.Joint` Additions and Deletions:

- Added: `from codetocad.interfaces.joint_interface import JointInterface`

## `Fusion360.Material` Additions and Deletions:

- Added: `from codetocad.interfaces.material_interface import MaterialInterface`

## `Fusion360.Animation` Additions and Deletions:

- Added: `from codetocad.interfaces.animation_interface import AnimationInterface`

## `Fusion360.Light` Additions and Deletions:

- Added: `from codetocad.interfaces.light_interface import LightInterface`

## `Fusion360.Camera` Additions and Deletions:

- Added: `from codetocad.interfaces.camera_interface import CameraInterface`

## `Fusion360.Render` Additions and Deletions:

- Added: `from codetocad.interfaces.render_interface import RenderInterface`

## `Fusion360.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces.scene_interface import SceneInterface`

## `Fusion360.Analytics` Additions and Deletions:

- Added: `from codetocad.interfaces.analytics_interface import AnalyticsInterface`

