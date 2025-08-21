"""
MuJoCo simulation export implementation.
"""

import json
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from codetocad.interfaces.simulation.simulation_export_interface import (
    SimulationExportInterface,
)


class MuJoCoSimulationExport(SimulationExportInterface):
    """MuJoCo implementation of simulation export functionality."""

    def urdf(
        self,
        filename: str,
        include_visuals: bool = True,
        include_collisions: bool = True,
        include_inertials: bool = True,
        **kwargs,
    ) -> str:
        """Export simulation to URDF format."""
        urdf_content = '<?xml version="1.0"?>\n'
        urdf_content += f'<robot name="{self.simulation.name or "robot"}">\n'

        # Export each body as a link
        for i, body in enumerate(self.simulation.bodies):
            link_name = body.name or f"link_{i}"
            urdf_content += f'  <link name="{link_name}">\n'

            if include_visuals:
                urdf_content += "    <visual>\n"
                urdf_content += "      <geometry>\n"
                urdf_content += '        <box size="1 1 1"/>\n'
                urdf_content += "      </geometry>\n"
                urdf_content += '      <material name="default">\n'
                urdf_content += '        <color rgba="0.8 0.8 0.8 1.0"/>\n'
                urdf_content += "      </material>\n"
                urdf_content += "    </visual>\n"

            if include_collisions:
                urdf_content += "    <collision>\n"
                urdf_content += "      <geometry>\n"
                urdf_content += '        <box size="1 1 1"/>\n'
                urdf_content += "      </geometry>\n"
                urdf_content += "    </collision>\n"

            if include_inertials:
                mass = body.get_mass() if hasattr(body, "get_mass") else 1.0
                urdf_content += "    <inertial>\n"
                urdf_content += f'      <mass value="{mass}"/>\n'
                urdf_content += f'      <inertia ixx="{mass}" ixy="0" ixz="0" iyy="{mass}" iyz="0" izz="{mass}"/>\n'
                urdf_content += "    </inertial>\n"

            urdf_content += "  </link>\n"

        urdf_content += "</robot>\n"

        with open(filename, "w") as f:
            f.write(urdf_content)

        return filename

    def sdf(
        self,
        filename: str,
        version: str = "1.7",
        include_physics: bool = True,
        **kwargs,
    ) -> str:
        """Export simulation to SDF format."""
        sdf_content = f'<?xml version="1.0"?>\n'
        sdf_content += f'<sdf version="{version}">\n'
        sdf_content += f'  <world name="{self.simulation.name or "world"}">\n'

        if include_physics:
            sdf_content += '    <physics type="ode">\n'
            sdf_content += (
                f"      <max_step_size>{self.simulation.time_step}</max_step_size>\n"
            )
            sdf_content += "      <real_time_factor>1</real_time_factor>\n"
            sdf_content += "    </physics>\n"

            gravity = self.simulation.gravity
            sdf_content += (
                f"    <gravity>{gravity.x} {gravity.y} {gravity.z}</gravity>\n"
            )

        # Add bodies as models
        for i, body in enumerate(self.simulation.bodies):
            model_name = body.name or f"model_{i}"
            sdf_content += f'    <model name="{model_name}">\n'
            sdf_content += '      <link name="link">\n'

            mass = body.get_mass() if hasattr(body, "get_mass") else 1.0
            sdf_content += "        <inertial>\n"
            sdf_content += f"          <mass>{mass}</mass>\n"
            sdf_content += "        </inertial>\n"

            sdf_content += '        <collision name="collision">\n'
            sdf_content += "          <geometry>\n"
            sdf_content += "            <box><size>1 1 1</size></box>\n"
            sdf_content += "          </geometry>\n"
            sdf_content += "        </collision>\n"

            sdf_content += '        <visual name="visual">\n'
            sdf_content += "          <geometry>\n"
            sdf_content += "            <box><size>1 1 1</size></box>\n"
            sdf_content += "          </geometry>\n"
            sdf_content += "        </visual>\n"

            sdf_content += "      </link>\n"
            sdf_content += "    </model>\n"

        sdf_content += "  </world>\n"
        sdf_content += "</sdf>\n"

        with open(filename, "w") as f:
            f.write(sdf_content)

        return filename

    def mjcf(self, filename: str, **kwargs) -> str:
        """Export to MuJoCo MJCF XML format with full material and mesh support."""
        # Create MJCF package directory structure
        mjcf_path = Path(filename)
        package_dir = mjcf_path.parent / mjcf_path.stem
        meshes_dir = package_dir / "meshes"
        textures_dir = package_dir / "textures"

        # Create directories
        package_dir.mkdir(parents=True, exist_ok=True)
        meshes_dir.mkdir(exist_ok=True)
        textures_dir.mkdir(exist_ok=True)

        xml_content = '<mujoco model="codetocad_mujoco_export">\n'
        xml_content += (
            '  <compiler angle="radian" meshdir="meshes" texturedir="textures"/>\n'
        )
        xml_content += (
            f'  <option timestep="{getattr(self.simulation, "time_step", 0.002)}"/>\n'
        )

        # Assets section for materials and textures
        xml_content += "  <asset>\n"

        # Export materials and textures
        material_definitions = {}
        for i, body in enumerate(self.simulation.bodies):
            # Export mesh
            mesh_info = self._export_body_mesh(body, meshes_dir, i)
            if mesh_info:
                mesh_name = f"mesh_{i}"
                xml_content += (
                    f'    <mesh name="{mesh_name}" file="{mesh_info["filename"]}"/>\n'
                )

            # Export textures and create material
            texture_info = self._export_body_textures(body, textures_dir, i)
            material_name, color_rgba = self._get_material_properties(body)

            if material_name not in material_definitions:
                material_definitions[material_name] = {
                    "color": color_rgba,
                    "textures": texture_info,
                }

                # Add texture definitions
                if texture_info and texture_info.get("diffuse"):
                    texture_name = f"tex_{material_name}"
                    xml_content += f'    <texture name="{texture_name}" type="2d" file="{texture_info["diffuse"]}"/>\n'
                    xml_content += f'    <material name="{material_name}" texture="{texture_name}"/>\n'
                else:
                    # Material with just color
                    r, g, b, a = [float(x) for x in color_rgba.split()]
                    xml_content += f'    <material name="{material_name}" rgba="{r} {g} {b} {a}"/>\n'

        xml_content += "  </asset>\n"

        # Worldbody section
        xml_content += "  <worldbody>\n"
        xml_content += '    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>\n'
        xml_content += '    <geom name="floor" pos="0 0 -0.1" size="5 5 0.1" type="plane" rgba="0.8 0.9 0.8 1"/>\n'

        for i, body in enumerate(self.simulation.bodies):
            body_name = body.name or f"body_{i}"
            mass = body.get_mass() if hasattr(body, "get_mass") else 1.0
            material_name, _ = self._get_material_properties(body)

            xml_content += f'    <body name="{body_name}" pos="0 0 {i * 0.2}">\n'

            # Get mesh info
            mesh_info = self._export_body_mesh(body, meshes_dir, i)
            if mesh_info:
                mesh_name = f"mesh_{i}"
                xml_content += f'      <geom type="mesh" mesh="{mesh_name}" material="{material_name}" mass="{mass}"/>\n'
            else:
                # Fallback to box
                xml_content += f'      <geom type="box" size="0.05 0.05 0.05" material="{material_name}" mass="{mass}"/>\n'

            xml_content += "    </body>\n"

        xml_content += "  </worldbody>\n"
        xml_content += "</mujoco>\n"

        with open(filename, "w") as f:
            f.write(xml_content)

        return filename

    def _export_body_mesh(
        self, body, meshes_dir: Path, index: int
    ) -> Optional[Dict[str, Any]]:
        """Export body geometry to mesh file."""
        try:
            if hasattr(body, "original_part") and body.original_part is not None:
                part = body.original_part

                # Generate mesh filename
                part_name = getattr(part, "name", f"part_{index}")
                mesh_filename = f"{part_name}.stl"
                mesh_path = meshes_dir / mesh_filename

                # Export part to STL
                if hasattr(part, "export") and hasattr(part.export, "stl"):
                    part.export.stl(str(mesh_path))

                    return {
                        "filename": mesh_filename,
                        "scale": "1 1 1",  # Default scale
                        "path": str(mesh_path),
                    }
        except Exception as e:
            print(f"Error exporting mesh for body {index}: {e}")

        return None

    def _export_body_textures(
        self, body, textures_dir: Path, index: int
    ) -> Optional[Dict[str, str]]:
        """Export body material textures."""
        try:
            if hasattr(body, "original_part") and body.original_part is not None:
                part = body.original_part

                # Get material from part
                if hasattr(part, "get_material") and part.get_material() is not None:
                    material = part.get_material()

                    if hasattr(material, "textures") and material.has_textures():
                        texture_files = {}

                        # Copy texture files to textures directory
                        for texture_type, texture_path in [
                            ("diffuse", material.textures.diffuse),
                            ("normal", material.textures.normal),
                            ("roughness", material.textures.roughness),
                            ("metallic", material.textures.metallic),
                        ]:
                            if texture_path and Path(texture_path).exists():
                                # Generate new filename
                                part_name = getattr(part, "name", f"part_{index}")
                                texture_ext = Path(texture_path).suffix
                                new_filename = (
                                    f"{part_name}_{texture_type}{texture_ext}"
                                )
                                new_path = textures_dir / new_filename

                                # Copy texture file
                                shutil.copy2(texture_path, new_path)
                                texture_files[texture_type] = new_filename

                        return texture_files if texture_files else None
        except Exception as e:
            print(f"Error exporting textures for body {index}: {e}")

        return None

    def _get_material_properties(self, body) -> tuple[str, str]:
        """Get material name and color from body."""
        material_name = "default"
        color_rgba = "0.8 0.8 0.8 1.0"  # Default gray

        if hasattr(body, "original_part") and body.original_part is not None:
            part = body.original_part

            # Get color
            if hasattr(part, "color") and part.color is not None:
                r, g, b, a = part.color
                color_rgba = f"{r} {g} {b} {a}"

            # Get material name
            if hasattr(part, "material") and part.material is not None:
                material_name = str(part.material).lower().replace(" ", "_")

        return material_name, color_rgba

    def xml(self, filename: str, format_type: str = "mujoco", **kwargs) -> str:
        """Export simulation to XML format (native MuJoCo format)."""
        xml_content = f'<mujoco model="{self.simulation.name or "simulation"}">\n'
        xml_content += '  <compiler angle="radian"/>\n'
        xml_content += f'  <option timestep="{self.simulation.time_step}"/>\n'

        # Add default assets
        xml_content += "  <asset>\n"
        xml_content += '    <texture name="grid" type="2d" builtin="checker" rgb1=".1 .2 .3" rgb2=".2 .3 .4" width="300" height="300"/>\n'
        xml_content += '    <material name="grid" texture="grid" texrepeat="8 8" reflectance=".2"/>\n'
        xml_content += "  </asset>\n"

        # Add worldbody
        xml_content += "  <worldbody>\n"
        xml_content += '    <geom name="floor" pos="0 0 0" size="10 10 0.1" type="plane" material="grid"/>\n'
        xml_content += '    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>\n'

        # Add bodies
        for i, body in enumerate(self.simulation.bodies):
            body_name = body.name or f"body_{i}"
            mass = body.get_mass() if hasattr(body, "get_mass") else 1.0

            xml_content += f'    <body name="{body_name}" pos="0 0 1">\n'
            xml_content += f'      <geom name="{body_name}_geom" type="box" size="0.5 0.5 0.5" mass="{mass}"/>\n'
            xml_content += "    </body>\n"

        # Add cameras from simulation
        for i, camera in enumerate(self.simulation.cameras):
            cam_name = camera.name or f"camera_{i}"
            xml_content += f'    <camera name="{cam_name}" pos="{camera.position.x} {camera.position.y} {camera.position.z}" '
            xml_content += f'xyaxes="1 0 0 0 1 0" fovy="{camera.field_of_view}"/>\n'

        # Add lights from simulation
        for i, light in enumerate(self.simulation.lights):
            light_name = light.name or f"light_{i}"
            xml_content += f'    <light name="{light_name}" pos="{light.position.x} {light.position.y} {light.position.z}" '
            xml_content += (
                f'diffuse="{light.color[0]} {light.color[1]} {light.color[2]}"/>\n'
            )

        xml_content += "  </worldbody>\n"

        # Add actuators if needed
        xml_content += "  <actuator>\n"
        xml_content += "  </actuator>\n"

        xml_content += "</mujoco>\n"

        with open(filename, "w") as f:
            f.write(xml_content)

        return filename

    def state(
        self,
        filename: str,
        format: str = "json",
        include_velocities: bool = True,
        include_forces: bool = False,
        **kwargs,
    ) -> str:
        """Export current simulation state."""
        state_data = {
            "simulation_name": self.simulation.name,
            "current_time": self.simulation.current_time,
            "time_step": self.simulation.time_step,
            "gravity": [
                self.simulation.gravity.x,
                self.simulation.gravity.y,
                self.simulation.gravity.z,
            ],
            "bodies": [],
        }

        for body in self.simulation.bodies:
            body_data = {
                "name": body.name,
                "mass": body.get_mass() if hasattr(body, "get_mass") else 1.0,
                "position": [0, 0, 0],  # Would get actual position from MuJoCo
                "orientation": [0, 0, 0, 1],  # Would get actual orientation
            }

            if include_velocities and hasattr(body, "get_linear_velocity"):
                vel = body.get_linear_velocity()
                body_data["linear_velocity"] = [vel.x, vel.y, vel.z]

            if include_velocities and hasattr(body, "get_angular_velocity"):
                ang_vel = body.get_angular_velocity()
                body_data["angular_velocity"] = [ang_vel.x, ang_vel.y, ang_vel.z]

            state_data["bodies"].append(body_data)

        with open(filename, "w") as f:
            json.dump(state_data, f, indent=2)

        return filename

    def trajectory(
        self,
        filename: str,
        format: str = "csv",
        bodies: Optional[list] = None,
        **kwargs,
    ) -> str:
        """Export trajectory data."""
        if format.lower() == "csv":
            with open(filename, "w") as f:
                f.write("time,body_name,pos_x,pos_y,pos_z,vel_x,vel_y,vel_z\n")
                # Would write actual trajectory data here
                f.write(f"{self.simulation.current_time},placeholder,0,0,0,0,0,0\n")
        else:
            trajectory_data = {
                "simulation_name": self.simulation.name,
                "trajectory": [],
            }
            with open(filename, "w") as f:
                json.dump(trajectory_data, f, indent=2)

        return filename

    def scene(
        self,
        filename: str,
        include_cameras: bool = True,
        include_lights: bool = True,
        **kwargs,
    ) -> str:
        """Export complete scene description."""
        scene_data = {
            "simulation_name": self.simulation.name,
            "physics": {
                "time_step": self.simulation.time_step,
                "gravity": [
                    self.simulation.gravity.x,
                    self.simulation.gravity.y,
                    self.simulation.gravity.z,
                ],
            },
            "bodies": [
                {"name": body.name, "type": "rigid_body"}
                for body in self.simulation.bodies
            ],
        }

        if include_cameras:
            scene_data["cameras"] = [
                {
                    "name": camera.name,
                    "position": [
                        camera.position.x,
                        camera.position.y,
                        camera.position.z,
                    ],
                    "target": [camera.target.x, camera.target.y, camera.target.z],
                    "fov": camera.field_of_view,
                }
                for camera in self.simulation.cameras
            ]

        if include_lights:
            scene_data["lights"] = [
                {
                    "name": light.name,
                    "type": light.light_type.value,
                    "position": [light.position.x, light.position.y, light.position.z],
                    "intensity": light.intensity,
                    "color": list(light.color),
                }
                for light in self.simulation.lights
            ]

        with open(filename, "w") as f:
            json.dump(scene_data, f, indent=2)

        return filename
