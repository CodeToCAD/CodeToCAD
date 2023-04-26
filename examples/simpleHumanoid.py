from CodeToCAD import *

# MARK: Create body
body = Part("body").createCube(1, 2, 3)
body_top = body.createLandmark("top", center, center, max)

# MARK: Create head
head = Part("head").createSphere(0.5)
head_bottom = head.createLandmark("bottom", center, center, min)

# Mark: Create Eye
eye = Part("eye").createCylinder(0.1, 0.1)
eye_bottom = eye.createLandmark("bottom", center, center, min)

eye.rotateXYZ(0, 90, 0)

# Mark: Attach head to Body
Joint(body_top, head_bottom).limitLocationXYZ(
    0, 0, 0).limitLocationY(-0.3, 0.3).limitRotationX(0, 0).limitRotationY(-20, 90).limitRotationZ(-30, 30)

# Mark: Attach eye to head:
head_leftEye = head.createLandmark("leftEye", "max-0.1", -0.2, "max/3")
Joint(head_leftEye, eye_bottom).limitLocationXYZ(
    0, 0, 0).limitRotationXYZ(0, 0, 0)

# Mark: mirror the eyes
eye.mirror("head", "y", None)
