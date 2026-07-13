"""The CodeToCAD CLI.

``codetocad init <name>`` creates a project folder with a ``<name>.py`` file
and starts an interactive session that generates/updates part scripts.

The interactive designer covers the full robot workflow the way
``codetocad_integrations/robotics/turtlebot/turtlebot_diff_drive.py`` does by
hand: parts and sketches, joints between them, electronics (motors, cameras,
encoders bound to a microcontroller), a physics simulation with the firmware
emulated in-process, and a control web app. A live Open3D preview window can
rebuild and re-display the design after every change.

``codetocad <path/to/script>`` runs a CodeToCAD script.
"""

from __future__ import annotations

import importlib.util
import json
import re
import runpy
import subprocess
import sys
import tempfile
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

USAGE = """\
CodeToCAD - one language to define your design.

Usage:
  codetocad init <project_name>   Start a new project and open the
                                  interactive designer.
  codetocad load <path/to/project>
                                  Load an existing project folder and
                                  continue designing.
  codetocad <path/to/script.py>   Run a CodeToCAD script.
  codetocad run <path/to/script>  Same as above.
"""

#: Session state manifest kept next to the generated files, so a project
#: can be reloaded with ``codetocad load``.
STATE_FILE_NAME = ".codetocad.json"

_GREY = "\x1b[90m"
_RESET = "\x1b[0m"

#: Registry kinds that are geometry (selectable, imported by the project file).
_GEOMETRY_KINDS = ("sketch", "part")


def _sanitize_identifier(name: str) -> str:
    identifier = re.sub(r"\W+", "_", name.strip()).strip("_")
    if not identifier or identifier[0].isdigit():
        identifier = f"part_{identifier}"
    return identifier.lower()


def _camel(var_name: str) -> str:
    return "".join(word.title() for word in var_name.split("_"))


#: The preview window process: GUI windows must live on a process's main
#: thread (macOS refuses windows on background threads), so the viewer runs
#: as its own python process, watching a directory of exported STL meshes
#: and hot-reloading them whenever the version stamp changes.
_VIEWER_SOURCE = """
import json
import sys
import time
from pathlib import Path

import open3d as o3d

directory = Path(sys.argv[1])
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="CodeToCAD preview", width=1000, height=800)
vis.get_render_option().mesh_show_back_face = True
version = None
populated = False
while True:
    stamp = directory / "version.txt"
    current = stamp.read_text() if stamp.exists() else None
    if current != version:
        version = current
        colors = {}
        color_file = directory / "colors.json"
        if color_file.exists():
            colors = json.loads(color_file.read_text())
        vis.clear_geometries()
        for stl in sorted(directory.glob("*.stl")):
            mesh = o3d.io.read_triangle_mesh(str(stl))
            if mesh.is_empty():
                continue
            mesh.compute_vertex_normals()
            mesh.paint_uniform_color(colors.get(stl.stem, [0.62, 0.66, 0.7]))
            vis.add_geometry(mesh, reset_bounding_box=not populated)
            populated = True
    if not vis.poll_events():
        break
    vis.update_renderer()
    time.sleep(1 / 30)
vis.destroy_window()
"""


