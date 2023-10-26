from codetocad import *

# MARK: Create body
body = Part("body").create_cube(1, 2, 3)
body_top = body.create_landmark("top", center, center, max)

# MARK: Create head
head = Part("head").create_sphere(0.5)
head_bottom = head.create_landmark("bottom", center, center, min)

# Mark: Create Eye
eye = Part("eye").create_cylinder(0.1, 0.1)
eye_bottom = eye.create_landmark("bottom", center, center, min)

eye.rotate_xyz(0, 90, 0)

# Mark: Attach head to Body
Joint(body_top, head_bottom).limit_location_xyz(0, 0, 0).limit_location_y(
    -0.3, 0.3
).limit_rotation_x(0, 0).limit_rotation_y(-20, 90).limit_rotation_z(-30, 30)

# Mark: Attach eye to head:
head_leftEye = head.create_landmark("leftEye", "max-0.1", -0.2, "max/3")
Joint(head_leftEye, eye_bottom).limit_location_xyz(0, 0, 0).limit_rotation_xyz(0, 0, 0)

# Mark: mirror the eyes
eye.mirror("head", "y", None)
