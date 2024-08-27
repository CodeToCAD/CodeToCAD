from codetocad import Sketch

circle = Sketch("cylinder").create_circle(0.5).extrude("2cm")

# new_circle = circle.clone("new_circle")

new_circle = circle.clone("new_circle2", "circ2")
