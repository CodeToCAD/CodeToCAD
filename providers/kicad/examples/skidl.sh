!/bin/bash

set -e

# clone the repo if no exist
# git clone https://github.com/devbisme/skidl
cd skidl/tests/examples/stm32_usb_buck
# create dev env 
# python -m venv dev_env
source dev_env/bin/activate
cd ../../.. && pip install -e .
python tests/examples/stm32_usb_buck/main.py

# python tests/examples/stm32_usb_buck/main.py 
# WARNING: KICAD_SYMBOL_DIR environment variable is missing, so the default KiCad symbol libraries won't be searched. @ [/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/<frozen importlib._bootstrap_external>:940=>/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/<frozen importlib._bootstrap>:241]
# WARNING: Could not load KiCad schematic library "MCU_ST_STM32F4", falling back to backup library. @ [/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/tests/examples/stm32_usb_buck/main.py:18]
# Traceback (most recent call last):
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/tests/examples/stm32_usb_buck/main.py", line 18, in <module>
#     stm32.stm32f405r()
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/src/skidl/group.py", line 75, in sub_f
#     results = f(*args, **kwargs)
#               ^^^^^^^^^^^^^^^^^^
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/tests/examples/stm32_usb_buck/stm32_circuit.py", line 11, in stm32f405r
#     u = Part("MCU_ST_STM32F4", "STM32F405RGTx", footprint="LQFP-64_10x10mm_P0.5mm")
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/src/skidl/part.py", line 201, in __init__
#     raise e
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/src/skidl/part.py", line 191, in __init__
#     lib = SchLib(filename=libname, tool=tool)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/src/skidl/schlib.py", line 88, in __init__
#     tool_modules[tool].load_sch_lib(
#   File "/Users/patrickwilkie/Documents/Work/30.14 codetocad_bounty/CodeToCAD/providers/kicad/examples/skidl/src/skidl/tools/kicad/kicad.py", line 87, in load_sch_lib
#     raise FileNotFoundError(
# FileNotFoundError: Unable to open KiCad Schematic Library File MCU_ST_STM32F4