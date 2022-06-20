# CodeToCAD

CodeToCAD is an automation tool to allow you to write code to define and create 3D models.

CodeToCAD is not a 3D modeling engine, it is an interface to define shapes and curves to build meshes. We leave the 3D engine haul to the software that is good at them.

Current integrations:
- [CodeToCAD-Blender](https://github.com/CodeToCad/CodeToCad-Blender)

Future planned integrations:
- OnShape
- OpenSCAD
- ThreeJS

## Why does CodeToCAD matter?

### Purpose tl;dr

- Allow the user to define shapes and curves to build 3D models using a common programming language.
  - The user can then transform their shapes and curves into a 3D modeling software of their choice, using a translation tool.
    - This assumes that the "translation tool" (aka the Provider) has been built to support that 3D modeling software.

### Side Goals:

- The CodeToCAD interface should be "in English".
  - Meaning that a layman can look at it and understand how the model is built with only the knowledge of programming, and without knowledge of the underlying 3D modeling software.

- Provide automations or pre-built models for commonly used modeling techniques.

### Why CodeToCAD?

Why do we need CodeToCAD? Because engineers and digital artists currently have
limited options to create 3D models. They could either:

1. Use vendor-locked software (e.g. Fusion360, AutoCAD, SolidWorks, OnShape,
Blender) that offer a Point-and-Click-and-Drag UI software that is slow and
complicated to work with.

2. Resort to complicated scripting and modeling-specific programming
languages and libraries like OpenSCAD and QueryCAD or the API's for
Blender, Fusion360 etc.. that are not very user friendly.

In either case, the models they create can only be used on the software they
used to create them on, and they have to do most of the model building from scratch.

Moreover, keeping a linear version history of their work is nigh impossible, and
making updates to their models is an absolute nightmare.

Cue CodeToCAD, where we provide one modeling technique to rule
them all!

### Why not just use the API's of the 3D Software?

Most GUI-based modeling software have an API to interact with the context of the modeling scene. These API's are usually very capable of doing almost everything the user can with the mouse. But what if you didn't have to learn the software's specific API to use it?

What if the multi-line complexity of some common operations are abstracted into one call?

What if you wanted a text-based model that can call the API commands to automatically build your 3D model?

This is what this automation project aims to do!

But it doesn't stop there. By defining joints, materials, properties and landmarks, your model becomes defined beyond the needs of the common modeling software! You can now have one file that is the source of truth for your model, which you can use in simulation or analytics.

It's like OpenSCAD and URDF/SDF rolled into one generic HUMAN-FRIENDLY format! (no seriously, human-readable model formats that are not confusing are a major design point for this project.)

### Purpose - long version

As a model-maker, I would like a text-based model to define all the components of my 3D model, independent of a 3D modeling software or GUI. This text-based model should have the same capabilties of the 3D modeling software's API.

A text-based model should have the capabilities of creating and modifying shapes, reference vertices, edges and faces (aka landmarks), define joints, materials and other properties.

One of the most important things in this project is UX. If a layman looks at a model file and cannot figure out what it does, then this project is not performing as it should be - design and architecture wise.

This project takes inspiration from the [SDF spec](http://sdformat.org/spec), [Blender's Generate modifiers](https://docs.blender.org/manual/en/dev/modeling/modifiers/introduction.html) and [OpenScad's language reference](https://openscad.org/documentation.html#language-reference)

## Technical Concepts Start Here

### Capabilities.json and Jinja2 templates

[Capabilities.json](./capabilities.json) defines all the possible functions that can be used to create a model.

Jinja2 files are used to turn the json file into actual code:
- [Python template](./capabilitiesToPython.j2) - Creates the classes and methods templates in python

### Generating Jinja2 templates:

Currently using (https://j2live.ttl255.com/)[https://j2live.ttl255.com/] to generate the template. If merging it into an existing file, KDiff3 is used to resolve the merge process.

## Capabilities

All capabilities are recorded in [capabilities.json](./capabilities.json). The lists below may be outdated.

Basic capabilities are separated into:

- Shapes
- Landmarks
- Joints
- Materials
- Scene
- Analytics

### Shapes

A source can be:
- a primitive shape (e.g. cube, sphere, cone, cylinder)
- a reference to a mesh file
- a reference image
- text
- verticies
- paths

## Source Modification

Mesh modification should be able to do the following operations:
- Boolean
  - addition
  - subtraction
  - union
- Pattern
  - linear
  - circular
  - contour
- Mirror
- Bevel
- Subdivision of surface
- Remesh

> For reference, [Blender's Generate modifiers](https://docs.blender.org/manual/en/dev/modeling/modifiers/introduction.html) are some of the modifiers that should be supported.

