import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))

def testPrimitive():
    import bpy
    from CodeToCADBlenderProvider import shape
    
    shape("primitiveTestCube") \
        .primitive("cube", "100mm,20cm,100mm")

testPrimitive()