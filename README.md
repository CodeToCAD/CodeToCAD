# CodeToCAD

## ONE LANGUAGE FOR ALL YOUR CAD NEEDS

Use one python script to interact with all these software:

- [Blender](https://www.blender.org/)* - Digital Modeling Software
- [Onshape](https://www.onshape.com/en/)** - Product Development and CAD Software
- [PyBullet](https://pybullet.org/)*** - Real-time Physics Simulation Library
- [KiCAD](https://www.kicad.org/)*** - Electronic/PCB Design Software
- LLM/AI based model generation ***
- [FreeCAD](https://www.freecad.org/)*** - CAD Software
- [ThreeJS](https://threejs.org/)*** - Web-based 3D Library
- [Libfive](https://libfive.com/)*** Signed Distance Field Modeling library

<sub>* Alpha/Beta support
** Pre-alpha development.
*** To be developed.</sub>


#### [READ THE DOCS](https://codetocad.github.io/CodeToCAD/docs.html)

#### [EXAMPLES WITH CODE](https://codetocad.github.io/CodeToCAD/examples.html)


## SIMPLIFY YOUR CAD WORKFLOW NOW:

> Pre-requisites: Python 3.10 or newer.

1. Install the [CodeToCAD PIP Package](https://pypi.org/project/CodeToCAD/) to get intellisense syntax highlighting.

   `pip install CodeToCAD`

2. Create your own CodeToCAD python file and save it:

   ```python
   # my_codetocad_script.py
   # This is also the examples/materials.py example
   from codetocad import *

   my_material = Material("material").set_color(169, 76, 181, 0.8)
   Part("Cube").create_cube(1, 1, 1).set_material(my_material)
   ```

   ![Material Cube](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/material_cube.png)

3. Run your script in your modeling software. If you are using Blender, check out the instructions for installing the [Blender Addon](#blender) addon below.


[![Release Version and Blender Addon](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/on-pr-resolved.yml/badge.svg?branch=develop)](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/on-pr-resolved.yml) [![Documentation Pages](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/pages/pages-build-deployment)


### BLENDER

> Note: Blender 3.1 or newer is required.

1. Download a release and install the Blender Addon from [CodeToCADBlenderAddon.zip](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/CodeToCADBlenderAddon.zip) or from the latest Release (see the sidebar).

   > If you're a developer, instead of downloading a release, you can clone this repository. [Video Guide](https://youtu.be/YD_4nj0QUJ4)

2. Import your script using the file menu > import > CodeToCAD or the CodeToCAD menu in the sidebar.
   ![import_file](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/import_file_in_blender.png)

> Note, you can also run CodeToCAD in Blender via cli: `blender -- --codetocad $(pwd)/yourScript.py`

## WHAT DO I DO NEXT?

- Run or browse the [examples](./examples/)!

  ![Stacked Cubes](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/stacked_cubes.png)

- Join the [Discord Server](https://discord.gg/MnZEtqwt74) to receive updates and help from the community! [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)


## WARNING!

Since CodeToCAD scripts are written and executed in Python, be careful when running scripts you find on the internet!

## STILL HAVE DOUBTS?


<div align="center">
<image src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/three_axis_mill.gif"/>
</div>


Benefits of code-based modeling with CodeToCAD:

✅ Simplified modeling interface - it's all text! No more scrolling and clicking into sub-menus to edit your models.

🔓 Not vendor locked - your models are created in an open-source language. If you want to use another software, you do not lose the features you have defined. Note: There is no guarantee that a model created for, e.g. Blender, will work right away for another software, but with some refactoring, it theoretically should!

🪶 Lightweight and portable. All you need is a text-editor to model. You can occasionally fire-up your modeling software to run your creations.

💪 Leverages existing programming languages, like Python. You can keep using the languages you're familiar with and love. There is no one-off language you and your team has to learn. Use CodeToCAD like a library or a framework.

🚦Easy version control. Your models are written in code, you can use industry-loved git to keep track of versions of your models.

💕 Built by people who believe in automation and that modeling workflows should be intuitive, reliable and most importantly free and open source!
