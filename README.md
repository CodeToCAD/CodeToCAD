# CodeToCAD - Blender Provider

This is the CodeToCAD Blender Provider repo, that allows CodeToCAD to talk to Blender.

Please refer to the [CodeToCAD repo](https://github.com/CodeToCad/CodeToCAD) for more information about this CodeToCAD.

## Cloning

This repository contains a submodule. Clone it using `git clone --recurse-submodules -j8 git@github.com:CodeToCad/CodeToCad-Blender.git`

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

2. In the console, type `from CodeToCADBlenderProvider import shape, curve, landmark, scene, analytics, joint`. Now you can use CodeToCAD commands in the console.