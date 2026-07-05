"""Build a cube with a hole in Build123D and export it as an STL.

Run with: codetocad examples/build123d_cube_with_hole.py
(requires the build123d extra: uv sync --extra build123d)
"""

from codetocad_integrations.build123d import make_cube

if __name__ == "__main__":
    cube = make_cube("10cm", "10cm", "5cm")
    cube.hole(cube.top_center, radius="4cm", amount="5cm")
    cube.export("my_cube.stl")
    print(f"Exported my_cube.stl (volume: {cube.get_volume():.6f} m^3)")
