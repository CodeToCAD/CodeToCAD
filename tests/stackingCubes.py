from CodeToCADBlenderProvider import *

Part("a").createCube(1,1,1).landmark("top","center,center,max").landmark("bottom","center,center,min")
Part("b").createCube(1,1,1).landmark("bottom","center,center,min")
Part("c").createCube(1,1,1).landmark("top","center,center,max")

# Joint("a","b","top","bottom").transformLandmarkOntoAnother()

Joint("a","b","top","bottom")\
    .limitLocation(0,0,0)\
    .limitRotation(0,0,0)
    
Joint("a","c","bottom","top")\
    .limitLocation(0,0,0)\
    .limitRotation(0,0,0)