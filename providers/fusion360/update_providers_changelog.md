## `Fusion360.Entity` Additions and Deletions:


- Deleted:
    ```python
    @property
def center(self):
    from . import Part, Sketch
    if isinstance(self, Part):
        return self.fusion_body.center
    if isinstance(self, Sketch):
        return self.fusion_sketch.center
    ```

- Deleted:
    ```python
    def create_landmark(self, landmark_name: 'str', x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue) -> 'Landmark':
    from . import Landmark
    boundingBox = self.fusion_body.get_bounding_box()
    localPositions = [Dimension.from_dimension_or_its_float_or_string_value(x, boundingBox.x), Dimension.from_dimension_or_its_float_or_string_value(y, boundingBox.y), Dimension.from_dimension_or_its_float_or_string_value(z, boundingBox.z)]
    landmark = Landmark(landmark_name, self)
    landmark.fusion_landmark.create_landmark(localPositions[0].value, localPositions[1].value, localPositions[2].value)
    return landmark
    ```
## `Fusion360.Part` Additions and Deletions:


- Added:
    ```python
    def create_landmark(self, landmark_name: 'str', x: 'DimensionOrItsFloatOrStringValue', y: 'DimensionOrItsFloatOrStringValue', z: 'DimensionOrItsFloatOrStringValue') -> 'LandmarkInterface':
    print('create_landmark called', f': {landmark_name}, {x}, {y}, {z}')
    return Landmark('name', 'parent')
    ```

- Added:
    ```python
    def get_landmark(self, landmark_name: 'PresetLandmarkOrItsName') -> 'LandmarkInterface':
    print('get_landmark called', f': {landmark_name}')
    return Landmark('name', 'parent')
    ```
- Added: `from codetocad.interfaces.material_interface import MaterialInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`

- Added: `from providers.fusion360.fusion360_provider.material import Material`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

- Added: `from providers.fusion360.fusion360_provider.landmark import Landmark`

## `Fusion360.Sketch` Additions and Deletions:


- Added:
    ```python
    def create_landmark(self, landmark_name: 'str', x: 'DimensionOrItsFloatOrStringValue', y: 'DimensionOrItsFloatOrStringValue', z: 'DimensionOrItsFloatOrStringValue') -> 'LandmarkInterface':
    print('create_landmark called', f': {landmark_name}, {x}, {y}, {z}')
    return Landmark('name', 'parent')
    ```

- Added:
    ```python
    def get_landmark(self, landmark_name: 'PresetLandmarkOrItsName') -> 'LandmarkInterface':
    print('get_landmark called', f': {landmark_name}')
    return Landmark('name', 'parent')
    ```
- Added: `from codetocad.interfaces import SketchInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`

- Added: `from codetocad.interfaces.part_interface import PartInterface`

- Added: `from codetocad.interfaces.wire_interface import WireInterface`

- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

- Added: `from providers.fusion360.fusion360_provider.vertex import Vertex`

- Added: `from providers.fusion360.fusion360_provider.landmark import Landmark`

- Added: `from providers.fusion360.fusion360_provider.part import Part`

- Added: `from providers.fusion360.fusion360_provider.wire import Wire`

- Added: `from providers.fusion360.fusion360_provider.edge import Edge`

## `Fusion360.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`


- Deleted:
    ```python
    @property
def center(self):
    return self.location
    ```
## `Fusion360.Edge` Additions and Deletions:


- Added:
    ```python
    def create_landmark(self, landmark_name: 'str', x: 'DimensionOrItsFloatOrStringValue', y: 'DimensionOrItsFloatOrStringValue', z: 'DimensionOrItsFloatOrStringValue') -> 'LandmarkInterface':
    print('create_landmark called', f': {landmark_name}, {x}, {y}, {z}')
    return Landmark('name', 'parent')
    ```

- Added:
    ```python
    def get_landmark(self, landmark_name: 'PresetLandmarkOrItsName') -> 'LandmarkInterface':
    print('get_landmark called', f': {landmark_name}')
    return Landmark('name', 'parent')
    ```
- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

- Added: `from providers.fusion360.fusion360_provider.vertex import Vertex`

- Added: `from providers.fusion360.fusion360_provider.landmark import Landmark`


- Deleted:
    ```python
    @classmethod
def get_dummy_edge(cls):
    return cls(v1=(0, 5), v2=(5, 10), name='dummy')
    ```
