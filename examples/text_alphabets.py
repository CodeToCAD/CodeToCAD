from codetocad import *

starting_letter_ascii = ord('a')

for letter_ascii in range(starting_letter_ascii, starting_letter_ascii+26):
    letter = chr(letter_ascii)

    Sketch(letter).create_text(letter)

    if letter_ascii == starting_letter_ascii:
        continue

    previous_letter = chr(letter_ascii-1)

    Joint(
        Sketch(previous_letter),
        Sketch(letter)
    ).limit_location_x(1)
