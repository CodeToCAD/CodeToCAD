# CodeToCAD Core

The Core module contains the interface (non-implementation) details and enumerations of CodeToCAD, as well as generic utilities.

## Capabilities

[capabilities.json](./capabilities.json) contains all the "actions" that CodeToCAD is expected to perform.

### Code-generation from capabilities.json using JINJA2

[CodeToCADInterface.py](./CodeToCADInterface.py) and [CodeToCADProvider.py](./CodeToCADProvider.py) are auto-generated using Jinja2 templates.

To generate those files, please run `sh capabilitiesToPyInterface.sh` and `sh capabilitiesToPyProvider.sh` respectively.

#### Python Code Auto-Generation explanation:

Nesting in capabilities.json is formatted like this:
    className > methods > properties > parameters/information > definitions

E.g.:
    "Part": => className
        "information": => a method
            "Capabilities related to...",
        "constructor": { => a method
            "parameters": => a property
                {"name": => a parameter
                    {"type": "string"} => a definition
                },
        },
        "fromFile": { => a method
            "information": => a property
                "Create a shape from a file.",
            "parameters": => a property
                {"filePath": => a parameter
                    {"type": "string"}, => a definition
                "fileType": => a parameter
                    {"type": "string", "required": false} => a definition
                }
        }

The jinja2 templates reference this structure to build python classes and methods.