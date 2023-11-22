# CodeToCAD - One language for all your CAD needs.

Use one python script to interact with all these software:

- [Blender](https://www.blender.org/)* - Digital Modeling Software
- [Onshape](https://www.onshape.com/en/)** - Product Development and CAD Software
- [PyBuller](https://pybullet.org/)*** - Real-time Physics Simulation Library
- [KiCAD](https://www.kicad.org/)*** - Electronic/PCB Design Software
- [FreeCAD](https://www.freecad.org/)*** - CAD Software
- [ThreeJS](https://threejs.org/)*** - Web-based 3D Library
- [Libfive](https://libfive.com/)*** Signed Distance Field Modeling library

<sub>* Alpha/Beta support
** Pre-alpha development.
*** To be developed.</sub>

CodeToCAD brings intuitive and reliable code-based modeling automation to your favorite 3D modeling software.

[READ THE DOCS](https://codetocad.github.io/CodeToCAD/docs.html) will help you get started.

## Mesh or B-Rep geometry?

Neither! CodeToCAD uses common surface topologies to define shapes. There are case-specific methods that might only make sense to use if you're modeling in a mesh-based software. The outcome of your model depends on the software you're doing the modeling in.

<div align="center">
<image src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/three_axis_mill.gif"/>
</div>

## Documentation

You can find the CodeToCAD documentation here: [https://codetocad.github.io/CodeToCAD/docs.html](https://codetocad.github.io/CodeToCAD/docs.html).

You should browse the examples too! [https://codetocad.github.io/CodeToCAD/examples.html](https://codetocad.github.io/CodeToCAD/examples.html).

## Getting Started

[![Release Version and Blender Addon](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/on-pr-resolved.yml/badge.svg?branch=develop)](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/on-pr-resolved.yml) [![Documentation Pages](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/pages/pages-build-deployment)

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

### Blender

> Note: Blender 3.1 or newer is required.

1. Download a release and install the Blender Addon from [CodeToCADBlenderAddon.zip](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/CodeToCADBlenderAddon.zip) or from the latest Release (see the sidebar).

   > If you're a developer, instead of downloading a release, you can clone this repository. [Video Guide](https://youtu.be/YD_4nj0QUJ4)

2. Import your script using the file menu > import > CodeToCAD or the CodeToCAD menu in the sidebar.
   ![import_file](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/import_file_in_blender.png)

> Note, you can also run CodeToCAD in Blender via cli: `blender -- --codetocad $(pwd)/yourScript.py`

## What do I do next?

- Run or browse the [examples](./examples/)!

  ![Stacked Cubes](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/stacked_cubes.png)

- Join the [Discord Server](https://discord.gg/MnZEtqwt74) to receive updates and help from the community! [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)

## Integrations

Current integrations:

- [CodeToCAD-Blender](#blender)
- Onshape (Work-in-progress)

Future planned integrations (not in any order):

- KiCAD
- FreeCAD
- ThreeJS
- Libfive (SDF library)

## Warning

Since CodeToCAD scripts are written and executed in Python, be careful when running scripts you find on the internet!

## Benefits of code-based modeling with CodeToCAD:

✅ Simplified modeling interface - it's all text! No more scrolling and clicking into sub-menus to edit your models.

🔓 Not vendor locked - your models are created in an open-source language. If you want to use another software, you do not lose the features you have defined. Note: There is no guarantee that a model created for, e.g. Blender, will work right away for another software, but with some refactoring, it theoretically should!

🪶 Lightweight and portable. All you need is a text-editor to model. You can occasionally fire-up your modeling software to run your creations.

💪 Leverages existing programming languages, like Python. You can keep using the languages you're familiar with and love. There is no one-off language you and your team has to learn. Use CodeToCAD like a library or a framework.

🚦Easy version control. Your models are written in code, you can use industry-loved git to keep track of versions of your models.

💕 Built by people who believe in automation and that modeling workflows should be intuitive, reliable and most importantly free and open source!

## Development & Contributing

### Setting up development environment.

1. Please install the VSCode python virtual environment using
   `sh development/create_python_virtual_environment.sh`
   or
   `sh development/create_python_virtual_environment.sh /path/to/python_binary`.

> If you are on Windows, please use Git Bash.
> Note: Python 3.10+ is required.
> Note 2: It might be a good idea to restart VSCode after installing the virtual environment.
> Note 3: If VSCode prompts you, please use the interpreter under `development/developmentVirtualEnvironment`.

2. It's good practice to run tests before committing. Please run `sh ./development/install_git_hooks.sh` to instll Git Hooks.

3. Install Blender 3.1+, this is the first Blender version with Python 3.10.

4. Install the Blender Addon at [providers/blender/CodeToCADBlenderAddon.py](./providers/blender/CodeToCADBlenderAddon.py) [Video Guide](https://youtu.be/YD_4nj0QUJ4)

### Running Tests

Run tests using `sh run_tests.sh`.

### Capabilities.json and Jinja2 templates

[CodeToCAD/capabilities.json](./CodeToCAD/capabilities.json) is a schema used to generate the [CodeToCAD interfaces](./CodeToCAD/interfaces/).

Jinja2 templates are used to turn capabilities.json into an interface, as well as templates for CodeToCAD Providers and Tests.

You can generate the Jinja2 templates by running the "Capabilities.json to Python" task in VSCode, or `sh development/capabilities_json_to_python/capabilities_to_py.sh`

### Architecture

CodeToCAD is an automation. Here is the high-level architecture for this tool.

![Architecture](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/CodeToCAD%20architecture%20overview.drawio.png)

### Contributing

If you would like to contribute to the project, please feel free to submit a PR.

Please join the Discord Server if you have any questions or suggestions: [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)
