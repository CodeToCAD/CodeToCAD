from CodeToCADBlenderProvider import *

ball = Part("ball").createSphere(1)
ball_center = ball.createLandmark("center", center, center, center)
ball_bottom = ball.createLandmark("bottom", center, center, min)

link = Part("link").createCube(1,1,2)
link_top = link.createLandmark("top", center, center, max)
link_bottom = link.createLandmark("bottom",center, center, min)

Joint(ball, link, ball_center, link_bottom)\
    .limitLocation(0,0,0).limitRotation(0,0,0)

socket = Part("socket").createSphere(0.9)
socket_cutoff = socket.createLandmark("cutoff",center, center, "min + 0.2")
socket_center = socket.createLandmark("center", center, center, center)

Joint(socket, ball, socket_cutoff, ball_bottom).translateLandmarkOntoAnother()

socket.subtract("ball", deleteAfterSubtract=False, isTransferLandmarks=False)

Joint("socket","ball","center").limitRotation(-30,-30,0,30,30,0).pivot()