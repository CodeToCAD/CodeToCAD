## `Onshape.Entity` Additions and Deletions:

## `Onshape.Part` Additions and Deletions:

- Added: `from codetocad.interfaces.part_interface import PartInterface`

## `Onshape.Sketch` Additions and Deletions:

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

## `Onshape.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

## `Onshape.Edge` Additions and Deletions:

- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

## `Onshape.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.wire_interface import WireInterface`

## `Onshape.Landmark` Additions and Deletions:

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`


- Deleted:
    ```python
    def get_location_local(self) -> 'Point':
    print('get_location_local called')
    return Point.from_list_of_float_or_string([0, 0, 0])
    ```
## `Onshape.Joint` Additions and Deletions:

- Added: `from codetocad.interfaces.joint_interface import JointInterface`

## `Onshape.Material` Additions and Deletions:

- Added: `from codetocad.interfaces.material_interface import MaterialInterface`

## `Onshape.Animation` Additions and Deletions:

- Added: `from codetocad.interfaces.animation_interface import AnimationInterface`

## `Onshape.Light` Additions and Deletions:

- Added: `from codetocad.interfaces.light_interface import LightInterface`

## `Onshape.Camera` Additions and Deletions:

- Added: `from codetocad.interfaces.camera_interface import CameraInterface`

## `Onshape.Render` Additions and Deletions:

- Added: `from codetocad.interfaces.render_interface import RenderInterface`

## `Onshape.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces.scene_interface import SceneInterface`

## `Onshape.Analytics` Additions and Deletions:

- Added: `from codetocad.interfaces.analytics_interface import AnalyticsInterface`

