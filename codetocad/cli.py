"""The CodeToCAD CLI.

``codetocad init <name>`` creates a project folder with a ``<name>.py`` file
and starts an interactive session that generates/updates part scripts.

``codetocad <path/to/script>`` runs a CodeToCAD script.
"""

from __future__ import annotations

import re
import runpy
import sys
from pathlib import Path

USAGE = """\
CodeToCAD - one language to define your design.

Usage:
  codetocad init <project_name>   Start a new project and open the
                                  interactive designer.
  codetocad <path/to/script.py>   Run a CodeToCAD script.
  codetocad run <path/to/script>  Same as above.
"""


def _sanitize_identifier(name: str) -> str:
    identifier = re.sub(r"\W+", "_", name.strip()).strip("_")
    if not identifier or identifier[0].isdigit():
        identifier = f"part_{identifier}"
    return identifier.lower()


class InteractiveSession:
    """The interactive menu shown after ``codetocad init``.

    All operations update generated python part files, extending to the full
    functionality of the CodeToCAD classes.
    """

    def __init__(self, project_dir: Path, project_name: str, input_fn=None, output_fn=None):
        self.project_dir = Path(project_dir)
        self.project_name = project_name
        self._input = input_fn or input
        self._print = output_fn or print
        # var name -> {"file": Path, "dim": "2d" | "3d"}
        self.parts: dict[str, dict] = {}
        self.selected: str | None = None
        self._shown_welcome = False

    # -- IO helpers --

    def _ask(self, prompt: str) -> str:
        try:
            return self._input(prompt).strip()
        except (EOFError, StopIteration):
            raise _QuitSession()

    def _header(self) -> None:
        self._print("")
        if not self._shown_welcome:
            self._print(f"You've started the project {self.project_name}!")
            self._shown_welcome = True
        else:
            self._print(f"On project {self.project_name}.")
        self._print("")
        self._print(f"Selected Geometry: {self.selected or 'None'}")
        self._print("")

    def _menu(self, title: str, options: list[tuple[str, bool]]) -> int:
        """Print a numbered menu; disabled options are greyed out. Returns the
        chosen 1-based index, or 0 for back/quit."""
        self._print(title)
        for number, (label, enabled) in enumerate(options, start=1):
            suffix = "" if enabled else "  (greyed out since no selected geometry)"
            self._print(f"{number}. {label}{suffix}")
        self._print("")
        while True:
            choice = self._ask("Enter a command using the numbers (or q to quit): ")
            if choice.lower() in ("q", "quit", "exit"):
                return 0
            if choice.lower() in ("b", "back"):
                return 0
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                index = int(choice)
                if not options[index - 1][1]:
                    self._print("Please select geometry first.")
                    continue
                return index
            self._print("Please enter one of the listed numbers.")

    # -- codegen helpers --

    def _part_file(self, var_name: str) -> Path:
        return self.parts[var_name]["file"]

    def _append_line(self, var_name: str, line: str) -> None:
        path = self._part_file(var_name)
        path.write_text(path.read_text() + line + "\n")

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

    def _register_part(self, var_name: str, dim: str, file: Path) -> None:
        self.parts[var_name] = {"file": file, "dim": dim}
        self.selected = var_name
        self._write_project_file()

    def _write_project_file(self) -> None:
        lines = [f'"""CodeToCAD project {self.project_name}."""', ""]
        for var_name, info in self.parts.items():
            lines.append(f"from {info['file'].stem} import {var_name}")
        lines += [
            "",
            'if __name__ == "__main__":',
        ]
        if self.parts:
            joined = ", ".join(self.parts)
            lines += [
                f"    for _part in [{joined}]:",
                "        _part.build()",
            ]
        else:
            lines.append("    pass")
        (self.project_dir / f"{self.project_name}.py").write_text(
            "\n".join(lines) + "\n"
        )

    def _new_part_file(self, var_name: str, description: str | None, code: str) -> Path:
        path = self.project_dir / f"{var_name}.py"
        header = f'"""Part {var_name} generated by the CodeToCAD CLI."""\n'
        body = "import codetocad\n\n" + code
        if description:
            body += f"{var_name}.description = {description!r}\n"
        path.write_text(header + body)
        return path

    def _execute_project(self) -> None:
        """Run the selected part's file so declarative operations (such as
        export) take effect immediately."""
        if self.selected is None:
            return
        path = self._part_file(self.selected)
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
            runpy.run_path(str(path), run_name="__codetocad_cli__")
        except Exception as error:  # surface, don't crash the session
            self._print(f"Note: could not execute {path.name}: {error}")
        finally:
            os.chdir(old_cwd)
            sys.path.remove(str(self.project_dir))

    # -- menus --

    def run(self) -> None:
        try:
            while True:
                self._header()
                choice = self._menu(
                    "What do you want to do?",
                    [
                        ("Part", True),
                        ("Sketch", True),
                        ("Select geometry", True),
                        ("Export selected geometry", True),
                    ],
                )
                if choice == 0:
                    return
                if choice == 1:
                    self._part_menu()
                elif choice == 2:
                    self._sketch_menu()
                elif choice == 3:
                    self._select_geometry()
                elif choice == 4:
                    self._export_selected()
        except _QuitSession:
            return

    def _part_menu(self) -> None:
        self._header()
        has_selection = self.selected is not None
        choice = self._menu(
            "What do you want to do?",
            [
                ("Create a part", True),
                ("Define a location on selected part", has_selection),
                ("Transform selected part", has_selection),
                ("Boolean selected part", has_selection),
                ("Shell selected part", has_selection),
                ("Add a constraint with another part", has_selection),
            ],
        )
        if choice == 1:
            self._create_part()
        elif choice == 2:
            self._define_location()
        elif choice == 3:
            self._transform_selected()
        elif choice == 4:
            self._boolean_selected()
        elif choice == 5:
            self._shell_selected()
        elif choice == 6:
            self._constrain_selected()

    def _create_part(self) -> None:
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
                f"class {var_name.title().replace('_', '')}(codetocad.Part3D):\n"
                "    def build(self):\n"
                '        """User defined script to generate a shape here."""\n'
                "        ...\n"
                "\n"
                f"{var_name} = {var_name.title().replace('_', '')}(name={var_name!r})\n"
            )
        elif choice == 2:
            file_path = self._ask("Enter the path of the file to import: ")
            code = f"{var_name} = codetocad.import_file({file_path!r})\n"
            code += f"{var_name}.name = {var_name!r}\n"
        elif choice == 3:
            dims = self._ask_dimensions(
                "Enter length, width, height of the cube: ", 3
            )
            if dims is None:
                return
            code = (
                f"{var_name} = codetocad.cube("
                f"length={dims[0]!r}, width={dims[1]!r}, height={dims[2]!r})\n"
                f"{var_name}.name = {var_name!r}\n"
            )
        elif choice == 4:
            dims = self._ask_dimensions("Enter radius, height of the cylinder: ", 2)
            if dims is None:
                return
            code = (
                f"{var_name} = codetocad.cylinder("
                f"radius={dims[0]!r}, height={dims[1]!r})\n"
                f"{var_name}.name = {var_name!r}\n"
            )
        else:
            dims = self._ask_dimensions("Enter radius of the sphere: ", 1)
            if dims is None:
                return
            code = (
                f"{var_name} = codetocad.sphere(radius={dims[0]!r})\n"
                f"{var_name}.name = {var_name!r}\n"
            )
        path = self._new_part_file(var_name, description or None, code)
        self._register_part(var_name, "3d", path)

    def _sketch_menu(self) -> None:
        self._header()
        selected_is_2d = (
            self.selected is not None and self.parts[self.selected]["dim"] == "2d"
        )
        choice = self._menu(
            "What do you want to do?",
            [
                ("Create a sketch", True),
                ("Extrude selected sketch", selected_is_2d),
                ("Transform selected sketch", selected_is_2d),
                ("Add a constraint with another sketch", selected_is_2d),
            ],
        )
        if choice == 1:
            self._create_sketch()
        elif choice == 2:
            self._extrude_selected()
        elif choice == 3:
            self._transform_selected()
        elif choice == 4:
            self._constrain_selected()

    def _create_sketch(self) -> None:
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
            code = (
                f"{var_name} = codetocad.rectangle("
                f"width={dims[0]!r}, height={dims[1]!r})\n"
            )
        elif choice == 2:
            dims = self._ask_dimensions("Enter radius of the circle: ", 1)
            if dims is None:
                return
            code = f"{var_name} = codetocad.circle(radius={dims[0]!r})\n"
        else:
            content = self._ask("Enter the text: ")
            font = self._ask("Enter the font (leave blank for default): ") or "Arial"
            size = self._ask("Enter the text size: ")
            code = (
                f"{var_name} = codetocad.text("
                f"{content!r}, font={font!r}, size={size!r})\n"
            )
        code += f"{var_name}.name = {var_name!r}\n"
        path = self._new_part_file(var_name, description or None, code)
        self._register_part(var_name, "2d", path)

    def _ask_dimensions(self, prompt: str, count: int) -> list[str] | None:
        raw = self._ask(prompt)
        dims = [dim.strip() for dim in raw.split(",") if dim.strip()]
        if len(dims) != count:
            self._print(f"Expected {count} comma-separated value(s), got {len(dims)}.")
            return None
        return dims

    def _select_geometry(self) -> None:
        if not self.parts:
            self._print("There is no geometry yet. Create a part or sketch first.")
            return
        self._print("")
        options = [(var_name, True) for var_name in self.parts]
        choice = self._menu("Select geometry:", options)
        if choice:
            self.selected = list(self.parts)[choice - 1]

    def _export_selected(self) -> None:
        if self.selected is None:
            self._print("Please select geometry first.")
            return
        self._print("")
        default = f"{self.selected}.stl"
        destination = (
            self._ask(f"Enter an export file path (default {default}): ") or default
        )
        self._append_line(self.selected, f"{self.selected}.export({destination!r})")
        self._execute_project()
        self._print(f"Added export of {self.selected} to {destination}.")

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
            from .location import CubeLocations

            if member not in CubeLocations.__members__:
                self._print(f"Unknown cube location {raw!r}.")
                return
            line = (
                f"{var_name}_{location_name} = "
                f"codetocad.CubeLocations.{member}.to_location({var_name})"
            )
        self._append_line(var_name, line)
        self._print(f"Defined location {var_name}_{location_name}.")

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

    def _boolean_selected(self) -> None:
        operation_choice = self._menu(
            "Boolean operation:",
            [("Subtract", True), ("Union", True), ("Intersect", True)],
        )
        if operation_choice == 0:
            return
        other = self._choose_other_part()
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

    def _shell_selected(self) -> None:
        self._print("")
        thickness = self._ask("Enter a shell thickness: ")
        self._append_line(
            self.selected, f"{self.selected}.shell(thickness={thickness!r})"
        )
        self._print(f"Added shell to {self.selected}.")

    def _constrain_selected(self) -> None:
        is_2d = self.parts[self.selected]["dim"] == "2d"
        if is_2d:
            options = [("Coincide", True), ("Parallel", True), ("Perpendicular", True), ("Tangent", True)]
            methods = {1: "coincide", 2: "parallel", 3: "perpendicular", 4: "tangent"}
        else:
            options = [("Fixed", True), ("Revolute", True), ("Prismatic", True)]
            methods = {1: "fixed", 2: "revolute", 3: "prismatic"}
        constraint_choice = self._menu("Constraint type:", options)
        if constraint_choice == 0:
            return
        other = self._choose_other_part()
        if other is None:
            return
        method = methods[constraint_choice]
        self._ensure_part_import(self.selected, other)
        self._append_line(
            self.selected,
            f"{self.selected}.{method}(codetocad.Location(), {other}, "
            "codetocad.Location())",
        )
        self._print(f"Added {method} constraint between {self.selected} and {other}.")

    def _choose_other_part(self) -> str | None:
        others = [var_name for var_name in self.parts if var_name != self.selected]
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
        from . import __version__

        print(__version__)
        return 0
    if args[0] == "init":
        if len(args) < 2:
            print("Usage: codetocad init <project_name>")
            return 1
        name = _sanitize_identifier(args[1])
        project_dir = init_project(name)
        InteractiveSession(project_dir, name).run()
        return 0
    target = args[1] if args[0] == "run" and len(args) > 1 else args[0]
    run_script(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
