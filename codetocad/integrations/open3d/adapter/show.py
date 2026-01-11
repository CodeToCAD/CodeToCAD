from platform import system
from codetocad.cli.config import get_temp_stl_export_path
from codetocad.core.cad.shape import Shape
from codetocad.core.cad.vertex_edge_solid import Solid
import open3d as o3d

if system() != "Darwin":
    from open3d.web_visualizer import draw
else:
    # The web visualizer is not available on macOS.
    from open3d.visualization import draw


def show_in_open3d(shape: Solid):
    """Export and visualize a shape."""
    Shape.export_file(shape, str(get_temp_stl_export_path()))
    
    mesh = o3d.io.read_triangle_mesh(str(get_temp_stl_export_path()))

    mesh.paint_uniform_color([0.5, 0.5, 0.5])  # Gray color
    
    draw(mesh)