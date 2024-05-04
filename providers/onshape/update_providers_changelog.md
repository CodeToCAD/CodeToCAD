## `Onshape.Entity` Additions and Deletions:

## `Onshape.Part` Additions and Deletions:

## `Onshape.Sketch` Additions and Deletions:


- Deleted:
    ```python
    def revolve(self, angle: 'str|float|Angle', about_entity_or_landmark: 'str|Entity', axis: 'str|int|Axis'='z') -> 'Part':
    raise NotImplementedError()
    ```

- Deleted:
    ```python
    def sweep(self, profile_name_or_instance: 'str|Sketch', fill_cap: 'bool'=True) -> 'Part':
    raise NotImplementedError()
    ```

- Deleted:
    ```python
    def profile(self, profile_curve_name: 'str'):
    return self
    ```
## `Onshape.Vertex` Additions and Deletions:

## `Onshape.Edge` Additions and Deletions:

## `Onshape.Wire` Additions and Deletions:


- Added:
    ```python
    def revolve(self, angle: 'str|float|Angle', about_entity_or_landmark: 'str|Entity', axis: 'str|int|Axis'='z') -> 'PartInterface':
    print('revolve called', f': {angle}, {about_entity_or_landmark}, {axis}')
    return Part('a part')
    ```

- Added:
    ```python
    def twist(self, angle: 'str|float|Angle', screw_pitch: 'str|float|Dimension', iterations: 'int'=1, axis: 'str|int|Axis'='z'):
    print('twist called', f': {angle}, {screw_pitch}, {iterations}, {axis}')
    return self
    ```

- Added:
    ```python
    def sweep(self, profile_name_or_instance: 'str|Sketch', fill_cap: 'bool'=True) -> 'PartInterface':
    print('sweep called', f': {profile_name_or_instance}, {fill_cap}')
    return Part('a part')
    ```

- Added:
    ```python
    def offset(self, radius: 'str|float|Dimension'):
    print('offset called', f': {radius}')
    return self
    ```

- Added:
    ```python
    def profile(self, profile_curve_name: 'str'):
    print('profile called', f': {profile_curve_name}')
    return self
    ```
- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

- Added: `from providers.onshape.onshape_provider.sketch import Sketch`

## `Onshape.Landmark` Additions and Deletions:

## `Onshape.Joint` Additions and Deletions:

## `Onshape.Material` Additions and Deletions:

## `Onshape.Animation` Additions and Deletions:

## `Onshape.Light` Additions and Deletions:

## `Onshape.Camera` Additions and Deletions:

## `Onshape.Render` Additions and Deletions:

## `Onshape.Scene` Additions and Deletions:

## `Onshape.Analytics` Additions and Deletions:

