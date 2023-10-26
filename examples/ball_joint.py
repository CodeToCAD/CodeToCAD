from codetocad import *

ball = Part("ball").create_sphere(1)
ball_center = ball.create_landmark("center", center, center, center)
ball_bottom = ball.create_landmark("bottom", center, center, min)

link = Part("link").create_cube(1, 1, 2)
link_top = link.create_landmark("top", center, center, max)
link_bottom = link.create_landmark("bottom", center, center, min)

Joint(ball_center, link_bottom).limit_location_xyz(0, 0, 0).limit_rotation_xyz(0, 0, 0)

socket = Part("socket").create_sphere(1.2)
socket_cutoff = socket.create_landmark("cutoff", center, center, "min + 0.7")
socket_center = socket.create_landmark("center", center, center, center)

Joint(ball_bottom, socket_cutoff).translate_landmark_onto_another()

socket.subtract(ball, delete_after_subtract=False, is_transfer_landmarks=False)

Joint(socket_center, ball).limit_rotation_x(-30, 30).limit_rotation_y(
    -30, 30
).limit_rotation_z(0, 0)


blue_material = Material("blue").set_color(0.0826006, 0.214978, 0.406714, 1.0)
green_material = Material("socket").set_color(0.249275, 0.709804, 0.392972, 0.8)
ball.set_material(blue_material)
link.set_material(blue_material)
socket.set_material(green_material)
