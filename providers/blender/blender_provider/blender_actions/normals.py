import mathutils


def project_vector_along_normal(translate_vector: list, normal_vector: list):
    """
    Projects a vector along a normal
    """
    # references https://stackoverflow.com/a/46979141
    vector = mathutils.Vector(translate_vector)
    normal = mathutils.Vector(normal_vector)
    # return translate_vector.dot(normal_vector) * normal_vector
    return vector.project(normal)
