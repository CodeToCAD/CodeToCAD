from codetocad import *

starting_letter_ascii = ord("a")

for letter_ascii in range(starting_letter_ascii, starting_letter_ascii + 26):
    letter = chr(letter_ascii)

    extrude_amount = 0.2

    letter_sketch = Sketch(letter).create_text(letter)
    letter_sketch.extrude(extrude_amount)
    letter_sketch.rotate_xyz(90, 0, -90)

    if letter_ascii == starting_letter_ascii:
        continue

    previous_letter = chr(letter_ascii - 1)

    desired_spacing = 1

    limit_x = desired_spacing - extrude_amount * 2

    Joint(
        Sketch(previous_letter).get_landmark("center"),
        Sketch(letter).get_landmark("center"),
    ).limit_location_xyz(desired_spacing, 0, 0)
