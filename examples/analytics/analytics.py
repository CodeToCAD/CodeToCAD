from codetocad import Analytics, Part


analytics = Analytics()

my_cube = Part.create_cube(1, 1, 1)

dimensions = analytics.get_dimensions(my_cube)

# This will write logs inside the provider or to the console:
# you can also just do print() to print to the console.
analytics.log(f"Dimensions for myCube are: {dimensions}")
