# Development & Contributing

## Setting up development environment.

1. Please install the VSCode python virtual environment using
   `sh development/create_python_virtual_environment.sh`
   or
   `sh development/create_python_virtual_environment.sh /path/to/python_binary`.

> If you are on Windows, please use Git Bash.
> Note: Python 3.10+ is required.
> Note 2: It might be a good idea to restart VSCode after installing the virtual environment.
> Note 3: If VSCode prompts you, please use the interpreter under `development/developmentVirtualEnvironment`.

2. It's good practice to run tests and linting before committing. Please run `sh ./development/install_git_hooks.sh` to instll Git Hooks.

3. Read the README for each provider for information on setting them up:
   - Blender: [providers/blender/README.md](../providers/blender/README.md)
   - Fusion360: [providers/fusion360/README.md](../providers/fusion360/README.md)
   - Onshape: [providers/onshape/README.md](../providers/onshape/README.md)

## Running Scripts

Run scripts using `sh development/{script_name}.sh`.

The following are the available scripts:

- [run_tests.sh](./run_tests.sh) - Executes tests using pyunittest.
- [run_lint.sh](./run_lint.sh) - Uses Flake8 to generate a lint report of the project. Use the --autofix flag to fix link and formatting.
- [create_blender_addon.sh](./create_blender_addon.sh) - Generates the BlenderAddon zip file
- [create_python_virtual_environment.sh](./create_python_virtual_environment.sh) - Creates a pyenv on your local machine and installs development related packages.
- [pip_package_create.sh](./pip_package_create.sh) - Builds a python package using setup.py.
- [pip_package_upload.sh](./pip_package_upload.sh) - Builds a python package and uploads it to pypi using twine. You will need a `.pypirc` file in the root directory for this to work.


## Nightly/dev builds

We don't currently automatically release a nightly/dev build. However, here are some instructions on generating release files:

- pypi python release: run the [pip_package_create.sh](./pip_package_create.sh) script
- Blender Addon zip file: run the [create_blender_addon.sh](./create_blender_addon.sh) script

## Capabilities.json and Jinja2 templates

[CodeToCAD/capabilities.json](./CodeToCAD/capabilities.json) is a schema used to generate the [CodeToCAD interfaces](./CodeToCAD/interfaces/).

Jinja2 templates are used to turn capabilities.json into an interface, as well as templates for CodeToCAD Providers and Tests.

You can generate the Jinja2 templates by running the "Capabilities.json to Python" task in VSCode, or `sh development/capabilities_json_to_python/capabilities_to_py.sh`

## Architecture

CodeToCAD is an automation. Here is the high-level architecture for this tool.

![Architecture](https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/develop/docs/CodeToCAD%20architecture%20overview.drawio.png)

## Contributing

If you would like to contribute to the project, please feel free to submit a PR.

Please join the Discord Server if you have any questions or suggestions: [https://discord.gg/MnZEtqwt74](https://discord.gg/MnZEtqwt74)