class LivePreview:
    """A live 3D view of the design, rendered with Open3D.

    ``update()`` exports the parts as STL meshes into a session directory
    and a small viewer process (see ``_VIEWER_SOURCE``) displays them,
    reloading whenever they change. With ``live`` set, the session rebuilds
    and re-exports after every change."""

    def __init__(self, print_fn=print):
        self._print = print_fn
        self._process: subprocess.Popen | None = None
        self._directory: Path | None = None
        self._warned = False
        self.live = False

    def available(self) -> bool:
        return importlib.util.find_spec("open3d") is not None

    def warn_unavailable(self) -> None:
        if not self._warned:
            self._warned = True
            self._print(
                "The preview needs Open3D: pip install 'codetocad[open3d]'"
            )

    @property
    def directory(self) -> Path:
        """Where the preview meshes live for this session."""
        if self._directory is None:
            self._directory = Path(tempfile.mkdtemp(prefix="codetocad_preview_"))
        return self._directory

    def update(self, parts: list) -> None:
        """Export ``parts`` to the preview directory and (re)display them."""
        if not self.available():
            self.warn_unavailable()
            return
        directory = self.directory
        for stale in directory.glob("*.stl"):
            stale.unlink()
        colors = {}
        for part in parts:
            name = getattr(part, "name", None) or f"part_{id(part)}"
            try:
                part.export(str(directory / f"{name}.stl"))
            except Exception as error:
                self._print(f"Note: could not mesh {name}: {error}")
                continue
            material = getattr(part, "material", None)
            rgba = getattr(material, "color_rgba", None) if material else None
            if rgba is not None:
                colors[name] = list(rgba.to_tuple()[:3])
        (directory / "colors.json").write_text(json.dumps(colors))
        self.publish()

    def publish(self) -> None:
        """Tell the viewer the meshes in the preview directory changed."""
        if not self.available():
            self.warn_unavailable()
            return
        (self.directory / "version.txt").write_text(str(time.time_ns()))
        self._ensure_viewer()

    def _ensure_viewer(self) -> None:
        if self._process is not None and self._process.poll() is None:
            return
        self._process = subprocess.Popen(
            [sys.executable, "-c", _VIEWER_SOURCE, str(self.directory)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def close(self) -> None:
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()
        self._process = None


class InteractiveSession:
    """The interactive menu shown after ``codetocad init``.

    All operations update generated python files: one file per part/device,
    plus a ``<project>.py`` entry point that imports and builds the geometry.
    """

    def __init__(self, project_dir: Path, project_name: str, input_fn=None, output_fn=None):
        # Resolve so generated-file paths survive the chdir in _project_env
        # (codetocad load/init may be given a relative path).
        self.project_dir = Path(project_dir).resolve()
        self.project_name = project_name
        self._input = input_fn or input
        self._print = output_fn or print
        self._use_color = output_fn is None and sys.stdout.isatty()
        # var name -> {"file": Path, "kind": "sketch" | "part" | "mcu" |
        #              "encoder" | "sim" | "app" | "emulator", ...extras}
        self.parts: dict[str, dict] = {}
        # joint name -> {"parent": var, "child": var, "type": "fixed" | ...}
        self.joints: dict[str, dict] = {}
        self.selected: str | None = None
        # Modeling backend for generated parts: "none" (pure CodeToCAD),
        # "build123d" or "blender". Asked on first part creation.
        self.backend: str | None = None
        self.preview = LivePreview(self._print)
        self._shown_welcome = False
        self._welcome: str | None = None
        self._warned_core_ops = False

    # -- IO helpers --

    def _ask(self, prompt: str) -> str:
        try:
            return self._input(prompt).strip()
        except (EOFError, StopIteration):
            raise _QuitSession()

    def _header(self) -> None:
        self._print("")
        if not self._shown_welcome:
            self._print(self._welcome or f"You've started the project {self.project_name}!")
            self._shown_welcome = True
        else:
            self._print(f"On project {self.project_name}.")
        self._print("")
        status = f"Selected Geometry: {self.selected or 'None'}"
        if self.preview.live:
            status += "   [live preview on]"
        self._print(status)
        self._print("")

    def _grey(self, text: str) -> str:
        return f"{_GREY}{text}{_RESET}" if self._use_color else text

    def _menu(
        self,
        title: str,
        options: list[tuple[str, bool]],
        hint: str = "select geometry first (main menu > Select geometry)",
    ) -> int:
        """Print a numbered menu; disabled options are greyed out and cannot
        be chosen. Returns the chosen 1-based index, or 0 for back."""
        self._print(title)
        for number, (label, enabled) in enumerate(options, start=1):
            line = f"{number}. {label}"
            self._print(line if enabled else self._grey(line))
        self._print("")
        while True:
            choice = self._ask(
                "Enter a command using the numbers (b for back, q to quit): "
            )
            if choice.lower() in ("q", "quit", "exit"):
                raise _QuitSession()
            if choice.lower() in ("b", "back"):
                return 0
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                index = int(choice)
                if not options[index - 1][1]:
                    self._print(f"That option is unavailable: {hint}.")
                    continue
                return index
            self._print("Please enter one of the listed numbers.")

    def _ask_dimensions(self, prompt: str, count: int) -> list[str] | None:
        raw = self._ask(prompt)
        dims = [dim.strip() for dim in raw.split(",") if dim.strip()]
        if len(dims) != count:
            self._print(f"Expected {count} comma-separated value(s), got {len(dims)}.")
            return None
        return dims

    def _ask_numbers(self, prompt: str, defaults: list[float]) -> list[float]:
        """Comma-separated numbers with per-position defaults; blank keeps
        the default."""
        raw = self._ask(prompt)
        values = list(defaults)
        for index, token in enumerate(part.strip() for part in raw.split(",")):
            if not token or index >= len(values):
                continue
            try:
                values[index] = float(token)
            except ValueError:
                self._print(f"Could not parse {token!r}; using {values[index]}.")
        return values

    # -- registry helpers --

    def _vars_of_kind(self, *kinds: str) -> list[str]:
        return [var for var, info in self.parts.items() if info["kind"] in kinds]

    def _geometry_vars(self) -> list[str]:
        return self._vars_of_kind(*_GEOMETRY_KINDS)

    def _selected_kind(self) -> str | None:
        return self.parts[self.selected]["kind"] if self.selected else None

    def _motor_vars(self) -> list[str]:
        return [var for var, info in self.parts.items() if info.get("motor")]

    def _camera_vars(self) -> list[str]:
        return [var for var, info in self.parts.items() if info.get("camera")]

    # -- codegen helpers --

    def _part_file(self, var_name: str) -> Path:
        return self.parts[var_name]["file"]

    def _append_line(self, var_name: str, line: str) -> None:
        path = self._part_file(var_name)
        path.write_text(path.read_text() + line + "\n")

    def _append_block(self, var_name: str, block: str) -> None:
        path = self._part_file(var_name)
        path.write_text(path.read_text().rstrip("\n") + "\n\n" + block.strip("\n") + "\n")

    def _ensure_part_import(self, into_var: str, other_var: str) -> None:
        """Make sure `into_var`'s file imports `other_var` from its module."""
        path = self._part_file(into_var)
        if path == self._part_file(other_var):
            return
        import_line = f"from {self._part_file(other_var).stem} import {other_var}"
        content = path.read_text()
        if import_line in content:
            return
        lines = content.splitlines()
        insert_at = next(
            (i + 1 for i, l in enumerate(lines) if l.startswith("import codetocad")),
            0,
        )
        lines.insert(insert_at, import_line)
        path.write_text("\n".join(lines) + "\n")

    def _register(
        self, var_name: str, kind: str, file: Path, select: bool = True, **extra
    ) -> None:
        self.parts[var_name] = {"file": file, "kind": kind, **extra}
        if select and kind in _GEOMETRY_KINDS:
            self.selected = var_name
        self._write_project_file()

    def _unique_var(self, base: str) -> str:
        var_name = base
        counter = 2
        while var_name in self.parts:
            var_name = f"{base}_{counter}"
            counter += 1
        return var_name

    def _write_project_file(self) -> None:
        lines = [f'"""CodeToCAD project {self.project_name}."""', ""]
        geometry = self._geometry_vars()
        for var_name in geometry:
            lines.append(f"from {self._part_file(var_name).stem} import {var_name}")
        lines += [
            "",
            'if __name__ == "__main__":',
        ]
        if geometry:
            joined = ", ".join(geometry)
            lines += [
                f"    for _part in [{joined}]:",
                "        _part.build()",
            ]
        else:
            lines.append("    pass")
        (self.project_dir / f"{self.project_name}.py").write_text(
            "\n".join(lines) + "\n"
        )

    # -- session state (save / load) --

    def _save_state(self) -> None:
        """Persist the session state next to the generated files so the
        project can be reopened with ``codetocad load``."""
        data = {
            "project": self.project_name,
            "backend": self.backend,
            "selected": self.selected,
            "joints": self.joints,
            "parts": {
                var_name: {
                    **{key: value for key, value in info.items() if key != "file"},
                    "file": info["file"].name,
                }
                for var_name, info in self.parts.items()
            },
        }
        (self.project_dir / STATE_FILE_NAME).write_text(
            json.dumps(data, indent=2) + "\n"
        )

    def restore(self) -> bool:
        """Load session state from the project manifest, falling back to
        scanning the generated files. Returns True when anything was
        recovered."""
        manifest = self.project_dir / STATE_FILE_NAME
        data = None
        if manifest.exists():
            try:
                data = json.loads(manifest.read_text())
            except ValueError:
                self._print(
                    f"Note: could not read {manifest.name}; scanning the "
                    "project files instead."
                )
        if data:
            self.project_name = data.get("project") or self.project_name
            self.backend = data.get("backend")
            for var_name, info in data.get("parts", {}).items():
                file = self.project_dir / str(info.get("file", ""))
                if not file.exists():
                    continue
                info = dict(info)
                info["file"] = file
                camera = info.get("camera")
                if camera and isinstance(camera.get("resolution"), list):
                    camera["resolution"] = tuple(camera["resolution"])
                self.parts[var_name] = info
            self.joints = {
                name: joint
                for name, joint in data.get("joints", {}).items()
                if joint.get("parent") in self.parts and joint.get("child") in self.parts
            }
            geometry = self._geometry_vars()
            selected = data.get("selected")
            self.selected = (
                selected if selected in geometry else (geometry[-1] if geometry else None)
            )
        else:
            self._scan_project()
        if self.parts:
            counts = Counter(info["kind"] for info in self.parts.values())
            summary = ", ".join(
                f"{count} {kind}" for kind, count in sorted(counts.items())
            )
            self._welcome = (
                f"You've loaded the project {self.project_name} ({summary})!"
            )
        return bool(self.parts)

    def _scan_project(self) -> None:
        """Best-effort state recovery by reading the generated files - used
        when the manifest is missing (e.g. a hand-assembled project)."""
        files = [
            path
            for path in self.project_dir.glob("*.py")
            if path.stem != self.project_name
            and not path.stem.endswith("_firmware")
        ]
        # Keep the project file's import order for geometry, then the rest
        # in modification order.
        order: list[str] = []
        project_file = self.project_dir / f"{self.project_name}.py"
        if project_file.exists():
            order = re.findall(r"^from (\w+) import ", project_file.read_text(), re.M)
        files.sort(
            key=lambda path: (
                order.index(path.stem) if path.stem in order else len(order),
                path.stat().st_mtime,
            )
        )
        texts = {}
        for path in files:
            texts[path] = path.read_text()
            self._scan_file(path, texts[path])
        # Joints only make sense between recovered geometry.
        self.joints = {
            name: joint
            for name, joint in self.joints.items()
            if joint["parent"] in self.parts and joint["child"] in self.parts
        }
        # Encoders learn which joint they measure from the emulation wiring.
        for text in texts.values():
            for name, joint in re.findall(
                r"emulator\.set_sensor\('(\w+)', _encoder_reader\('(\w+)'", text
            ):
                if self.parts.get(name, {}).get("kind") == "encoder":
                    self.parts[name]["joint"] = joint
        joined = "\n".join(texts.values())
        if "codetocad_integrations.build123d import adapt" in joined:
            self.backend = "build123d"
        elif "codetocad_integrations.blender import adapt" in joined:
            self.backend = "blender"
        elif self._geometry_vars():
            self.backend = "none"
        geometry = self._geometry_vars()
        self.selected = geometry[-1] if geometry else None

    def _scan_file(self, path: Path, text: str) -> None:
        for match in re.finditer(
            r"^(\w+) = codetocad\."
            r"(rectangle|circle|text|cube|cylinder|sphere|import_file)\(",
            text,
            re.M,
        ):
            kind = (
                "sketch"
                if match.group(2) in ("rectangle", "circle", "text")
                else "part"
            )
            self.parts[match.group(1)] = {"file": path, "kind": kind}
        for match in re.finditer(r"^(\w+) = \w+\.extrude\(", text, re.M):
            self.parts[match.group(1)] = {"file": path, "kind": "part"}
        if "codetocad.Part3D" in text:  # blank part: var = ClassName(name=...)
            for match in re.finditer(r"^(\w+) = [A-Z]\w*\(name=", text, re.M):
                self.parts[match.group(1)] = {"file": path, "kind": "part"}
        for match in re.finditer(
            r"class \w+\(type\((\w+)\), codetocad\.(DC|BLDC|Stepper)MotorMixin\)",
            text,
        ):
            var_name = match.group(1)
            if var_name in self.parts:
                motor = {"kind": match.group(2).lower()}
                rpm = re.search(r"no_load_speed_rpm = ([\d.]+)", text)
                stall = re.search(r"stall_torque_nm = ([\d.]+)", text)
                if rpm:
                    motor["no_load_rpm"] = float(rpm.group(1))
                if stall:
                    motor["stall_torque"] = float(stall.group(1))
                self.parts[var_name]["motor"] = motor
        for match in re.finditer(
            r"class \w+\(type\((\w+)\), codetocad\.CameraMixin\)", text
        ):
            if match.group(1) in self.parts:
                resolution = re.search(r"resolution = \((\d+), (\d+)\)", text)
                self.parts[match.group(1)]["camera"] = {
                    "resolution": (
                        (int(resolution.group(1)), int(resolution.group(2)))
                        if resolution
                        else (320, 240)
                    )
                }
        match = re.search(r"^(\w+) = codetocad\.Microcontroller\(", text, re.M)
        if match:
            bindings = []
            for bound in re.finditer(
                r"^\w+\.bind_(actuator|sensor)\((\w+), name='(\w+)'(.*)$", text, re.M
            ):
                role, var_name, name, rest = bound.groups()
                kind = (
                    "motor"
                    if role == "actuator"
                    else ("encoder" if "a=" in rest else "camera")
                )
                bindings.append({"var": var_name, "name": name, "kind": kind})
            self.parts[match.group(1)] = {
                "file": path,
                "kind": "mcu",
                "bindings": bindings,
            }
        if "codetocad.EncoderMixin" in text:
            match = re.search(r"^(\w+) = \w+\(\)$", text, re.M)
            if match:
                cpr = re.search(r"counts_per_revolution = (\d+)", text)
                self.parts[match.group(1)] = {
                    "file": path,
                    "kind": "encoder",
                    "joint": None,
                    "cpr": int(cpr.group(1)) if cpr else 4096,
                }
        match = re.search(r"^(\w+) = simulate\(", text, re.M)
        if match:
            root = re.search(r"= simulate\(\s*(\w+)\s*,", text)
            camera = re.search(r"(\w+)_view = CameraSpec\(", text)
            info = {
                "file": path,
                "kind": "sim",
                "engine": (
                    "pybullet"
                    if "codetocad_integrations.pybullet" in text
                    else "mujoco"
                ),
                "root": root.group(1) if root else None,
                "camera": camera.group(1) if camera else None,
            }
            if "EmulatedMicrocontroller(" in text:
                info["emulated"] = True
                self.parts["emulator"] = {
                    "file": path,
                    "kind": "emulator",
                    "sim": match.group(1),
                }
            self.parts[match.group(1)] = info
        match = re.search(r"^(\w+) = codetocad\.WebApp\(", text, re.M)
        if match:
            self.parts[match.group(1)] = {
                "file": path,
                "kind": "app",
                "emulator": "emulator.communication" in text,
            }
        for match in re.finditer(
            r"^(\w+)\.(revolute|prismatic)\((\w+), (\w+), \3\)", text, re.M
        ):
            parent, method, joint_name, child = match.groups()
            self.joints[joint_name] = {"parent": parent, "child": child, "type": method}
        for match in re.finditer(
            r"^(\w+)\.fixed\(codetocad\.Location\(.*?\), (\w+),", text, re.M
        ):
            parent, child = match.groups()
            self.joints.setdefault(
                f"{child}_fixed", {"parent": parent, "child": child, "type": "fixed"}
            )

    def _new_part_file(self, var_name: str, description: str | None, code: str) -> Path:
        path = self.project_dir / f"{var_name}.py"
        header = f'"""Part {var_name} generated by the CodeToCAD CLI."""\n'
        imports = "import codetocad\n"
        prelude = ""
        if "adapt(" in code:
            if self.backend == "build123d":
                imports += "from codetocad_integrations.build123d import adapt\n"
            elif self.backend == "blender":
                imports += (
                    "from codetocad_integrations.blender import adapt, ensure_blender\n"
                )
                prelude = "ensure_blender()\n\n"
        body = imports + "\n" + prelude + code
        if description:
            body += f"{var_name}.description = {description!r}\n"
        path.write_text(header + body)
        return path

    # -- modeling backend --

    def _backend_available(self, backend: str) -> bool:
        """Whether the backend can actually run in this python/environment."""
        if backend == "build123d":
            return importlib.util.find_spec("build123d") is not None
        if backend == "blender":
            import os
            import shutil

            return (
                shutil.which(os.environ.get("CODETOCAD_BLENDER", "blender"))
                is not None
            )
        return True

    def _warn_backend_missing(self, backend: str) -> None:
        if backend == "build123d":
            self._print(
                "WARNING: build123d is not installed in the python running "
                f"this CLI ({sys.executable}).\n"
                "Exports and previews of these parts will fail until you "
                "install it, e.g.:\n"
                "  uv pip install build123d    (or: pip install 'codetocad[build123d]')"
            )
        elif backend == "blender":
            self._print(
                "WARNING: no blender executable found on the PATH. Install "
                "Blender or point CODETOCAD_BLENDER at it."
            )

    def _print_missing_module_hint(self, error: Exception) -> None:
        name = getattr(error, "name", None)
        if name in ("build123d", "open3d"):
            self._print(
                f"The {name!r} package is missing from the python running "
                f"this CLI ({sys.executable}). Install it with:\n"
                f"  uv pip install {name}    (or: pip install 'codetocad[{name}]')"
            )

    def _factory(self, call: str) -> str:
        """Wrap a core factory call in the backend's ``adapt()`` so recorded
        operations (booleans, shells, holes, ...) are replayed on real CAD
        geometry in exports and previews."""
        if self.backend in ("build123d", "blender"):
            return f"adapt({call})"
        return call

    def _ensure_backend(self) -> None:
        if self.backend is not None:
            return
        choice = self._menu(
            "Which modeling backend should parts use? "
            "(changeable later: Part > Set modeling backend)",
            [
                ("No integration (pure CodeToCAD; exports mesh only the base shapes)", True),
                ("Build123D (CAD kernel: booleans/shells/holes in exports and preview)", True),
                ("Blender (part files run under blender --background)", True),
            ],
        )
        self.backend = {0: "none", 1: "none", 2: "build123d", 3: "blender"}[choice]
        if self.backend != "none" and not self._backend_available(self.backend):
            self._warn_backend_missing(self.backend)
            if not self._ask("Use it anyway? y/N: ").lower().startswith("y"):
                self.backend = "none"
                self._print("Using no integration for now.")
                return
        if self.backend == "build123d":
            self._print("Using Build123D.")
        elif self.backend == "blender":
            self._print("Using Blender.")

    def _set_backend(self) -> None:
        current = self.backend or "not set"
        choice = self._menu(
            f"Modeling backend (current: {current}):",
            [
                ("No integration (pure CodeToCAD)", True),
                ("Build123D (CAD kernel: booleans/shells/holes everywhere)", True),
                ("Blender (part files run under blender --background)", True),
            ],
        )
        if choice == 0:
            return
        previous = self.backend
        self.backend = ("none", "build123d", "blender")[choice - 1]
        if self.backend != "none" and not self._backend_available(self.backend):
            self._warn_backend_missing(self.backend)
            if not self._ask("Use it anyway? y/N: ").lower().startswith("y"):
                self.backend = previous
                self._print(f"Keeping the previous backend ({previous or 'not set'}).")
                return
        self._print(f"New parts will use the {self.backend} backend.")
        if self.backend == "none":
            return
        plain_files = [
            path
            for path in {self._part_file(var) for var in self._geometry_vars()}
            if "adapt(" not in path.read_text()
        ]
        if plain_files and not self._ask(
            f"Rewrite the {len(plain_files)} existing part file(s) to use "
            f"{self.backend} too? Y/n: "
        ).lower().startswith("n"):
            self._retrofit_backend(plain_files)
            self._refresh_preview()

    def _retrofit_backend(self, files: list[Path]) -> None:
        """Wrap the factory calls of already-generated files in ``adapt()``."""
        factory_call = re.compile(
            r"^(\w+ = )(codetocad\."
            r"(?:cube|cylinder|sphere|import_file|rectangle|circle|text)\(.*\))$",
            re.M,
        )
        if self.backend == "build123d":
            import_line = "from codetocad_integrations.build123d import adapt"
            prelude = ""
        else:
            import_line = "from codetocad_integrations.blender import adapt, ensure_blender"
            prelude = "\nensure_blender()"
        for path in files:
            text, wrapped = factory_call.subn(r"\1adapt(\2)", path.read_text())
            if not wrapped:
                continue
            lines = text.splitlines()
            insert_at = next(
                (i + 1 for i, l in enumerate(lines) if l.startswith("import codetocad")),
                0,
            )
            lines.insert(insert_at, import_line + prelude)
            path.write_text("\n".join(lines) + "\n")
            self._print(f"Rewrote {path.name} to use {self.backend}.")

    def _warn_core_operation(self) -> None:
        """Nudge once when recording kernel operations without a backend."""
        if self._warned_core_ops or self.backend not in (None, "none"):
            return
        self._warned_core_ops = True
        self._print(
            "Note: without a modeling backend this operation is recorded but "
            "exports/preview only mesh the base shape. Choose Part > Set "
            "modeling backend > Build123D to bake it into the geometry."
        )

    @contextmanager
    def _project_env(self):
        """Run generated files from the project directory with a clean module
        cache, so edits are picked up on every rebuild."""
        import os

        old_cwd = os.getcwd()
        sys.path.insert(0, str(self.project_dir))
        stale_modules = [
            name
            for name, module in sys.modules.items()
            if getattr(module, "__file__", None)
            and str(self.project_dir) in str(module.__file__)
        ]
        for name in stale_modules:
            del sys.modules[name]
        try:
            os.chdir(self.project_dir)
            yield
        finally:
            os.chdir(old_cwd)
            sys.path.remove(str(self.project_dir))

    def _execute_var(self, var_name: str | None) -> bool:
        """Run a var's file so declarative operations (such as export) take
        effect immediately. Returns whether it ran to completion."""
        if var_name is None:
            return False
        path = self._part_file(var_name)
        if self.backend == "blender":
            # ensure_blender() relaunches the running script under blender
            # --background, so the file must run in its own process.
            return self._run_subprocess([sys.executable, str(path)], path.name)
        with self._project_env():
            try:
                runpy.run_path(str(path), run_name="__codetocad_cli__")
                return True
            except Exception as error:  # surface, don't crash the session
                self._print(f"Note: could not execute {path.name}: {error}")
                self._print_missing_module_hint(error)
                return False

    def _run_subprocess(self, command: list[str], label: str) -> bool:
        try:
            result = subprocess.run(
                command,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            self._print(f"Note: could not execute {label}: {error}")
            return False
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip().splitlines()
            self._print(
                f"Note: could not execute {label}: "
                + (details[-1] if details else f"exit code {result.returncode}")
            )
            return False
        return True

    def _load_solid_parts(self) -> dict[str, object]:
        """Rebuild the 3D part files and return their live part objects."""
        files: dict[Path, list[str]] = {}
        for var_name in self._vars_of_kind("part"):
            files.setdefault(self._part_file(var_name), []).append(var_name)
        results: dict[str, object] = {}
        with self._project_env():
            for path, var_names in files.items():
                try:
                    namespace = runpy.run_path(str(path), run_name="__codetocad_cli__")
                except Exception as error:
                    self._print(f"Note: could not rebuild {path.name}: {error}")
                    self._print_missing_module_hint(error)
                    continue
                for var_name in var_names:
                    if var_name in namespace:
                        results[var_name] = namespace[var_name]
        return results

    def _refresh_preview(self, force: bool = False) -> None:
        """Rebuild the design and refresh the preview window. Called after
        every change when live preview is on."""
        if not force and not (self.preview.live and self.preview.available()):
            return
        if not self._vars_of_kind("part"):
            if force:
                self._print("Nothing to preview yet - create a part first.")
            return
        if self.backend == "blender":
            if self._export_preview_via_blender():
                self.preview.publish()
            return
        parts = self._load_solid_parts()
        if parts:
            self.preview.update(list(parts.values()))
        elif force:
            self._print(
                "The preview could not rebuild any parts - fix the notes "
                "above and try again."
            )

    def _export_preview_via_blender(self) -> bool:
        """Blender-backed files cannot run inside the CLI process, so a
        helper script (relaunched under blender by ensure_blender) exports
        the preview meshes."""
        files: dict[str, list[str]] = {}
        for var_name in self._vars_of_kind("part"):
            files.setdefault(str(self._part_file(var_name)), []).append(var_name)
        directory = self.preview.directory
        for stale in directory.glob("*.stl"):
            stale.unlink()
        script = directory / "_export_preview.py"
        script.write_text(
            "import runpy\n"
            "import sys\n"
            "from pathlib import Path\n"
            f"sys.path.insert(0, {str(self.project_dir)!r})\n"
            "from codetocad_integrations.blender import ensure_blender\n"
            "ensure_blender()\n"
            "import os\n"
            f"os.chdir({str(self.project_dir)!r})\n"
            f"for file, names in {files!r}.items():\n"
            "    namespace = runpy.run_path(file, run_name='__codetocad_cli__')\n"
            "    for name in names:\n"
            "        if name in namespace:\n"
            f"            namespace[name].export(str(Path({str(directory)!r}) / (name + '.stl')))\n"
        )
        return self._run_subprocess([sys.executable, str(script)], "the Blender preview export")

    # -- menus --

    def run(self) -> None:
        try:
            while True:
                self._header()
                has_selection = self.selected is not None
                choice = self._menu(
                    "What do you want to do?",
                    [
                        ("Part (create and shape solids)", True),
                        ("Sketch (2D profiles)", True),
                        ("Assemble (joints between geometry)", has_selection),
                        ("Electronics (motors, sensors, microcontroller)", True),
                        ("Simulate (physics simulation)", has_selection or bool(self._vars_of_kind("sim"))),
                        ("App (control dashboard)", True),
                        ("Select geometry", bool(self._geometry_vars())),
                        ("Preview (3D view of the design)", True),
                        ("Export selected geometry", has_selection),
                    ],
                )
                if choice == 0:
                    self._end_session()
                    return
                (
                    self._part_menu,
                    self._sketch_menu,
                    self._assemble_menu,
                    self._electronics_menu,
                    self._simulate_menu,
                    self._app_menu,
                    self._select_geometry,
                    self._preview_menu,
                    self._export_selected,
                )[choice - 1]()
                self._save_state()
        except _QuitSession:
            self._end_session()
            return

    def _end_session(self) -> None:
        self._save_state()
        self.preview.close()

    # -- part menu --

    def _part_menu(self) -> None:
        self._header()
        has_part = self._selected_kind() == "part"
        choice = self._menu(
            "Part - what do you want to do?",
            [
                ("Create a part", True),
                ("Set material of selected part", has_part),
                ("Transform selected part", has_part),
                ("Boolean selected part (subtract/union/intersect)", has_part),
                ("Shell selected part", has_part),
                ("Cut a hole in selected part", has_part),
                ("Define a location on selected part", has_part),
                ("Set modeling backend (bakes booleans into exports)", True),
            ],
            hint="select a 3D part first (main menu > Select geometry)",
        )
        if choice == 0:
            return
        (
            self._create_part,
            self._set_material,
            self._transform_selected,
            self._boolean_selected,
            self._shell_selected,
            self._hole_selected,
            self._define_location,
            self._set_backend,
        )[choice - 1]()

    def _create_part(self) -> None:
        self._ensure_backend()
        self._print("")
        self._print("You are creating a new part.")
        self._print("")
        raw = self._ask("Enter name, description? Leave blank for none. ")
        name, _, description = (part.strip() for part in raw.partition(","))
        var_name = _sanitize_identifier(name or f"part_{len(self.parts) + 1}")
        self._print("")
        self._print(f'You are creating a part "{var_name}".')
        self._print("")
        choice = self._menu(
            "What do you want to create?",
            [
                ("Blank Part (creates a blank part.py)", True),
                ("Import STL or other file", True),
                ("Cube", True),
                ("Cylinder", True),
                ("Sphere", True),
            ],
        )
        if choice == 0:
            return
        if choice == 1:
            code = (
                f"class {_camel(var_name)}(codetocad.Part3D):\n"
                "    def build(self):\n"
                '        """User defined script to generate a shape here."""\n'
                "        ...\n"
                "\n"
                f"{var_name} = {_camel(var_name)}(name={var_name!r})\n"
            )
        elif choice == 2:
            file_path = self._ask("Enter the path of the file to import: ")
            factory = self._factory(f"codetocad.import_file({file_path!r})")
            code = f"{var_name} = {factory}\n"
            code += f"{var_name}.name = {var_name!r}\n"
        elif choice == 3:
            dims = self._ask_dimensions(
                "Enter length, width, height of the cube: ", 3
            )
            if dims is None:
                return
            factory = self._factory(
                f"codetocad.cube("
                f"length={dims[0]!r}, width={dims[1]!r}, height={dims[2]!r})"
            )
            code = f"{var_name} = {factory}\n{var_name}.name = {var_name!r}\n"
        elif choice == 4:
            dims = self._ask_dimensions("Enter radius, height of the cylinder: ", 2)
            if dims is None:
                return
            factory = self._factory(
                f"codetocad.cylinder(radius={dims[0]!r}, height={dims[1]!r})"
            )
            code = f"{var_name} = {factory}\n{var_name}.name = {var_name!r}\n"
        else:
            dims = self._ask_dimensions("Enter radius of the sphere: ", 1)
            if dims is None:
                return
            factory = self._factory(f"codetocad.sphere(radius={dims[0]!r})")
            code = f"{var_name} = {factory}\n{var_name}.name = {var_name!r}\n"
        path = self._new_part_file(var_name, description or None, code)
        self._register(var_name, "part", path)
        self._refresh_preview()

    def _set_material(self) -> None:
        var_name = self.selected
        choice = self._menu(
            "Material:",
            [
                ("Steel", True),
                ("Aluminum", True),
                ("Custom (name, mass, color)", True),
            ],
        )
        if choice == 0:
            return
        if choice == 1:
            line = f"{var_name}.set_material(codetocad.steel_material())"
        elif choice == 2:
            line = f"{var_name}.set_material(codetocad.aluminum_material())"
        else:
            name = self._ask("Enter a material name: ") or "material"
            mass = self._ask("Enter the mass in kg (blank to skip): ")
            rgba = self._ask("Enter the color r, g, b, a in 0-1 (blank to skip): ")
            args = [repr(name)]
            if mass:
                args.append(f"mass={mass}")
            if rgba:
                channels = ", ".join(part.strip() for part in rgba.split(","))
                args.append(f"color_rgba=codetocad.Vec4({channels})")
            line = f"{var_name}.set_material(codetocad.MaterialBase({', '.join(args)}))"
        self._append_line(var_name, line)
        self._print(f"Set the material of {var_name}.")
        self._refresh_preview()

    def _transform_selected(self) -> None:
        self._print("")
        mode_choice = self._menu(
            "Transform:", [("Relative (translate by)", True), ("Absolute (move to)", True)]
        )
        if mode_choice == 0:
            return
        dims = self._ask_dimensions("Enter x, y, z: ", 3)
        if dims is None:
            return
        keyword = "relative" if mode_choice == 1 else "absolute"
        self._append_line(
            self.selected,
            f"{self.selected}.transform({keyword}=codetocad.Location("
            f"x={dims[0]!r}, y={dims[1]!r}, z={dims[2]!r}))",
        )
        self._print(f"Added {keyword} transform to {self.selected}.")
        self._refresh_preview()

    def _boolean_selected(self) -> None:
        operation_choice = self._menu(
            "Boolean operation:",
            [("Subtract", True), ("Union", True), ("Intersect", True)],
        )
        if operation_choice == 0:
            return
        other = self._choose_other_geometry(kinds=("part",))
        if other is None:
            return
        method = {1: "subtract", 2: "union", 3: "intersect"}[operation_choice]
        self._ensure_part_import(self.selected, other)
        self._append_line(
            self.selected,
            f"{self.selected}.{method}(codetocad.Location(), {other}, "
            "codetocad.Location())",
        )
        self._print(f"Added {method} of {other} to {self.selected}.")
        self._warn_core_operation()
        self._refresh_preview()

    def _shell_selected(self) -> None:
        self._print("")
        thickness = self._ask("Enter a shell thickness: ")
        self._append_line(
            self.selected, f"{self.selected}.shell(thickness={thickness!r})"
        )
        self._print(f"Added shell to {self.selected}.")
        self._warn_core_operation()
        self._refresh_preview()

    def _hole_selected(self) -> None:
        self._print("")
        dims = self._ask_dimensions("Enter the hole start x, y, z: ", 3)
        if dims is None:
            return
        radius = self._ask("Enter the hole radius: ")
        depth = self._ask("Enter the hole depth: ")
        self._append_line(
            self.selected,
            f"{self.selected}.hole(codetocad.Location("
            f"x={dims[0]!r}, y={dims[1]!r}, z={dims[2]!r}), "
            f"radius={radius!r}, amount={depth!r})",
        )
        self._print(f"Added a hole to {self.selected}.")
        self._warn_core_operation()
        self._refresh_preview()

    def _define_location(self) -> None:
        self._print("")
        location_name = _sanitize_identifier(
            self._ask("Enter a name for the location: ") or "location"
        )
        raw = self._ask(
            "Enter a cube location (e.g. TOP_CENTER) or x, y, z coordinates: "
        )
        var_name = self.selected
        if "," in raw:
            coords = [coord.strip() for coord in raw.split(",")]
            coords += ["0"] * (3 - len(coords))
            line = (
                f"{var_name}_{location_name} = codetocad.Location("
                f"x={coords[0]!r}, y={coords[1]!r}, z={coords[2]!r}, "
                f"name={location_name!r})"
            )
        else:
            member = raw.upper().replace(" ", "_")
            from codetocad.location import CubeLocations

            if member not in CubeLocations.__members__:
                self._print(f"Unknown cube location {raw!r}.")
                return
            line = (
                f"{var_name}_{location_name} = "
                f"codetocad.CubeLocations.{member}.to_location({var_name})"
            )
        self._append_line(var_name, line)
        self._print(f"Defined location {var_name}_{location_name}.")

    # -- sketch menu --

    def _sketch_menu(self) -> None:
        self._header()
        has_sketch = self._selected_kind() == "sketch"
        choice = self._menu(
            "Sketch - what do you want to do?",
            [
                ("Create a sketch", True),
                ("Extrude selected sketch into a part", has_sketch),
                ("Transform selected sketch", has_sketch),
            ],
            hint="select a sketch first (main menu > Select geometry)",
        )
        if choice == 1:
            self._create_sketch()
        elif choice == 2:
            self._extrude_selected()
        elif choice == 3:
            self._transform_selected()

    def _create_sketch(self) -> None:
        self._ensure_backend()
        self._print("")
        raw = self._ask("Enter name, description? Leave blank for none. ")
        name, _, description = (part.strip() for part in raw.partition(","))
        var_name = _sanitize_identifier(name or f"sketch_{len(self.parts) + 1}")
        choice = self._menu(
            "What do you want to create?",
            [("Rectangle", True), ("Circle", True), ("Text", True)],
        )
        if choice == 0:
            return
        if choice == 1:
            dims = self._ask_dimensions("Enter width, height of the rectangle: ", 2)
            if dims is None:
                return
            factory = self._factory(
                f"codetocad.rectangle(width={dims[0]!r}, height={dims[1]!r})"
            )
        elif choice == 2:
            dims = self._ask_dimensions("Enter radius of the circle: ", 1)
            if dims is None:
                return
            factory = self._factory(f"codetocad.circle(radius={dims[0]!r})")
        else:
            content = self._ask("Enter the text: ")
            font = self._ask("Enter the font (leave blank for default): ") or "Arial"
            size = self._ask("Enter the text size: ")
            factory = self._factory(
                f"codetocad.text({content!r}, font={font!r}, size={size!r})"
            )
        code = f"{var_name} = {factory}\n{var_name}.name = {var_name!r}\n"
        path = self._new_part_file(var_name, description or None, code)
        self._register(var_name, "sketch", path)

    def _extrude_selected(self) -> None:
        self._print("")
        height = self._ask("Enter the extrude height: ")
        default = f"{self.selected}_solid"
        raw = self._ask(f"Enter a name for the new part (default {default}): ")
        var_name = self._unique_var(_sanitize_identifier(raw or default))
        self._append_line(self.selected, f"{var_name} = {self.selected}.extrude({height!r})")
        self._append_line(self.selected, f"{var_name}.name = {var_name!r}")
        self._register(var_name, "part", self._part_file(self.selected))
        self._print(f"Extruded {self.selected} into the part {var_name}.")
        self._refresh_preview()

    # -- assemble menu --

    def _assemble_menu(self) -> None:
        self._header()
        if self._selected_kind() == "sketch":
            options = [
                ("Coincide", True),
                ("Parallel", True),
                ("Perpendicular", True),
                ("Tangent", True),
            ]
            methods = {1: "coincide", 2: "parallel", 3: "perpendicular", 4: "tangent"}
            choice = self._menu(
                f"Constrain {self.selected} - which constraint?", options
            )
            if choice == 0:
                return
            self._sketch_constraint(methods[choice])
            return
        choice = self._menu(
            f"Joint on {self.selected} - what kind?",
            [
                ("Fixed (weld another part on)", True),
                ("Revolute (hinge, e.g. a wheel axle)", True),
                ("Prismatic (slide along an axis)", True),
            ],
        )
        if choice == 0:
            return
        self._joint_selected({1: "fixed", 2: "revolute", 3: "prismatic"}[choice])

    def _sketch_constraint(self, method: str) -> None:
        other = self._choose_other_geometry(kinds=("sketch",))
        if other is None:
            return
        self._ensure_part_import(self.selected, other)
        self._append_line(
            self.selected,
            f"{self.selected}.{method}(codetocad.Location(), {other}, "
            "codetocad.Location())",
        )
        self._print(f"Added {method} constraint between {self.selected} and {other}.")

    def _joint_selected(self, method: str) -> None:
        other = self._choose_other_geometry(kinds=("part",))
        if other is None:
            return
        default = self._unique_var(f"{other}_joint")
        joint_name = _sanitize_identifier(
            self._ask(f"Enter a name for the joint (default {default}): ") or default
        )
        dims = self._ask_dimensions("Enter the joint position x, y, z: ", 3)
        if dims is None:
            return
        self._ensure_part_import(self.selected, other)
        if method == "fixed":
            location = (
                f"codetocad.Location(x={dims[0]!r}, y={dims[1]!r}, z={dims[2]!r})"
            )
            self._append_line(
                self.selected, f"{self.selected}.fixed({location}, {other}, {location})"
            )
        else:
            axis_args = ""
            raw = self._ask(
                "Enter the axis tilt x_deg, y_deg, z_deg "
                "(blank keeps the joint axis on Z; -90 on x points it along Y): "
            )
            if raw:
                degrees = [part.strip() for part in raw.split(",")]
                for keyword, value in zip(("x_deg", "y_deg", "z_deg"), degrees):
                    if value:
                        axis_args += f", {keyword}={value}"
            self._append_line(
                self.selected,
                f"{joint_name} = codetocad.Location.from_euler("
                f"x={dims[0]!r}, y={dims[1]!r}, z={dims[2]!r}"
                f"{axis_args}, name={joint_name!r})",
            )
            self._append_line(
                self.selected,
                f"{self.selected}.{method}({joint_name}, {other}, {joint_name})",
            )
        self.joints[joint_name] = {
            "parent": self.selected,
            "child": other,
            "type": method,
        }
        self._print(f"Added {method} joint {joint_name}: {self.selected} -> {other}.")
        self._refresh_preview()

    # -- electronics menu --

    def _electronics_menu(self) -> None:
        self._header()
        has_part = self._selected_kind() == "part"
        has_mcu = bool(self._vars_of_kind("mcu"))
        has_device = bool(
            self._motor_vars() or self._camera_vars() or self._vars_of_kind("encoder")
        )
        choice = self._menu(
            "Electronics - what do you want to do?",
            [
                ("Add a microcontroller", True),
                ("Make selected part a motor", has_part),
                ("Make selected part a camera", has_part),
                ("Add an encoder", True),
                ("Connect a device to the microcontroller", has_mcu and has_device),
                ("Generate firmware for the microcontroller", has_mcu),
            ],
            hint=(
                "it needs a selected 3D part, or a microcontroller with "
                "devices to connect"
            ),
        )
        if choice == 0:
            return
        (
            self._add_microcontroller,
            self._motorize_selected,
            self._camerize_selected,
            self._add_encoder,
            self._connect_device,
            self._generate_firmware,
        )[choice - 1]()

    def _add_microcontroller(self) -> None:
        self._print("")
        default = self._unique_var("mcu")
        var_name = _sanitize_identifier(
            self._ask(f"Enter a name for the microcontroller (default {default}): ")
            or default
        )
        var_name = self._unique_var(var_name)
        choice = self._menu(
            "Which board?",
            [
                ("ESP32", True),
                ("ESP32-CAM (streams camera frames)", True),
                ("ESP8266", True),
                ("Raspberry Pi Pico", True),
                ("Raspberry Pi", True),
            ],
        )
        if choice == 0:
            return
        board = ["ESP32", "ESP32_CAM", "ESP8266", "RASPBERRY_PI_PICO", "RASPBERRY_PI"][
            choice - 1
        ]
        code = (
            f"{var_name} = codetocad.Microcontroller({var_name!r}, "
            f"board=codetocad.MicrocontrollerBoard.{board})\n"
        )
        path = self._new_part_file(var_name, None, code)
        self._register(var_name, "mcu", path, bindings=[])
        self._print(
            f"Added microcontroller {var_name}. Connect motors and sensors to "
            "it from the Electronics menu."
        )

    def _motorize_selected(self) -> None:
        var_name = self.selected
        choice = self._menu(
            f"What kind of motor is {var_name}?",
            [
                ("DC motor (H-bridge driver)", True),
                ("BLDC motor (ESC or VESC)", True),
                ("Stepper motor (STEP/DIR driver)", True),
            ],
        )
        if choice == 0:
            return
        info: dict = {"kind": ("dc", "bldc", "stepper")[choice - 1]}
        if choice == 1:
            rpm, stall, volts = self._ask_numbers(
                "Enter no-load rpm, stall torque N*m, voltage "
                "(blank for 57, 1.4, 11.1 - a Dynamixel XL430): ",
                [57.0, 1.4, 11.1],
            )
            mixin, suffix = "DCMotorMixin", "DCMotor"
            body = (
                f"    no_load_speed_rpm = {rpm}\n"
                f"    stall_torque_nm = {stall}\n"
                f"    nominal_voltage = {volts}\n"
            )
            info.update(no_load_rpm=rpm, stall_torque=stall)
        elif choice == 2:
            kv, poles = self._ask_numbers(
                "Enter kv rating, pole pairs (blank for 900, 7): ", [900.0, 7]
            )
            mixin, suffix = "BLDCMotorMixin", "BLDCMotor"
            body = f"    kv_rating = {kv}\n    pole_pairs = {int(poles)}\n"
        else:
            steps, microsteps = self._ask_numbers(
                "Enter steps per revolution, microsteps (blank for 200, 16): ",
                [200, 16],
            )
            mixin, suffix = "StepperMotorMixin", "StepperMotor"
            body = (
                f"    steps_per_revolution = {int(steps)}\n"
                f"    microsteps = {int(microsteps)}\n"
            )
        class_name = f"{_camel(var_name)}{suffix}"
        self._append_block(
            var_name,
            f"class {class_name}(type({var_name}), codetocad.{mixin}):\n"
            f'    """{var_name} is also its own motor: microcontroller pins and\n'
            f'    app controls can target the part directly."""\n'
            f"{body}\n"
            f"\n{var_name}.__class__ = {class_name}",
        )
        self.parts[var_name]["motor"] = info
        self._print(f"{var_name} is now a {info['kind'].upper()} motor.")

    def _camerize_selected(self) -> None:
        var_name = self.selected
        width, height, fps = self._ask_numbers(
            "Enter resolution width, height and fps (blank for 320, 240, 8): ",
            [320, 240, 8],
        )
        class_name = f"{_camel(var_name)}Camera"
        self._append_block(
            var_name,
            f"class {class_name}(type({var_name}), codetocad.CameraMixin):\n"
            f'    """{var_name} is also the camera sensor, like an ESP32-CAM."""\n'
            f"    resolution = ({int(width)}, {int(height)})\n"
            f"    sample_rate_hz = {fps}\n"
            f"\n{var_name}.__class__ = {class_name}",
        )
        self.parts[var_name]["camera"] = {"resolution": (int(width), int(height))}
        self._print(f"{var_name} is now a camera streaming {int(width)}x{int(height)}.")

    def _add_encoder(self) -> None:
        self._print("")
        default = self._unique_var("encoder")
        var_name = _sanitize_identifier(
            self._ask(f"Enter a name for the encoder (default {default}): ") or default
        )
        var_name = self._unique_var(var_name)
        (cpr,) = self._ask_numbers(
            "Enter counts per revolution (blank for 4096): ", [4096]
        )
        joint = None
        moving_joints = [
            name
            for name, info in self.joints.items()
            if info["type"] in ("revolute", "prismatic")
        ]
        if moving_joints:
            options = [(name, True) for name in moving_joints]
            options.append(("None / decide later", True))
            choice = self._menu("Which joint does it measure?", options)
            if choice and choice <= len(moving_joints):
                joint = moving_joints[choice - 1]
        class_name = f"{_camel(var_name)}Encoder"
        code = (
            f"class {class_name}(codetocad.EncoderMixin):\n"
            f"    counts_per_revolution = {int(cpr)}\n"
            f"    sample_rate_hz = 20.0\n"
            f"\n\n{var_name} = {class_name}()\n"
        )
        path = self._new_part_file(var_name, None, code)
        self._register(var_name, "encoder", path, joint=joint, cpr=int(cpr))
        self._print(f"Added encoder {var_name} ({int(cpr)} ticks/rev).")

    def _choose_var(self, title: str, candidates: list[str]) -> str | None:
        if not candidates:
            return None
        if len(candidates) == 1:
            return candidates[0]
        choice = self._menu(title, [(var, True) for var in candidates])
        return candidates[choice - 1] if choice else None

    def _connect_device(self) -> None:
        mcu = self._choose_var("Which microcontroller?", self._vars_of_kind("mcu"))
        if mcu is None:
            return
        devices = (
            [(var, "motor") for var in self._motor_vars()]
            + [(var, "encoder") for var in self._vars_of_kind("encoder")]
            + [(var, "camera") for var in self._camera_vars()]
        )
        choice = self._menu(
            "Which device?", [(f"{var} ({kind})", True) for var, kind in devices]
        )
        if choice == 0:
            return
        var_name, kind = devices[choice - 1]
        if kind == "motor":
            pwm, direction = self._ask_numbers(
                "Enter PWM pin, direction pin (blank for 4, 16): ", [4, 16]
            )
            line = (
                f"{mcu}.bind_actuator({var_name}, name={var_name!r}, "
                f"pwm_pin={int(pwm)}, dir_pin={int(direction)})"
            )
        elif kind == "encoder":
            pin_a, pin_b = self._ask_numbers(
                "Enter encoder pin A, pin B (blank for 34, 35): ", [34, 35]
            )
            line = (
                f"{mcu}.bind_sensor({var_name}, name={var_name!r}, "
                f"a={int(pin_a)}, b={int(pin_b)})"
            )
        else:
            # Camera sensors live on dedicated pins (ESP32-CAM style).
            line = f"{mcu}.bind_sensor({var_name}, name={var_name!r})"
        self._ensure_part_import(mcu, var_name)
        self._append_line(mcu, line)
        self.parts[mcu]["bindings"].append({"var": var_name, "name": var_name, "kind": kind})
        self._print(f"Connected {var_name} to {mcu}.")

    def _generate_firmware(self) -> None:
        mcu = self._choose_var("Which microcontroller?", self._vars_of_kind("mcu"))
        if mcu is None:
            return
        firmware_name = f"{mcu}_firmware.py"
        self._append_block(
            mcu,
            "from pathlib import Path\n\n"
            f"Path(__file__).with_name({firmware_name!r}).write_text("
            f"{mcu}.generate_firmware())",
        )
        self._print(
            f"Added firmware generation. Run codetocad "
            f"{self.project_dir.name}/{self._part_file(mcu).name} to write "
            f"{firmware_name}, then flash it with mpremote."
        )

    # -- simulate menu --

    def _simulate_menu(self) -> None:
        self._header()
        has_part = self._selected_kind() == "part"
        sims = self._vars_of_kind("sim")
        mujoco_sims = [var for var in sims if self.parts[var]["engine"] == "mujoco"]
        has_mcu_bindings = any(
            self.parts[var]["bindings"] for var in self._vars_of_kind("mcu")
        )
        choice = self._menu(
            "Simulate - what do you want to do?",
            [
                ("Create a physics simulation of selected part", has_part),
                (
                    "Emulate the microcontroller inside the simulation",
                    bool(mujoco_sims) and has_mcu_bindings,
                ),
                ("Make the simulation runnable (physics viewer)", bool(sims)),
            ],
            hint=(
                "it needs a selected part, or a MuJoCo simulation plus a "
                "microcontroller with connected devices"
            ),
        )
        if choice == 1:
            self._create_simulation()
        elif choice == 2:
            self._emulate_microcontroller(mujoco_sims)
        elif choice == 3:
            self._make_sim_runnable(sims)

    def _actuated_joints(self) -> list[tuple[str, dict]]:
        """Moving joints whose child part is a motor - these become velocity
        actuators in the simulation."""
        actuated = []
        for name, joint in self.joints.items():
            motor = self.parts.get(joint["child"], {}).get("motor")
            if joint["type"] in ("revolute", "prismatic") and motor:
                actuated.append((name, motor))
        return actuated

    def _create_simulation(self) -> None:
        root = self.selected
        engine_choice = self._menu(
            "Which physics engine?",
            [
                ("MuJoCo (robots, terrain, cameras)", True),
                ("PyBullet", True),
            ],
        )
        if engine_choice == 0:
            return
        var_name = self._unique_var("sim")
        mobile = not self._ask(
            "Can it drive around (free base on a ground plane)? Y/n: "
        ).lower().startswith("n")
        if engine_choice == 2:
            code = (
                "from codetocad_integrations.pybullet import simulate\n\n"
                f"{var_name} = simulate({root}, gui=__name__ == '__main__', "
                f"fixed_base={not mobile}, ground_plane={mobile})\n"
            )
            path = self._new_part_file(var_name, None, code)
            self._register(var_name, "sim", path, engine="pybullet", root=root, camera=None)
            self._ensure_part_import(var_name, root)
            self._print(f"Created PyBullet simulation {var_name} of {root}.")
            return

        terrain = mobile and self._ask(
            "Add gentle rolling terrain to drive over? y/N: "
        ).lower().startswith("y")
        camera = None
        camera_position = None
        tilt = 15.0
        cameras = self._camera_vars()
        if cameras and self._ask(
            f"Mount the camera ({cameras[0]}) in the simulation? Y/n: "
        ).lower() not in ("n", "no"):
            camera = cameras[0]
            camera_position = self._ask_numbers(
                "Enter the camera eye x, y, z (blank for 0.06, 0, 0.14): ",
                [0.06, 0.0, 0.14],
            )
            (tilt,) = self._ask_numbers(
                "Enter the downward tilt in degrees (blank for 15): ", [15.0]
            )

        lines = ["import math", ""]
        imports = ["simulate"]
        if terrain:
            imports.insert(0, "TerrainSpec")
            lines.append("import numpy as np")
            lines.append("")
        if camera:
            imports.insert(0, "CameraSpec")
        lines.insert(0, f"from codetocad_integrations.mujoco import {', '.join(imports)}")
        if terrain:
            lines += [
                "# Gentle rolling bumps, faded to a flat launch pad at the origin.",
                "_coords = np.linspace(-3.0, 3.0, 128)",
                "_x, _y = np.meshgrid(_coords, _coords)",
                "_bumps = 0.5 * (1 + np.sin(2 * np.pi * _x / 1.2) * np.sin(2 * np.pi * _y / 1.2))",
                "_ramp = np.clip((np.hypot(_x, _y) - 0.4) / 0.6, 0.0, 1.0)",
                "_ramp = _ramp * _ramp * (3 - 2 * _ramp)  # smoothstep",
                "terrain = TerrainSpec(heights=0.04 * _bumps * _ramp, extent=(6.0, 6.0))",
                "",
            ]
        if camera:
            resolution = self.parts[camera]["camera"]["resolution"]
            x, y, z = camera_position
            lines += [
                f"_tilt = math.radians({tilt})",
                f"{camera}_view = CameraSpec(",
                f"    name={camera!r},",
                f"    link={camera!r},",
                f"    position=({x}, {y}, {z}),",
                "    xyaxes=(0, -1, 0, math.sin(_tilt), 0, math.cos(_tilt)),",
                "    fovy=60.0,",
                f"    resolution={resolution},",
                ")",
                "",
            ]
        call = [f"{var_name} = simulate(", f"    {root},", f"    fixed_base={not mobile},"]
        if mobile:
            call.append("    ground_plane=True,")
        actuated = self._actuated_joints()
        if actuated:
            names = [name for name, _ in actuated]
            types = ", ".join(f"{name!r}: 'velocity'" for name in names)
            forces = ", ".join(
                f"{name!r}: {motor.get('stall_torque') or 1.4}"
                for name, motor in actuated
            )
            damping = ", ".join(f"{name!r}: 0.005" for name in names)
            call += [
                f"    actuator_types={{{types}}},",
                "    # Stall torque, damping and reflected rotor inertia keep",
                "    # small geared motors stable instead of oscillating.",
                f"    actuator_forcerange={{{forces}}},",
                f"    joint_damping={{{damping}}},",
                f"    joint_armature={{{damping}}},",
            ]
        if camera:
            call.append(f"    cameras=[{camera}_view],")
        if terrain:
            call.append("    terrain=terrain,")
        call.append(")")
        code = "\n".join(lines + call) + "\n"
        path = self._new_part_file(var_name, None, code)
        self._register(var_name, "sim", path, engine="mujoco", root=root, camera=camera)
        self._ensure_part_import(var_name, root)
        self._print(
            f"Created MuJoCo simulation {var_name} of {root}"
            + (f" with {len(actuated)} actuated joint(s)" if actuated else "")
            + "."
        )

    def _joint_for_device(self, var_name: str, role: str) -> str | None:
        """The joint a bound motor drives (its own axle) or an encoder
        measures; asks when it cannot be inferred."""
        if role == "encoder" and self.parts[var_name].get("joint"):
            return self.parts[var_name]["joint"]
        moving = [
            name
            for name, joint in self.joints.items()
            if joint["type"] in ("revolute", "prismatic")
        ]
        if role == "motor":
            own = [name for name in moving if self.joints[name]["child"] == var_name]
            if len(own) == 1:
                return own[0]
            moving = own or moving
        if not moving:
            self._print(f"No moving joint found for {var_name}; skipping it.")
            return None
        return self._choose_var(f"Which joint does {var_name} drive/measure?", moving)

    def _emulate_microcontroller(self, mujoco_sims: list[str]) -> None:
        sim = self._choose_var("Which simulation?", mujoco_sims)
        mcu = self._choose_var(
            "Which microcontroller?",
            [var for var in self._vars_of_kind("mcu") if self.parts[var]["bindings"]],
        )
        if sim is None or mcu is None:
            return
        bindings = self.parts[mcu]["bindings"]
        lines = [
            "# -- emulation: the microcontroller's firmware channels wired to",
            "# the physics, exactly like real firmware over serial --",
            f"emulator = codetocad.EmulatedMicrocontroller({mcu})",
            "emulator.communication.connect()",
        ]
        motors = [b for b in bindings if b["kind"] == "motor"]
        encoders = [b for b in bindings if b["kind"] == "encoder"]
        cameras = [b for b in bindings if b["kind"] == "camera"]
        if motors:
            lines += [
                "",
                "",
                "def _motor_handler(joint_name, no_load_rpm):",
                "    def handle(value):",
                "        if not isinstance(value, dict):",
                "            value = {'duty': float(value)}",
                "        if value.get('stop'):",
                "            rpm = 0.0",
                "        elif 'velocity_rpm' in value:",
                "            rpm = float(value['velocity_rpm'])",
                "        elif 'duty' in value:",
                "            rpm = float(value['duty']) * no_load_rpm",
                "        else:",
                "            return",
                "        rpm = max(-no_load_rpm, min(no_load_rpm, rpm))",
                f"        {sim}.set_joint_velocity_target(joint_name, rpm * 2 * math.pi / 60)",
                "    return handle",
                "",
            ]
        if encoders:
            lines += [
                "",
                "def _encoder_reader(joint_name, counts_per_rev):",
                "    def read():",
                f"        angle = {sim}.get_joint_value(joint_name)",
                "        return {",
                "            'count': int(angle / (2 * math.pi) * counts_per_rev),",
                f"            'rpm': {sim}.get_joint_velocity(joint_name) * 60 / (2 * math.pi),",
                "        }",
                "    return read",
                "",
            ]
        sim_camera = self.parts[sim].get("camera")
        if cameras and sim_camera:
            lines += [
                "",
                "def _read_frame():",
                "    import base64",
                "",
                f"    png = codetocad.encode_png({sim}.get_camera_image({sim_camera!r}))",
                "    return {'frame': base64.b64encode(png).decode('ascii')}",
                "",
            ]
        lines.append("")
        for binding in motors:
            joint = self._joint_for_device(binding["var"], "motor")
            if joint is None:
                continue
            rpm = self.parts[binding["var"]]["motor"].get("no_load_rpm") or 100.0
            lines.append(
                f"emulator.on_command({binding['name']!r}, _motor_handler({joint!r}, {rpm}))"
            )
        for binding in encoders:
            joint = self._joint_for_device(binding["var"], "encoder")
            if joint is None:
                continue
            cpr = self.parts[binding["var"]].get("cpr", 4096)
            lines.append(
                f"emulator.set_sensor({binding['name']!r}, _encoder_reader({joint!r}, {cpr}))"
            )
        for binding in cameras:
            if sim_camera:
                lines.append(f"emulator.set_sensor({binding['name']!r}, _read_frame)")
        root = self.parts[sim]["root"]
        lines += [
            "",
            "",
            "def _read_pose():",
            f"    position, _ = {sim}.get_body_pose({root!r})",
            "    return {'x': round(position[0], 4), 'y': round(position[1], 4), "
            "'z': round(position[2], 4)}",
            "",
            "",
            "emulator.add_telemetry('pose', _read_pose, sample_rate_hz=10.0)",
        ]
        self._ensure_part_import(sim, mcu)
        self._append_block(sim, "\n".join(lines))
        self._register("emulator", "emulator", self._part_file(sim), sim=sim)
        self.parts[sim]["emulated"] = True
        self._print(
            f"Wired {mcu} into {sim}: motor commands drive the joints, "
            "encoder/camera telemetry reads back from the physics."
        )

    def _make_sim_runnable(self, sims: list[str]) -> None:
        sim = self._choose_var("Which simulation?", sims)
        if sim is None:
            return
        path = self._part_file(sim)
        if "if __name__ ==" in path.read_text():
            self._print(f"{path.name} is already runnable.")
            return
        if self.parts[sim]["engine"] == "mujoco":
            step = (
                f"    {sim}.launch_viewer(on_step=lambda: "
                f"emulator.step({sim}.data.time))"
                if self.parts[sim].get("emulated")
                else f"    {sim}.launch_viewer()"
            )
            block = (
                "if __name__ == '__main__':\n"
                "    # macOS needs mjpython for the MuJoCo viewer window.\n"
                f"{step}"
            )
        else:
            block = (
                "if __name__ == '__main__':\n"
                "    import time\n"
                "\n"
                f"    while {sim}.is_connected():\n"
                f"        {sim}.step(4)\n"
                "        time.sleep(4 / 240)"
            )
        self._append_block(sim, block)
        self._print(
            f"Run it with: codetocad {self.project_dir.name}/{path.name}"
            + (
                " (use mjpython on macOS for the viewer window)"
                if self.parts[sim]["engine"] == "mujoco"
                else ""
            )
        )

    # -- app menu --

    def _app_menu(self) -> None:
        self._header()
        apps = self._vars_of_kind("app")
        has_app = bool(apps)
        has_motor = bool(self._motor_vars())
        has_encoder = bool(self._vars_of_kind("encoder"))
        has_pose = any(
            self.parts[var].get("emulated") for var in self._vars_of_kind("sim")
        )
        choice = self._menu(
            "App - what do you want to do?",
            [
                ("Create a web app", True),
                ("Add a motor slider", has_app and has_motor),
                ("Add a motor stop button", has_app and has_motor),
                ("Add a sensor gauge", has_app and (has_encoder or has_pose)),
                ("Add a sensor plot", has_app and has_encoder),
                ("Add the camera image", has_app and bool(self._camera_vars())),
                ("Make the app runnable", has_app),
            ],
            hint="create the web app and the device it displays first",
        )
        if choice == 0:
            return
        (
            self._create_app,
            self._app_add_slider,
            self._app_add_button,
            self._app_add_gauge,
            self._app_add_plot,
            self._app_add_image,
            self._make_app_runnable,
        )[choice - 1]()

    def _create_app(self) -> None:
        self._print("")
        title = self._ask(f"Enter a title (default {self.project_name}): ") or self.project_name
        var_name = self._unique_var("app")
        emulators = self._vars_of_kind("emulator")
        if emulators:
            code = (
                f"{var_name} = codetocad.WebApp({title!r})"
                f".set_communication(emulator.communication)\n"
            )
        else:
            code = (
                f"{var_name} = codetocad.WebApp({title!r})\n"
                "# Talk to real hardware by setting a communication, e.g.:\n"
                f"# {var_name}.set_communication(codetocad.SerialCommunication())\n"
            )
        path = self._new_part_file(var_name, None, code)
        self._register(var_name, "app", path, emulator=bool(emulators))
        if emulators:
            self._ensure_part_import(var_name, "emulator")
        self._print(
            f"Created web app {var_name}. Add sliders, gauges and the camera "
            "image from the App menu."
        )

    def _pick_app(self) -> str | None:
        return self._choose_var("Which app?", self._vars_of_kind("app"))

    def _app_add_slider(self) -> None:
        app = self._pick_app()
        motor = self._choose_var("Which motor?", self._motor_vars())
        if app is None or motor is None:
            return
        rpm = self.parts[motor]["motor"].get("no_load_rpm") or 100.0
        self._ensure_part_import(app, motor)
        self._append_line(
            app,
            f"{app}.add_slider('{motor} (rpm)', target={motor}, "
            f"command='velocity_rpm', minimum=-{rpm}, maximum={rpm})",
        )
        self._print(f"Added a velocity slider for {motor}.")

    def _app_add_button(self) -> None:
        app = self._pick_app()
        motor = self._choose_var("Which motor?", self._motor_vars())
        if app is None or motor is None:
            return
        self._ensure_part_import(app, motor)
        self._append_line(
            app,
            f"{app}.add_button('stop {motor}', target={motor}, value={{'stop': True}})",
        )
        self._print(f"Added a stop button for {motor}.")

    def _app_add_gauge(self) -> None:
        app = self._pick_app()
        if app is None:
            return
        sources = [(var, "encoder") for var in self._vars_of_kind("encoder")]
        if any(self.parts[var].get("emulated") for var in self._vars_of_kind("sim")):
            sources.append(("pose", "pose"))
        choice = self._menu(
            "Which source?", [(f"{var} ({kind})", True) for var, kind in sources]
        )
        if choice == 0:
            return
        source, kind = sources[choice - 1]
        if kind == "encoder":
            key_choice = self._menu(
                "Which reading?", [("count (ticks)", True), ("rpm", True)]
            )
            if key_choice == 0:
                return
            key, units = [("count", "ticks"), ("rpm", "rpm")][key_choice - 1]
            self._ensure_part_import(app, source)
            line = (
                f"{app}.add_gauge('{source} {key}', source={source}, "
                f"key={key!r}, units={units!r})"
            )
        else:
            key_choice = self._menu("Which axis?", [("x", True), ("y", True), ("z", True)])
            if key_choice == 0:
                return
            key = ("x", "y", "z")[key_choice - 1]
            line = f"{app}.add_gauge('pose {key}', source='pose', key={key!r}, units='m')"
        self._append_line(app, line)
        self._print("Added the gauge.")

    def _app_add_plot(self) -> None:
        app = self._pick_app()
        encoder = self._choose_var("Which encoder?", self._vars_of_kind("encoder"))
        if app is None or encoder is None:
            return
        self._ensure_part_import(app, encoder)
        self._append_line(
            app, f"{app}.add_plot('{encoder} (rpm)', source={encoder}, key='rpm')"
        )
        self._print(f"Added an rpm plot for {encoder}.")

    def _app_add_image(self) -> None:
        app = self._pick_app()
        camera = self._choose_var("Which camera?", self._camera_vars())
        if app is None or camera is None:
            return
        self._ensure_part_import(app, camera)
        self._append_line(
            app, f"{app}.add_image('{camera} view', source={camera}, key='frame')"
        )
        self._print(f"Added the live image from {camera}.")

    def _make_app_runnable(self) -> None:
        app = self._pick_app()
        if app is None:
            return
        path = self._part_file(app)
        if "if __name__ ==" in path.read_text():
            self._print(f"{path.name} is already runnable.")
            return
        (port,) = self._ask_numbers("Enter the port (blank for 8080): ", [8080])
        port = int(port)
        emulated_sims = [
            var
            for var in self._vars_of_kind("sim")
            if self.parts[var].get("emulated") and self.parts[var]["engine"] == "mujoco"
        ]
        if self.parts[app].get("emulator") and emulated_sims:
            sim = emulated_sims[0]
            self._ensure_part_import(app, sim)
            block = (
                "if __name__ == '__main__':\n"
                "    import threading\n"
                "    import time\n"
                "\n"
                "    # Physics in a background thread; the app owns the main thread.\n"
                "    def _physics_loop():\n"
                "        start_wall = time.monotonic()\n"
                f"        start_sim = {sim}.data.time\n"
                "        while True:\n"
                f"            {sim}.step(4)\n"
                f"            emulator.step({sim}.data.time)\n"
                f"            lag = ({sim}.data.time - start_sim) - (time.monotonic() - start_wall)\n"
                "            if lag > 0:\n"
                "                time.sleep(lag)\n"
                "\n"
                "    threading.Thread(target=_physics_loop, daemon=True).start()\n"
                f"    {app}.run(port={port})"
            )
        else:
            block = f"if __name__ == '__main__':\n    {app}.run(port={port})"
        self._append_block(app, block)
        self._print(
            f"Run it with: codetocad {self.project_dir.name}/{path.name} "
            f"then open http://localhost:{port}"
        )

    # -- preview menu --

    def _preview_menu(self) -> None:
        self._header()
        live_label = (
            "Turn off live preview"
            if self.preview.live
            else "Turn on live preview (rebuild + display after every change)"
        )
        choice = self._menu(
            "Preview - what do you want to do?",
            [
                ("Open/refresh the preview window", True),
                (live_label, True),
                ("Save a PNG snapshot", True),
                ("Close the preview window", True),
            ],
        )
        if choice == 1:
            self._refresh_preview(force=True)
        elif choice == 2:
            self.preview.live = not self.preview.live
            if self.preview.live and not self.preview.available():
                self.preview.warn_unavailable()
                self.preview.live = False
            elif self.preview.live:
                self._print("Live preview is on.")
                self._refresh_preview()
            else:
                self._print("Live preview is off.")
        elif choice == 3:
            self._snapshot()
        elif choice == 4:
            self.preview.close()

    def _snapshot(self) -> None:
        if self.backend == "blender":
            self._print(
                "PNG snapshots are not supported with the Blender backend "
                "yet - use Open/refresh the preview window instead."
            )
            return
        parts = self._load_solid_parts()
        if not parts:
            self._print("Nothing to render yet - create a part first.")
            return
        default = self.project_dir / "preview.png"
        destination = self._ask(f"Enter a PNG path (default {default}): ") or str(default)
        try:
            from codetocad_integrations.open3d.viewer import render
        except ImportError:
            self.preview.warn_unavailable()
            return
        try:
            render(*parts.values(), path=destination)
        except Exception as error:
            self._print(f"Note: could not render the snapshot: {error}")
            return
        self._print(f"Saved {destination}.")

    # -- selection & export --

    def _select_geometry(self) -> None:
        geometry = self._geometry_vars()
        if not geometry:
            self._print("There is no geometry yet. Create a part or sketch first.")
            return
        self._print("")
        choice = self._menu(
            "Select geometry:", [(var_name, True) for var_name in geometry]
        )
        if choice:
            self.selected = geometry[choice - 1]

    def _export_selected(self) -> None:
        if self.selected is None:
            self._print("Please select geometry first.")
            return
        self._print("")
        default = f"{self.selected}.stl"
        destination = (
            self._ask(f"Enter an export file path (default {default}): ") or default
        )
        line = f"{self.selected}.export({destination!r})"
        if line not in self._part_file(self.selected).read_text():
            self._append_line(self.selected, line)
        executed = self._execute_var(self.selected)
        target = Path(destination)
        if not target.is_absolute():
            target = self.project_dir / target
        if executed and target.exists():
            self._print(f"Exported {self.selected} to {target}.")
        else:
            file_name = self._part_file(self.selected).name
            self._print(
                f"The export did not complete (see the note above). The "
                f"export line was saved in {file_name}; fix the problem and "
                f"export again, or run: codetocad {self.project_dir.name}/{file_name}"
            )

    def _choose_other_geometry(self, kinds=_GEOMETRY_KINDS) -> str | None:
        others = [
            var_name
            for var_name in self._vars_of_kind(*kinds)
            if var_name != self.selected
        ]
        if not others:
            self._print("There is no other geometry to use. Create another part first.")
            return None
        choice = self._menu(
            "With which geometry?", [(var_name, True) for var_name in others]
        )
        if choice == 0:
            return None
        return others[choice - 1]


class _QuitSession(Exception):
    pass


def init_project(name: str, parent_dir: Path | None = None) -> Path:
    project_dir = (parent_dir or Path.cwd()) / name
    project_dir.mkdir(parents=True, exist_ok=True)
    project_file = project_dir / f"{name}.py"
    if not project_file.exists():
        project_file.write_text(
            f'"""CodeToCAD project {name}."""\n\n'
            'if __name__ == "__main__":\n'
            "    pass\n"
        )
    return project_dir


def run_script(path: str) -> None:
    script = Path(path)
    if script.is_dir():
        candidate = script / f"{script.name}.py"
        if not candidate.exists():
            raise SystemExit(f"No script named {candidate.name} in {script}")
        script = candidate
    if not script.exists():
        raise SystemExit(f"No such script: {path}")
    sys.path.insert(0, str(script.parent))
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        sys.path.remove(str(script.parent))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    if args[0] == "--version":
        from codetocad import __version__

        print(__version__)
        return 0
    if args[0] == "init":
        if len(args) < 2:
            print("Usage: codetocad init <project_name>")
            return 1
        name = _sanitize_identifier(args[1])
        project_dir = init_project(name)
        session = InteractiveSession(project_dir, name)
        if (project_dir / STATE_FILE_NAME).exists():
            session.restore()
        session.run()
        return 0
    if args[0] == "load":
        if len(args) < 2:
            print("Usage: codetocad load <path/to/project>")
            return 1
        project_dir = Path(args[1]).expanduser()
        if not project_dir.is_dir():
            raise SystemExit(f"No such project folder: {args[1]}")
        name = _sanitize_identifier(project_dir.name)
        session = InteractiveSession(project_dir, name)
        if not session.restore():
            print(f"Note: no CodeToCAD project found in {project_dir}; starting fresh.")
        session.run()
        return 0
    target = args[1] if args[0] == "run" and len(args) > 1 else args[0]
    run_script(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
