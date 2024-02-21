## `Onshape.Entity` Additions and Deletions:


- Deleted:
    ```python
    def create_landmark(self, landmark_name: str, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue) -> 'Landmark':
    raise NotImplementedError()
    ```
## `Onshape.Part` Additions and Deletions:


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

- Added: `from providers.onshape.onshape_provider.material import Material`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

- Added: `from providers.onshape.onshape_provider.landmark import Landmark`

## `Onshape.Sketch` Additions and Deletions:


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

- Added: `from providers.onshape.onshape_provider.entity import Entity`

- Added: `from providers.onshape.onshape_provider.vertex import Vertex`

- Added: `from providers.onshape.onshape_provider.landmark import Landmark`

- Added: `from providers.onshape.onshape_provider.part import Part`

- Added: `from providers.onshape.onshape_provider.wire import Wire`

- Added: `from providers.onshape.onshape_provider.edge import Edge`


- Deleted:
    ```python
    @classmethod
def setUpClass(cls) -> None:
    import os
    configPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../.onshape_client_config.yaml')
    cls.client = get_onshape_client_with_config_file(config_filepath=configPath)
    cls.onshape_url = get_first_document_url_by_name(cls.client, onshape_document_name)
    ```
## `Onshape.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Edge` Additions and Deletions:


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

- Added: `from providers.onshape.onshape_provider.entity import Entity`

- Added: `from providers.onshape.onshape_provider.vertex import Vertex`

- Added: `from providers.onshape.onshape_provider.landmark import Landmark`

## `Onshape.Wire` Additions and Deletions:


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
- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`

- Added: `from codetocad.interfaces.part_interface import PartInterface`

- Added: `from codetocad.interfaces.edge_interface import EdgeInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

- Added: `from providers.onshape.onshape_provider.vertex import Vertex`

- Added: `from providers.onshape.onshape_provider.landmark import Landmark`

- Added: `from providers.onshape.onshape_provider.part import Part`

- Added: `from providers.onshape.onshape_provider.edge import Edge`

## `Onshape.Landmark` Additions and Deletions:


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

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Joint` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Material` Additions and Deletions:


- Added:
    ```python
    @staticmethod
def get_preset(parameter: 'PresetMaterial') -> 'MaterialInterface':
    print('get_preset called', f': {parameter}')
    return Material('mat')
    ```
## `Onshape.Animation` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Light` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Camera` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Render` Additions and Deletions:

- Added: `from codetocad.interfaces.camera_interface import CameraInterface`

- Added: `from providers.onshape.onshape_provider.camera import Camera`

## `Onshape.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

## `Onshape.Analytics` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.onshape.onshape_provider.entity import Entity`

