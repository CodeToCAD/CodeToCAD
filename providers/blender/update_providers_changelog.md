## `Blender.Entity` Additions and Deletions:

- Added: `from typing import Self`

## `Blender.Part` Additions and Deletions:


- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def create_text(self, text: 'str', extrude_amount: 'str|float|Dimension', font_size: 'str|float|Dimension'=1.0, bold: 'bool'=False, italic: 'bool'=False, underlined: 'bool'=False, character_spacing: 'int'=1, word_spacing: 'int'=1, line_spacing: 'int'=1, font_file_path: 'str| None'=None, profile_curve_name: 'str|WireInterface|SketchInterface| None'=None, options: 'PartOptions| None'=None) -> Self:
    print('create_text called', f': {text}, {extrude_amount}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}, {profile_curve_name}, {options}')
    return self
    ```
- Added: `from typing import Self`

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Sketch` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.edge import Edge`

- Added: `from codetocad.proxy.wire import Wire`

- Added: `from codetocad.proxy.landmark import Landmark`

## `Blender.Vertex` Additions and Deletions:

## `Blender.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Blender.Wire` Additions and Deletions:

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

