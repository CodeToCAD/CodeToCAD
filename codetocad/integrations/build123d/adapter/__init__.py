# Modular action functions for build123d API calls

# Export functions
from codetocad.integrations.build123d.adapter.export import (
    export_step,
    export_stl,
    export_obj,
    export_brep,
    import_step,
    import_stl,
    import_brep,
)

# Geometry functions
from codetocad.integrations.build123d.adapter.geometry import (
    create_vertex,
    create_edge_from_vertices,
    create_line_edge,
    create_arc_edge,
    create_center_arc_edge,
    create_wire_from_edges,
    create_rectangle_wire,
    create_circle_wire,
    create_regular_polygon_wire,
    create_polyline_wire,
    create_center_arc_wire,
    create_three_point_arc_wire,
    create_radius_arc_wire,
    create_tangent_arc_wire,
    create_spline_wire,
    create_bezier_wire,
    create_polar_line_wire,
    create_fillet_polyline_wire,
    create_ellipse_wire,
    create_polygon_wire,
    create_rectangle_rounded_wire,
    create_triangle_wire,
    create_trapezoid_wire,
    create_text_wire,
    create_face_from_wire,
    create_face_with_holes,
    extrude_face,
    create_cube,
    create_cylinder,
    create_sphere,
    boolean_union,
    boolean_difference,
    boolean_intersection,
)

# Solid operations
from codetocad.integrations.build123d.adapter.solid_operations import (
    extrude_wire,
    revolve_wire,
    loft_wires,
    sweep_wire,
    fillet_edges,
    chamfer_edges,
    mirror_solid,
    pattern_linear,
    pattern_polar,
    create_torus,
    create_cone,
)

# Sketch operations
from codetocad.integrations.build123d.adapter.sketch_operations import (
    create_sketch_context,
    create_line_context,
    add_line_to_sketch,
    add_rectangle_to_sketch,
    add_circle_to_sketch,
    add_arc_to_sketch,
    add_spline_to_sketch,
    close_wire_in_sketch,
    get_sketch_wires,
    get_sketch_faces,
    make_face_from_sketch,
    extrude_sketch,
    revolve_sketch,
)

# Transformation functions
from codetocad.integrations.build123d.adapter.transformations import (
    translate_object,
    rotate_object,
    scale_object,
    mirror_object,
    get_bounding_box,
    get_center_of_mass,
    get_volume,
    get_area,
    get_length,
)

# Constraint functions
from codetocad.integrations.build123d.adapter.constraints import (
    get_axis_vector,
    fix_at_location,
    make_tangent,
    make_parallel,
    make_perpendicular,
    create_revolute_joint_location,
    create_prismatic_joint_location,
)
