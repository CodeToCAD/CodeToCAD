<div align="center">
    <a href="https://pypi.org/project/codetocad/0.2.1688153771/">
        <img src="https://i.gyazo.com/c1a94076208b7b23010b00381a5b2b9e.png" width="256" height="256" alt="New Expensify Icon">
    </a>
    <h1></h1>
    <p><strong>One language for all your CAD needs</p>
</div>
<p align="center">
   <a href="https://codetocad.github.io/CodeToCAD/docs.html"><img src="https://img.shields.io/badge/Read_the_docs-white?logo=readthedocs&logoColor=black
   "/></a>
   <a href="https://discord.gg/MnZEtqwt74"><img alt="Discord" src="https://img.shields.io/discord/955573351806562335?logo=discord&logoColor=black&label=Discord&labelColor=white&color=blue"></a>
   <a href="https://github.com/CodeToCAD/CodeToCAD/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/CodeToCAD/CodeToCAD"/></a>
   <a href="https://github.com/search?q=repo%3ACodeToCAD%2FCodeToCAD++language%3APython&type=code"><img alt="GitHub top language" src="https://img.shields.io/github/languages/top/CodeToCAD/CodeToCAD?logo=python&labelColor=white&color=blue"></a>
   <a href="https://codetocad.github.io/CodeToCAD/examples.html"><img alt="Static Badge" src="https://img.shields.io/badge/Examples-white?logo=internetarchive&logoColor=black"></a>
</p>

## Table of Contents

Use one python script to interact with all these software:
1. [Getting Started](#getting-started)
2. [Supported Applications](#supported-applications)


## Getting started

> Pre-requisites: Python 3.10 or newer.

1. Install the [CodeToCAD PIP Package](https://pypi.org/project/CodeToCAD/) to get intellisense syntax highlighting.

   ```
   pip install CodeToCAD
   ```

2. Create your own CodeToCAD python file and save it:

   ```python
   # my_codetocad_script.py
   # More examples can be found under CodeToCAD/examples/
   from codetocad import *

   my_material = Material("material").set_color(169, 76, 181, 0.8)
   Part("Cube").create_cube(1, 1, 1).set_material(my_material)
   ```

3. Watch as your code gets seemlessly translated into CAD

![Material Cube](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/material_cube.png)

Above is the above script being run in blender using our [Blender Addon](#blender) below.


## Supported applications
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

## BLENDER

> Pre-requisites: Blender 3.1 or newer is required.

1. Download a release and install the Blender Addon from [CodeToCADBlenderAddon.zip](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/CodeToCADBlenderAddon.zip) or from the latest Release (see the sidebar).

   > If you're a developer, instead of downloading a release, you can clone this repository. [Video Guide](https://youtu.be/YD_4nj0QUJ4)

2. Import your script using the file menu > import > CodeToCAD or the CodeToCAD menu in the sidebar.
   ![import_file](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/import_file_in_blender.png)

> Note, you can also run CodeToCAD in Blender via cli: `blender -- --codetocad $(pwd)/yourScript.py`

## WHAT DO I DO NEXT?

- Run or browse the [examples](./examples/)!

  ![Stacked Cubes](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/stacked_cubes.png)

- Join the [Discord Server](https://discord.gg/MnZEtqwt74) to receive updates and help from the community! [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)


### WARNING!

Since CodeToCAD scripts are written and executed in Python, be careful when running scripts you find on the internet!

## THE POWER OF CODE-BASED CAD


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
