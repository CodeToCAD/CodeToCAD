from CodeToCADBlenderProvider import *

Part("ball").createSphere(1).landmark("center","center,center,center").landmark("bottom","center,center,min")
Part("link").createCube(1,1,2).landmark("top","center,center,max").landmark("bottom","center,center,min")

Joint("ball", "link", "center","bottom").limitLocation(0,0,0).limitRotation(0,0,0)

Part("socket").createSphere(0.9).landmark("cutoff","center,center,min+0.2").landmark("center","center,center,center")

Joint("socket","ball","cutoff","bottom").transformLandmarkOntoAnother()

Part("socket").subtract("ball").apply()

Joint("socket","ball","center").limitRotation("-30d,30d","-30d,30d",0).pivot()