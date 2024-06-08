## `Blender.Entity` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Part` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Sketch` Additions and Deletions:


- Added:
    ```python
    def create_line_to(self, to: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark', start_at: 'str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None'='PresetLandmark.end', options: 'SketchOptions| None'=None) -> 'WireInterface':
    print('create_line_to called', f': {to}, {start_at}, {options}')
    return Wire('a wire', [Edge(v1=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), v2=Vertex('a vertex', Point.from_list_of_float_or_string([0, 0, 0])), name='an edge')])
    ```
- Added: `from typing import Self`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.wire import Wire`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Vertex` Additions and Deletions:

## `Blender.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Blender.Wire` Additions and Deletions:


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

## `Blender.Landmark` Additions and Deletions:

## `Blender.Joint` Additions and Deletions:

- Added: `from codetocad.codetocad_types import *`

- Added: `from typing import Self`

## `Blender.Material` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Animation` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Light` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Camera` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Render` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Scene` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Analytics` Additions and Deletions:

- Added: `from typing import Self`

