# CodeToCAD - Code-based modeling automation

CodeToCAD brings intuitive and reliable code-based automation to your favorite 3D modeling software (e.g. Blender and OnShape). 

Unlike other code-based CAD (e.g. CADQuery and OpenSCAD), CodeToCAD interfaces directly with existing modeling software (like Blender and OnShape). Therefore, you can keep using the software you love, but leverage the power of code and automation in your work. You don't need to be a great programmer to use CodeToCAD - there will be a cheat-sheet and documentation to help you get started.

<div align="center">
<image src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/documentation/three_axis_mill.gif"/>
</div>

## Getting Started

[![Release Version and Blender Addon](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/on-pr-resolved.yml/badge.svg?branch=develop)](https://github.com/CodeToCAD/CodeToCAD/actions/workflows/on-pr-resolved.yml)

> Pre-requisites: Python 3.10 or newer. 

1. Install the [CodeToCAD PIP Package](https://pypi.org/project/CodeToCAD/) to get intellisense syntax highlighting.

    `pip install CodeToCAD`

2. Create your own CodeToCAD python file and save it:
    ```python
    # myCodeToCAD.py
    # This is also the examples/materials.py example
    from CodeToCAD import *

    myMaterial = Material("material").setColor(169, 76, 181, 0.8)
    Part("Cube").createCube(1, 1, 1).setMaterial(myMaterial)
    ```

    ![Material Cube](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/documentation/materialCube.png)

3. Run your script in your modeling software. If you are using Blender, check out the instructions for installing the [Blender Addon](#blender) addon below.

### Blender

> Note: Blender 3.1 or newer is required.

1. Download a release and install the Blender Addon from [CodeToCADBlenderAddon.zip](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/CodeToCADBlenderAddon.zip) or from the latest Release (see the sidebar).
    > If you're a developer, instead of downloading a release, you can clone this repository. [Video Guide](https://youtu.be/YD_4nj0QUJ4)

2. Import your script using the file menu > import > CodeToCAD or the CodeToCAD menu in the sidebar.
    ![import_file](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/documentation/import_file_in_blender.png)

## What do I do next?

- Run or browse the [examples](./examples/)! 

    ![Stacked Cubes](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/documentation/stackedCubes.png)

- Join the [Discord Server](https://discord.gg/MnZEtqwt74) to receive updates and help from the community! [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)


## Integrations

Current integrations:
- [CodeToCAD-Blender](https://github.com/CodeToCad/CodeToCad-Blender)

Future planned integrations:
- OnShape
- ThreeJS
- Electronic CAD (suggestions welcome)


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
`sh development/createPythonVirtualEnvironment.sh` 
or 
`sh development/createPythonVirtualEnvironment.sh /path/to/python_binary`.

> If you are on Windows, please use Git Bash.
> Note: Python 3.10+ is required.
> Note 2: It might be a good idea to restart VSCode after installing the virtual environment. 
> Note 3: If VSCode prompts you, please use the interpreter under `development/developmentVirtualEnvironment`.

2. It's good practice to run tests before committing. Please run `sh ./development/installGitHooks.sh` to instll Git Hooks.

3. Install Blender 3.1+, this is the first Blender version with Python 3.10.

4. Install the Blender Addon at [providers/blender/CodeToCADBlenderAddon.py](./providers/blender/CodeToCADBlenderAddon.py) [Video Guide](https://youtu.be/YD_4nj0QUJ4)


### Running Tests

Run tests using `sh runTests.sh`.

### Capabilities.json and Jinja2 templates

[CodeToCAD/capabilities.json](./CodeToCAD/capabilities.json) is a schema used to generate the [CodeToCAD interface](./CodeToCAD/CodeToCADInterface.py).

Jinja2 templates are used to turn capabilities.json into an interface, as well as templates for CodeToCAD Providers and Tests.

You can generate the Jinja2 templates by running the "Capabilities.json to Python" task in VSCode, or `sh development/capabilitiesJsonToPython/capabilitiesToPy.sh`

### Contributing

If you would like to contribute to the project, please feel free to submit a PR. 

Please join the Discord Server if you have any questions or suggestions: [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)