## `Fusion360.Wire` Additions and Deletions:


- Added:
    ```python
    def create_landmark(self, landmark_name: 'str', x: 'DimensionOrItsFloatOrStringValue', y: 'DimensionOrItsFloatOrStringValue', z: 'DimensionOrItsFloatOrStringValue') -> 'LandmarkInterface':
    print('create_landmark called', f': {landmark_name}, {x}, {y}, {z}')
    return Landmark('name', 'parent')
    ```

- Added:
    ```python
    def get_landmark(self, landmark_name: 'PresetLandmarkOrItsName') -> 'LandmarkInterface':
    print('get_landmark called', f': {landmark_name}')
    return Landmark('name', 'parent')
    ```

- Added:
    ```python
    def union(self, other: 'BooleanableOrItsName', delete_after_union: 'bool'=True, is_transfer_data: 'bool'=False):
    print('union called', f': {other}, {delete_after_union}, {is_transfer_data}')
    return self
    ```

- Added:
    ```python
    def subtract(self, other: 'BooleanableOrItsName', delete_after_subtract: 'bool'=True, is_transfer_data: 'bool'=False):
    print('subtract called', f': {other}, {delete_after_subtract}, {is_transfer_data}')
    return self
    ```

- Added:
    ```python
    def intersect(self, other: 'BooleanableOrItsName', delete_after_intersect: 'bool'=True, is_transfer_data: 'bool'=False):
    print('intersect called', f': {other}, {delete_after_intersect}, {is_transfer_data}')
    return self
    ```
- Added: `from codetocad.interfaces import WireInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`

- Added: `from codetocad.interfaces.part_interface import PartInterface`

- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

- Added: `from providers.fusion360.fusion360_provider.vertex import Vertex`

- Added: `from providers.fusion360.fusion360_provider.landmark import Landmark`

- Added: `from providers.fusion360.fusion360_provider.part import Part`

- Added: `from providers.fusion360.fusion360_provider.edge import Edge`

## `Fusion360.Landmark` Additions and Deletions:


- Added:
    ```python
    def get_location_world(self) -> 'Point':
    print('get_location_world called')
    return Point.from_list_of_float_or_string([0, 0, 0])
    ```

- Added:
    ```python
    def get_location_local(self) -> 'Point':
    print('get_location_local called')
    return Point.from_list_of_float_or_string([0, 0, 0])
    ```

- Added:
    ```python
    def translate_xyz(self, x: 'DimensionOrItsFloatOrStringValue', y: 'DimensionOrItsFloatOrStringValue', z: 'DimensionOrItsFloatOrStringValue'):
    print('translate_xyz called', f': {x}, {y}, {z}')
    return self
    ```
- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

## `Fusion360.Joint` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`


- Deleted:
    ```python
    @classmethod
def get_dummy_obj(cls):
    from . import Sketch
    instance = Sketch('mySketch')
    edge = instance.create_line(end_at=(0, 5, 0), start_at=(5, 10, 0))
    instance = Sketch('mySketch')
    edge2 = instance.create_line(end_at=(5, 10, 0), start_at=(5, 5, 0))
    return cls(entity1='mySketch', entity2='mySketch2')
    ```
## `Fusion360.Material` Additions and Deletions:

## `Fusion360.Animation` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

## `Fusion360.Light` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`


- Deleted:
    ```python
    @classmethod
def get_sample_light(cls):
    return cls(name='test-light', description='light instance for testing')
    ```
## `Fusion360.Camera` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`


- Deleted:
    ```python
    def translate_xyz(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue):
    x = Dimension.from_dimension_or_its_float_or_string_value(x, None).value
    y = Dimension.from_dimension_or_its_float_or_string_value(y, None).value
    z = Dimension.from_dimension_or_its_float_or_string_value(z, None).value
    self.fusion_camera.translate(x, y, z)
    return self
    ```
## `Fusion360.Render` Additions and Deletions:

- Added: `from codetocad.interfaces.camera_interface import CameraInterface`

- Added: `from providers.fusion360.fusion360_provider.camera import Camera`

## `Fusion360.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`


- Deleted:
    ```python
    @classmethod
def get_sample_scene(cls):
    return cls(name='myScene', description='this is for testing purpose')
    ```
## `Fusion360.Analytics` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.fusion360.fusion360_provider.entity import Entity`

