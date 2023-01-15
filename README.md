# CodeToCAD - Code-based modeling automation

CodeToCAD brings intuitive and reliable code-based automation to your favorite 3D modeling software (e.g. Blender and OnShape). 

Unlike other code-based CAD (e.g. CADQuery and OpenSCAD), CodeToCAD interfaces directly with existing modeling software (like Blender and OnShape). Therefore, you can keep using the software you love, but leverage the power of code and automation in your work. You don't need to be a great programmer to use CodeToCAD - there will be a cheat-sheet and documentation to help you get started.

<div align="center">
<image src="./documentation/three_axis_mill.gif"/>
</div>

## Getting Started

1. Download a release (Check Releases in the repository side-bar) and install the Blender Addon. [Video Guide](https://youtu.be/YD_4nj0QUJ4)
> If you're a developer, instead of downloading a release, you can clone this repository.

2. Join the [Discord Server](https://discord.gg/MnZEtqwt74) to receive updates and help from the community! [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)


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


## Technical Concepts Start Here

### [utilities.py](./utilities.py)

[Utilities.py](./utilities.py) provides common and built-in features of CodeToCAD. This includes Length and Angle parsing from string, and unit conversions.

Python3.8+ is needed to maintain [utilities.py](./utilities.py)

[test_utilities](./tests/test_utilities.py) tests Angle and Length parsing and unit conversions.

### Git Hooks

If you're working on this project, it might be helpful to use git hooks. To install hooks into your dev environment, please run `sh ./development/installGitHooks.sh`

### Running Tests

Run tests using `sh runTests.sh`.

### Capabilities.json and Jinja2 templates

[Capabilities.json](./capabilities.json) defines all the possible functions that can be used to create a model.

Jinja2 files are used to turn the json file into actual code:
- [Python template](./capabilitiesToPython.j2) - Creates the classes and methods templates in python

### Generating Jinja2 templates:

run [capabilitiesToPython.sh](./capabilitiesToPython.sh) to automatically generate [capabilities.py](capabilities.py). This script does the following:

- Create a python virtual environment
- Sources the virtual environment
- Runs `pip install jinja2-cli`
- Runs `jinja2 capabilitiesToPython.j2 capabilities.json --format=json > capabilities.py`

### Capabilities

All capabilities are recorded in [capabilities.json](./capabilities.json). 