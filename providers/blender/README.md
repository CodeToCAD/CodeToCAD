# CodeToCAD - Blender Provider

This is the CodeToCAD Blender Provider, that allows CodeToCAD to talk to Blender.

## Addon Setup

> Pre-requisites: Blender 3.1 or newer is required.

1. Download a release of the Blender Addon from [CodeToCADBlenderAddon.zip](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/CodeToCADBlenderAddon.zip) or from the latest [release](https://github.com/CodeToCAD/CodeToCAD/releases)
   > Note for developers: instead of downloading a release, you can clone this repository, then import [blender_addon.py](./blender_addon.py) and set to CodeToCAD path in the addon to the root of this repository. Please watch this guide to get set up: [Video Guide](https://youtu.be/YD_4nj0QUJ4)

2. Install the Blender Addon in the blender software

    <img src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/Blender_Install_Addon.gif" width=400 />

3. Import your script using the file menu > import > CodeToCAD or the CodeToCAD menu in the sidebar.

   <img src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/import_file_in_blender.png" width=400 />

> Warning: Since CodeToCAD scripts are written and executed in Python, be careful when running scripts you find on the internet!

> Note, you can also run CodeToCAD in Blender via cli: `blender -- --codetocad $(pwd)/yourScript.py` or `codetocad yourScript.py blender /path/to/blender/executable`

## Sidebar Panel

You can use the side-panel to import CodeToCAD files or start a debugger server.

<img src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/images/blender_panel.png" width=400 />

## Running CodeToCAD

There are two options:

1. Use the File > Import > CodeToCAD menu to import a python file uses the CodeToCAD commands. For example, you could import one of the [test scripts](./tests/text.py).

2. In the console, type `from blender_provider import shape, curve, landmark, scene, analytics, joint`. Now you can use CodeToCAD commands in the console.


## Development

### Dependencies

1. Run `pip install fake-bpy-module-latest` to get intellisense for the Blender API modules.
2. It is recommended to install all the requirements.txt dependencies under [development/requirements.txt](../../development/requirements.txt)
