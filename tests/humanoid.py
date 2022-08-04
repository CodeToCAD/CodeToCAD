from CodeToCADBlenderProvider import *

# MARK: Create body
Part("body").createCube(1,2,3)
Part("body").landmark("top", "center,center,max")

# MARK: Create head
Part("head").createSphere(0.5)
Part("head").landmark("bottom","center,center,min")

# Mark: Create Eye
Part("eye").createCylinder(0.1,0.1).landmark("bottom","center,center,min").rotate("0,90d,0")

# Mark: Attach head to Body
Joint("body","head","top","bottom").limitLocation(0,"-0.3,0.3",0).limitRotation(0,"-20d,90d","-30d,30d")

# Mark: Attach eye to head:
Part("head").landmark("leftEye","max-0.1,-0.2,max/3")
Joint("head","eye","leftEye","bottom").limitLocation(0,0,0).limitRotation(0,0,0)

#Mark: mirror the eyes
Part("eye").mirror("head",(False,True,False))