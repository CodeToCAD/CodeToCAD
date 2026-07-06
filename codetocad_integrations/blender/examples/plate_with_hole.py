"""A plate with a through-hole, built in Blender.

Run with a normal Python interpreter — ensure_blender() relaunches the
script under `blender --background` automatically:

    codetocad plate_with_hole.py
"""

from codetocad_integrations.blender import ensure_blender, make_cube

if __name__ == "__main__":
    ensure_blender()

    plate = make_cube("80mm", "60mm", "10mm")
    plate.hole(plate.top_center, radius="11mm", amount="10mm")
    plate.export("plate_with_hole.stl")
    print(f"volume: {plate.get_volume() * 1e9:.0f} mm^3")
