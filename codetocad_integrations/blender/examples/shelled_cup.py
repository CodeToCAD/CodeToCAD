"""The CodeToCAD cup: a shelled cylinder with an aluminum material, built in
Blender and saved as both an STL and a .blend scene.

    codetocad shelled_cup.py
"""

from codetocad import aluminum_material
from codetocad_integrations.blender import ensure_blender, make_cylinder

if __name__ == "__main__":
    ensure_blender()

    cup = make_cylinder("2cm", "5cm")
    cup.shell("5mm", start_at_location=cup.top_center)
    cup.set_material(aluminum_material())

    cup.export("shelled_cup.stl")
    cup.export("shelled_cup.blend")
    print(f"volume: {cup.get_volume() * 1e9:.0f} mm^3")
    print(f"mass: {cup.get_mass().value * 1000:.1f} g")
