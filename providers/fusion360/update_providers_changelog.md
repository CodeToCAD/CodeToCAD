## `Fusion360.Entity` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Part` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Sketch` Additions and Deletions:


- Added:
    ```python
    def create_line_to(self, to: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark', start_at: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None'='PresetLandmark.end', options: 'SketchOptions| None'=None) -> 'WireInterface':
    print('create_line_to called', f': {to}, {start_at}, {options}')
    return Wire('a wire', [Edge(v1=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), v2=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), name='an edge')])
    ```
- Added: `from typing import Self`

## `Fusion360.Vertex` Additions and Deletions:

## `Fusion360.Edge` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Wire` Additions and Deletions:


- Added:
    ```python
    def create_from_vertices(self, points: 'list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]', options: 'SketchOptions| None'=None) -> Self:
    print('create_from_vertices called', f': {points}, {options}')
    return self
    ```

- Added:
    ```python
    def create_point(self, point: 'str|list[str]|list[float]|list[Dimension]|Point', options: 'SketchOptions| None'=None) -> Self:
    print('create_point called', f': {point}, {options}')
    return self
    ```

- Added:
    ```python
    def create_line(self, length: 'str|float|Dimension', angle: 'str|float|Angle', start_at: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None'='PresetLandmark.end', options: 'SketchOptions| None'=None) -> Self:
    print('create_line called', f': {length}, {angle}, {start_at}, {options}')
    return self
    ```

- Added:
    ```python
    def create_line_to(self, to: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark', start_at: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None'='PresetLandmark.end', options: 'SketchOptions| None'=None) -> Self:
    print('create_line_to called', f': {to}, {start_at}, {options}')
    return self
    ```

- Added:
    ```python
    def create_arc(self, end_at: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface', radius: 'str|float|Dimension', start_at: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None'='PresetLandmark.end', flip: 'bool| None'=False, options: 'SketchOptions| None'=None) -> Self:
    print('create_arc called', f': {end_at}, {radius}, {start_at}, {flip}, {options}')
    return self
    ```
- Added: `from typing import Self`

- Added: `from codetocad.interfaces.vertex_interface import VertexInterface`

- Added: `from codetocad.interfaces.part_interface import PartInterface`

## `Fusion360.Landmark` Additions and Deletions:

## `Fusion360.Joint` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Material` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Animation` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Light` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Camera` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Render` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Scene` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Analytics` Additions and Deletions:

- Added: `from typing import Self`

