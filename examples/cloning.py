from codetocad import Sketch

circle = Sketch("circ").create_circle(0.5)

# new_circle = circle.clone("new_circle")

new_circle = circle.clone("new_circle2", "circ2")
