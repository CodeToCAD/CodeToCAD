## `Blender.Entity` Additions and Deletions:

- Added: `from codetocad.interfaces import EntityInterface`


- Deleted:
    ```python
    def create_landmark(self, landmark_name: str, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue) -> 'Landmark':
    boundingBox = get_bounding_box(self.name)
    localPositions = [Dimension.from_dimension_or_its_float_or_string_value(x, boundingBox.x), Dimension.from_dimension_or_its_float_or_string_value(y, boundingBox.y), Dimension.from_dimension_or_its_float_or_string_value(z, boundingBox.z)]
    localPositions = blender_definitions.BlenderLength.convert_dimensions_to_blender_unit(localPositions)
    landmark = Landmark(landmark_name, self.name)
    landmarkObjectName = landmark.get_landmark_entity_name()
    # Create an Empty object to represent the landmark
    # Using an Empty object allows us to parent the object to this Empty.
    # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
    # This might not work in other CodeToCAD implementations, but it does in Blender
    empty_object = create_object(landmarkObjectName, None)
    empty_object.empty_display_size = 0
    # Assign the landmark to the parent's collection
    assign_object_to_collection(landmarkObjectName, get_object_collection_name(self.name))
    # Parent the landmark to the object
    make_parent(landmarkObjectName, self.name)
    translate_object(landmarkObjectName, localPositions, blender_definitions.BlenderTranslationTypes.ABSOLUTE)  # type: ignore
    return landmark
    ```
## `Blender.Part` Additions and Deletions:


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
- Added: `from codetocad.interfaces import PartInterface`

- Added: `from codetocad.interfaces.material_interface import MaterialInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from codetocad.interfaces.landmark_interface import LandmarkInterface`

- Added: `from providers.blender.blender_provider.material import Material`

- Added: `from providers.blender.blender_provider.entity import Entity`

- Added: `from providers.blender.blender_provider.landmark import Landmark`


- Deleted:
    ```python
    def bevel(self, radius: DimensionOrItsFloatOrStringValue, bevel_edges_nearlandmark_names: Optional[list[LandmarkOrItsName]]=None, bevel_faces_nearlandmark_names: Optional[list[LandmarkOrItsName]]=None, use_width=False, chamfer=False, keyword_arguments: Optional[dict]=None):
    vertex_group_name = None
    if bevel_edges_nearlandmark_names is not None:
        vertex_group_name = create_uuid_like_id()
        self._add_edges_near_landmarks_to_vertex_group(bevel_edges_nearlandmark_names, vertex_group_name)
    if bevel_faces_nearlandmark_names is not None:
        vertex_group_name = vertex_group_name or create_uuid_like_id()
        self._add_faces_near_landmarks_to_vertex_group(bevel_faces_nearlandmark_names, vertex_group_name)
    radiusDimension = Dimension.from_string(radius)
    radiusDimension = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(radiusDimension)
    apply_bevel_modifier(self.name, radiusDimension, vertex_group_name=vertex_group_name, use_edges=True, use_width=use_width, chamfer=chamfer, **keyword_arguments or {})
    return self._apply_modifiers_only()
    ```
## `Blender.Sketch` Additions and Deletions:


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

- Added: `from providers.blender.blender_provider.entity import Entity`

- Added: `from providers.blender.blender_provider.vertex import Vertex`

- Added: `from providers.blender.blender_provider.landmark import Landmark`

- Added: `from providers.blender.blender_provider.part import Part`

- Added: `from providers.blender.blender_provider.wire import Wire`

- Added: `from providers.blender.blender_provider.edge import Edge`

## `Blender.Vertex` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`


- Deleted:
    ```python
    @property
    def location(self) -> Point:
        return get_vertex_location_from_blender_point(self.native_instance)
    ```
## `Blender.Edge` Additions and Deletions:


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

- Added: `from providers.blender.blender_provider.entity import Entity`

- Added: `from providers.blender.blender_provider.vertex import Vertex`

