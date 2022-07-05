from CodeToCADBlenderProvider import *

Part("a").createCube(1,1,1).landmark("top","center,center,max")
Part("b").createCube(1,1,1).landmark("bottom","center,center,min")

Joint("a","b","top","bottom").transformLandmarkOntoAnother()