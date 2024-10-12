## `Fusion360.Entity` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Part` Additions and Deletions:


- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def create_text(self, text: 'str', extrude_amount: 'str|float|Dimension', font_size: 'str|float|Dimension'=1.0, bold: 'bool'=False, italic: 'bool'=False, underlined: 'bool'=False, character_spacing: 'int'=1, word_spacing: 'int'=1, line_spacing: 'int'=1, font_file_path: 'str| None'=None, profile_curve_name: 'str|WireInterface|SketchInterface| None'=None, options: 'PartOptions| None'=None) -> Self:
    print('create_text called', f': {text}, {extrude_amount}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}, {profile_curve_name}, {options}')
    return self
    ```
- Added: `from typing import Self`

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

## `Fusion360.Sketch` Additions and Deletions:

- Added: `from typing import Self`

## `Fusion360.Vertex` Additions and Deletions:

## `Fusion360.Edge` Additions and Deletions:

- Added: `from typing import Self`

- Added: `from codetocad.proxy.vertex import Vertex`

## `Fusion360.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

- Added: `from codetocad.proxy.vertex import Vertex`

- Added: `from codetocad.proxy.edge import Edge`

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

