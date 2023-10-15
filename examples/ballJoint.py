from codetocad import *

ball = Part("ball").createSphere(1)
ball_center = ball.createLandmark("center", center, center, center)
ball_bottom = ball.createLandmark("bottom", center, center, min)

link = Part("link").createCube(1, 1, 2)
link_top = link.createLandmark("top", center, center, max)
link_bottom = link.createLandmark("bottom", center, center, min)

Joint(ball_center, link_bottom)\
    .limitLocationXYZ(0, 0, 0).limitRotationXYZ(0, 0, 0)

socket = Part("socket").createSphere(1.2)
socket_cutoff = socket.createLandmark("cutoff", center, center, "min + 0.7")
socket_center = socket.createLandmark("center", center, center, center)

Joint(ball_bottom, socket_cutoff).translateLandmarkOntoAnother()

socket.subtract(ball, deleteAfterSubtract=False,
                isTransferLandmarks=False)

Joint(socket_center, ball) \
    .limitRotationX(-30, 30) \
    .limitRotationY(-30, 30) \
    .limitRotationZ(0, 0)


blueMaterial = Material("blue").setColor(0.0826006, 0.214978, 0.406714, 1.0)
greenMaterial = Material("socket").setColor(0.249275, 0.709804, 0.392972, 0.8)
ball.setMaterial(blueMaterial)
link.setMaterial(blueMaterial)
socket.setMaterial(greenMaterial)
