# Launchers

The CLI tool uses these launchers to figure out how to run CodeToCAD scripts.

For example, invoking the Blender launcher will automatically build and execute a path like:
```sh
blender myscene.blend --background -- --codetocad $(pwd)/yourScript.py
```

## Entrypoint

The entrypoint for the cli tool is [run.py](../run.py).