- Added: `from providers.blender.blender_provider.landmark import Landmark`


- Deleted:
    ```python
    def get_native_instance(self) -> object:
    return self.native_instance
    ```
## `Blender.Wire` Additions and Deletions:


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

- Added: `from providers.blender.blender_provider.entity import Entity`

- Added: `from providers.blender.blender_provider.vertex import Vertex`

- Added: `from providers.blender.blender_provider.landmark import Landmark`

- Added: `from providers.blender.blender_provider.part import Part`

- Added: `from providers.blender.blender_provider.edge import Edge`


- Deleted:
    ```python
    def get_native_instance(self) -> object:
    return self.native_instance
    ```
## `Blender.Landmark` Additions and Deletions:


- Added:
    ```python
    def translate_xyz(self, x: 'DimensionOrItsFloatOrStringValue', y: 'DimensionOrItsFloatOrStringValue', z: 'DimensionOrItsFloatOrStringValue'):
    print('translate_xyz called', f': {x}, {y}, {z}')
    return self
    ```
- Added: `from codetocad.interfaces import LandmarkInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`


- Deleted:
    ```python
    def is_exists(self) -> bool:
    try:
        return get_object(self.get_landmark_entity_name()) is not None
    except:  # noqa E722
        return False
    ```

- Deleted:
    ```python
    def delete(self):
    remove_object(self.get_landmark_entity_name())
    return self
    ```

- Deleted:
    ```python
    def set_visible(self, is_visible: bool):
    set_object_visibility(self.get_landmark_entity_name(), is_visible)
    return self
    ```

- Deleted:
    ```python
    def select(self):
    select_object(self.get_landmark_entity_name())
    return self
    ```
## `Blender.Joint` Additions and Deletions:

- Added: `from codetocad.interfaces import JointInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`

## `Blender.Material` Additions and Deletions:

- Added: `from codetocad.interfaces import MaterialInterface`

## `Blender.Animation` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`

## `Blender.Light` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`


- Deleted:
    ```python
    def translate_xyz(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue):
    Entity(self.name).translate_xyz(x, y, z)
    return self
    ```

- Deleted:
    ```python
    def is_exists(self) -> bool:
    return Entity(self.name).is_exists()
    ```

- Deleted:
    ```python
    def delete(self):
    Entity(self.name).delete(False)
    return self
    ```

- Deleted:
    ```python
    def get_location_world(self) -> 'Point':
    return Entity(self.name).get_location_world()
    ```

- Deleted:
    ```python
    def select(self):
    Entity(self.name).select()
    return self
    ```
## `Blender.Camera` Additions and Deletions:

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`


- Deleted:
    ```python
    def create_panoramic(self):
    create_camera(self.name, type='PANO')
    return self
    ```

- Deleted:
    ```python
    def translate_xyz(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue):
    Entity(self.name).translate_xyz(x, y, z)
    return self
    ```

- Deleted:
    ```python
    def is_exists(self) -> bool:
    return Entity(self.name).is_exists()
    ```

- Deleted:
    ```python
    def delete(self):
    Entity(self.name).delete(False)
    return self
    ```

- Deleted:
    ```python
    def get_location_world(self) -> 'Point':
    return Entity(self.name).get_location_world()
    ```

- Deleted:
    ```python
    def select(self):
    Entity(self.name).select()
    return self
    ```
## `Blender.Render` Additions and Deletions:

- Added: `from codetocad.interfaces.camera_interface import CameraInterface`

- Added: `from providers.blender.blender_provider.camera import Camera`

## `Blender.Scene` Additions and Deletions:

- Added: `from codetocad.interfaces import SceneInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`

## `Blender.Analytics` Additions and Deletions:

- Added: `from codetocad.interfaces import AnalyticsInterface`

- Added: `from codetocad.interfaces.entity_interface import EntityInterface`

- Added: `from providers.blender.blender_provider.entity import Entity`

