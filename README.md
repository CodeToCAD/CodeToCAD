# Model to Model

As a model-maker, I would like a text-based model to define all the components of my 3D model, independent of a 3D modeling software or GUI. This text-based model should allow for both solid and surface modeling, and offer the same capabilties of the 3D modeling software.

A text-based model should have the capabilities of adding meshes to a Source, modify meshes, reference vertecies, edges and faces as landmarks, and define joints between Features.

## Example

### Chess Rook

```
# Features
Feature(name: "Battlement").
 define("height", "1.5cm", "outerDiameter", "1cm", "innerDiameter", "0.5cm", "bottomThickness", "0.3cm").
 source(type: SourceTypes.primitive, source: "cylinder", dimensions: (outerDiameter, height, outerDiameter) ).
 subtract ( 

    source(type: SourceTypes.primitive, source: "cylinder", dimensions: (innerDiameter, height - bottomThickness, innerDiameter) ).
    translate(0,bottomThickness,0)

 ).
 subtract (

    source(type: SourceTypes.primitive, source: "cylinder", dimensions: (innerDiameter, height - 0.5cm, innerDiameter) ).
    pattern(type: circular, radius: innerDiameter, instances: 6, separation: 0d, theta: 0d)

 ).
 landmark(name: "bottom_center", (Landmarks.center, Landmarks.min, Landmarks.center) )


Joint(source1: "Battlement", source2: "Tower", source1Landmark: "bottom_center", source2Landmark: "top_center", initialRotation: (0,0,0), limitRotation: (0,0,0), limitTranslation: (0,0,0))


# Sources
Name, Source, Initial Dimensions (x,y,z), *Description

Battlement, cylinder, (1cm, 1.5cm, 1cm)
Tower, cylinder, (1cm, 5cm, 1cm)
Base, cylinder, (1cm, 5mm, 1cm)

# Support Sources

# Joints
Source 1 Name, Source 2 Name, Landmark 1, Landmark 2, Joint Type, initial rotation (x,y,z), *limit rotation (default=0,0,0)

Base, Tower, top_center, bottom_center, fixed, (0d,0d,0d)
Tower, Battlement, top_center, bottom_center, fixed, (0d,0d,0d)


# Landmarks
Source Name, Landmark Name, Location (x,y,z), *Type (default=vertex), *Options

Battlement, bottom_center, (center,min,center)
Tower, top_center, (center,max,center)
Tower, bottom_center, (center,min,center)
Base, top_center, (center,max,center)

# Modification

Source Name, Modification type, Parameters...

```

## Features

A Feature is an entity that has a name and at least 1 mesh

## Adding meshes to a Feature

A mesh should have a name, initial dimensions and a source

### Source

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

