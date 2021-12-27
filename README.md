# Text Model to 3D Model Automation

## About

Most GUI-based modeling software have an API to interact with the context of the modeling scene. These API's are usually very capable of doing almost everything the user can with the mouse. But what if you didn't have to learn the software's specific API to use it?

What if the multi-line complexity of some common operations are abstracted into one call?

What if you wanted a text-based model that can call the API commands to automatically build your 3D model?

This is what this automation project aims to do!

But it doesn't stop there. By defining joints, materials, properties and landmarks, your model becomes defined beyond the needs of the common modeling software! You can now have one file that is the source of truth for your model, which you can use in simulation or analytics.

It's like OpenSCAD and URDF/SDF rolled into one generic HUMAN-FRIENDLY format! (no seriously, human-readable model formats that are not confusing are a major design point for this project.)

## Purpose

As a model-maker, I would like a text-based model to define all the components of my 3D model, independent of a 3D modeling software or GUI. This text-based model should have the same capabilties of the 3D modeling software's API.

A text-based model should have the capabilities of creating and modifying shapes, reference vertices, edges and faces (aka landmarks), define joints, materials and other properties.

The most important thing in this project is UX. If a high school cannot look at a model file and figure out what it does, then this project is not performing as it should be, design and architecture wise.

This project taks inspiration from the [SDF spec](http://sdformat.org/spec), [Blender's Generate modifiers](https://docs.blender.org/manual/en/dev/modeling/modifiers/introduction.html) and [OpenScad's language reference](https://openscad.org/documentation.html#language-reference)

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

