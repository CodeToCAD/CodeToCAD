def testPrimitive():
    import bpy
    from CodeToCADBlenderProvider import shape
    
    shape("primitiveTestCube") \
        .primitive("cube", "100mm,20cm,100mm")

testPrimitive()