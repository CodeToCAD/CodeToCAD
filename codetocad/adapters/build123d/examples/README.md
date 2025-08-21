# CodeToCAD build123d Examples

This directory contains CodeToCAD implementations of all the build123d introductory examples from the [build123d documentation](https://build123d.readthedocs.io/en/latest/introductory_examples.html).

Each example demonstrates how to achieve the same geometric results using CodeToCAD's API instead of direct build123d calls, while maintaining compatibility with the build123d backend.

## Overview

The examples are organized from simple to complex, following the same structure as the original build123d documentation:

### Basic Shape Examples (1-3)
- **Example 1**: Simple Rectangular Plate - Basic box creation
- **Example 2**: Plate with Hole - Boolean operations (difference/subtraction)  
- **Example 3**: An extruded prismatic solid - Sketch extrusion and boolean operations

### Line and Arc Examples (4-6)
- **Example 4**: Building Profiles using lines and arcs - Complex sketch creation
- **Example 5**: Moving the current working point - Positioning shapes at specific locations
- **Example 6**: Using Point Lists - Multiple features at various locations

### Polygon and Polyline Examples (7-8)
- **Example 7**: Polygons - Regular polygon creation and positioning
- **Example 8**: Polylines - Complex profiles using polylines and mirroring

### Advanced Examples (9-36)
Additional examples covering:
- **Example 9**: Selectors, Fillets, and Chamfers - Edge selection and modification (conceptual)
- **Example 23**: Revolve - Revolving 2D profiles around an axis (approximated)
- **Example 34**: Embossed and Debossed Text - Text operations with boolean operations (placeholder geometry)

Additional examples to be implemented:
- Workplane operations
- Loft operations
- Offset and split operations
- Programming patterns (loops, functions)
- Slot operations
- Advanced extrusion techniques

## Key Features

### Original Implementation Comparison
Each example includes:
- `original()` function - Creates the same geometry using direct build123d calls
- `compare_implementations()` function - Compares volume and bounding box between CodeToCAD and original implementations
- Tolerance-based matching to account for different implementation approaches

### CodeToCAD API Patterns
The examples demonstrate:
- **Part Presets**: `Part.preset.cube()`, `Part.preset.cylinder()`, `Part.preset.sphere()`
- **Sketch Operations**: Creating and manipulating 2D sketches
- **Wire Presets**: `sketch.preset.rectangle()`, `sketch.preset.circle()`, `sketch.preset.regular_polygon()`, `sketch.preset.center_arc()`, `sketch.preset.spline()`, `sketch.preset.bezier()`, `sketch.preset.ellipse()`, `sketch.preset.polygon()`, `sketch.preset.triangle()`
- **Boolean Operations**: `part.boolean.union()`, `part.boolean.difference()`, `part.boolean.intersection()`
- **Transformations**: `part.transform.translate()`, `part.transform.rotate()`, `part.transform.scale()`
- **Geometry Queries**: `part.geometry.volume()`, `part.geometry.bounding_box()`

## Running the Examples

### Prerequisites
```bash
# Install CodeToCAD with build123d adapter
pip install build123d

# Ensure you're in the CodeToCAD project directory
cd /path/to/CodeToCAD
```

### Running Individual Examples
```bash
# Run a specific example
python -m codetocad.adapters.build123d.examples.example_01_simple_rectangular_plate
python -m codetocad.adapters.build123d.examples.example_02_plate_with_hole
python -m codetocad.adapters.build123d.examples.example_03_extruded_prismatic_solid
# ... and so on
```

### Example Output
Each example produces output similar to:
```
Example 1: Simple Rectangular Plate
Creating a rectangular plate with CodeToCAD...
Created plate: simple_rectangular_plate
Volume: 48000.00
Bounding box: ((-40.0, -30.0, -5.0), (40.0, 30.0, 5.0))

==================================================
Comparing implementations...
CodeToCAD Volume: 48000.000000
Original Volume: 48000.000000
Volume Match: True
CodeToCAD BBox: ((-40.0, -30.0, -5.0), (40.0, 30.0, 5.0))
Original BBox: ((-40.0, -30.0, -5.0), (40.0, 30.0, 5.0))
BBox Match: True
Implementations match: True
```

## Implementation Notes

### Coordinate System Differences
Some examples may show bounding box differences due to coordinate system variations:
- build123d extrusions typically start from Z=0 and go upward
- CodeToCAD Part presets (like cylinders) are typically centered at the origin
- Volume calculations remain accurate despite positioning differences

### Approximations and Tolerances
- Complex curves and arcs may be approximated with line segments in some cases
- Polygon shapes use native build123d RegularPolygon when available
- Comparison functions use appropriate tolerances to account for implementation differences

### Missing Features
Some advanced build123d features may not have direct CodeToCAD equivalents yet:
- Advanced workplane operations
- Complex mirroring within sketches
- Specialized hole operations (CounterBore, CounterSink)
- Advanced sweep and loft operations

These are implemented using alternative approaches that achieve similar geometric results.

## File Structure

```
examples/
├── README.md                                          # This file
├── example_01_simple_rectangular_plate.py            # Basic box creation
├── example_02_plate_with_hole.py                     # Boolean operations
├── example_03_extruded_prismatic_solid.py           # Sketch extrusion
├── example_04_building_profiles_lines_arcs.py       # Complex sketches
├── example_05_moving_current_working_point.py       # Positioning
├── example_06_using_point_lists.py                  # Multiple features
├── example_07_polygons.py                           # Regular polygons
├── example_08_polylines.py                          # Polyline profiles
├── example_09_selectors_fillets_chamfers.py        # Edge operations (conceptual)
├── example_23_revolve.py                           # Revolve operations (approximated)
├── example_34_embossed_debossed_text.py           # Text operations (placeholder)
└── [additional examples...]                         # More advanced examples (to be implemented)
```

## Contributing

When adding new examples:
1. Follow the established naming convention: `example_XX_descriptive_name.py`
2. Include the original build123d code in the docstring
3. Implement both `original()` and CodeToCAD versions
4. Add comparison functionality with appropriate tolerances
5. Update this README with the new example description

## Support

For issues with specific examples or CodeToCAD functionality:
1. Check that build123d is properly installed
2. Verify you're running from the correct directory
3. Review the comparison output to understand any differences
4. Consult the main CodeToCAD documentation for API details
