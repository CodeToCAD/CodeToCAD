# CodeToCAD - Blender Provider

This is the CodeToCAD Blender Provider, that allows CodeToCAD to talk to Blender.

## Setup

The easiest way to use this BlenderProvider is to enable the addon in Blender:

1. In Blender, go to Edit -> Preferences -> Add-ons. 
2. Click Install. Select the [CodeToCADBlenderAddon.py](./CodeToCADBlenderAddon.py) file.
3. Enable the addon in blender by clicking on the checkmark.
4. Expand the arrow next to the CodeToCAD addon, this will open up the preferences.
5. Select the BlenderProvider folder, which is the root of this repo.
6. Click the "Refresh BlenderProvider" button

## Running CodeToCAD

There are two options:

1. Use the File > Import > CodeToCAD menu to import a python file uses the CodeToCAD commands. For example, you could import one of the [test scripts](./tests/text.py).

2. In the console, type `from BlenderProvider import shape, curve, landmark, scene, analytics, joint`. Now you can use CodeToCAD commands in the console.


## Development

### Dependencies

1. Run `pip install fake-bpy-module-latest` to get intellisense for the Blender API modules
