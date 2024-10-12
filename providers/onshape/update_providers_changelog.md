## `Onshape.Entity` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Part` Additions and Deletions:


- Added:
    ```python
    @supported(SupportLevel.SUPPORTED, notes='')
def create_text(self, text: 'str', extrude_amount: 'str|float|Dimension', font_size: 'str|float|Dimension'=1.0, bold: 'bool'=False, italic: 'bool'=False, underlined: 'bool'=False, character_spacing: 'int'=1, word_spacing: 'int'=1, line_spacing: 'int'=1, font_file_path: 'str| None'=None, profile_curve_name: 'str|WireInterface|SketchInterface| None'=None, options: 'PartOptions| None'=None) -> Self:
    print('create_text called', f': {text}, {extrude_amount}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}, {profile_curve_name}, {options}')
    return self
    ```
- Added: `from typing import Self`

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

## `Onshape.Sketch` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Vertex` Additions and Deletions:

## `Onshape.Edge` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Wire` Additions and Deletions:

- Added: `from codetocad.interfaces.sketch_interface import SketchInterface`

## `Onshape.Landmark` Additions and Deletions:

## `Onshape.Joint` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Material` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Animation` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Light` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Camera` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Render` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Scene` Additions and Deletions:

- Added: `from typing import Self`

## `Onshape.Analytics` Additions and Deletions:

- Added: `from typing import Self`

