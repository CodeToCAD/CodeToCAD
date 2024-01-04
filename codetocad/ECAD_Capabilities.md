## Scope
- two main tasks: 
    - drawing a schematic and 
    - laying out a circuit board
    - generating BOM

## Entities, Relations and Operations
- Library
    - Path management
        - Searching
    - Part library downloading / linking
        - Schematic Symbol
            - Contains Pin
        - PCB Footprint
        - Instantiation
        - Simulation parameters for SPICE
        - Additional fields  (required for BOM)
            - Manufacturer
            - Package type
            - Unit Cost (potentially at scale breaks)
    - Library conversion from KiCAD to SkiDL
- Bus
- Part / Component
    - From Library (i.e. KiCAD's standard component library, )
    - Place, rotate, translate part
    - NOT SCALE: scaling does not apply to electronic components, as different scales of part (i.e. 0204, 0408, 0603, 1206) are actually *different part numbers*
- Board
    - Layers
        - Silkscreen (F.S, B.S)
        - Copper (F.Cu, B.Cu)
    - Vias / Through-holes
        - Non-Plated Through Hole for screw mounts
        - Vias for signal paths
    - Traces / Track
    - Constraints
        - Stackup of Layers
        - Dimensions
        - Tracewidth minimums
        - Trace thicknesses
- Schematic
    - Symbol
    - Pin
    - Connections
    - Net / Netlist: connectivity information about parts and connections 
    - Import / Export Netlist as XML
    - Export as static SVG
    - Export as graphviz
    - Export to editable KiCAD schematic
    - Convert KiCAD schematic to SkiDL
- ERC: Electrical Rules Check
- DRC: Design Rules Check
- Naming and Aliasing
    - Alias: assign descriptive name to part
- Hierarchy
    - SkiDL supports subcircuits, packages and Groups 
        - Decorators: @package, @subcircuit
- KiCAD Geometric Classes
    - [Point2D](https://kicad-python-python.readthedocs.io/en/latest/kicad/util/point.html)
    - [Polygon](https://kicad-python-python.readthedocs.io/en/latest/kicad/primitives/polygon.html) 
        - Union, Intersection, Difference
        - Fracture / Unfracture (merges outline and holes, unmerges)

## Discussion
A much larger part of ECAD design than M-CAD design is the *topology* of circuits. In many cases, the geometric layout is secondary to the topology. A circuit could take many embeddings, or geometric layouts in 2D or even 3D, and so long as the topology is unchanged, the function of the circuit will remain unchanged. This is not the case with mechanical parts like gears, cams, etc, where the function is a direct result of the precise geometry.
Another central task is part selection. Unlike in mechanical design, where functionality is often achieved by fabricating a part, in electronics, parts typically have the desired functionality. Fabricating new parts is typically out of scope for individual, non-specialized companies. Specialized software for VLSI tasks exist, KiCAD is not really the target for it. The main tasks outlined are circuit /schematic definition and PCB layout. Both are typically simple assemblies from parts, with the notable exception of creative inductor / PCB wire coil designs to create PCB-based motors, following the work of Charles Bugeja and then [Chris Greening](https://www.atomic14.com/2022/10/23/scripting-keycad-to-make-coils.html).
Note: Chris Greening (atomic49) actually generated all the geometry for his wedge-shaped coiled PCB motor in a Python Notebook, exported the design as KiCAD-importable JSON. This, rather than developing and working directly in KiCAD's python interpreter, which has limited access to external libraries and was generally annoying to develop for, according to Greening.