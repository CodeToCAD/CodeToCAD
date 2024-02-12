# Generating CodeToCAD interface and sample files (CodeGen)

CodeToCAD interface and sample files are auto-generated from `capabilities.json` and JINJA2 templates.

- [paths.py](./paths.py) defines the locations of the templates to generate.
- [capabilities_parse](./capabilities_parser.py) parses a capabilities.json document to extract meaningful dataclasses.
- [capabilities_to_py.py](./capabilities_to_py.py) is the entry point to load `capabilities.json` and fire off the templating automation.
