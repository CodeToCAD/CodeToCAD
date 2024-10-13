import mathutils


def calculate_normal(v0: mathutils.Vector, v1: mathutils.Vector, v2: mathutils.Vector):
    # References https://blenderartists.org/t/getting-face-normals-from-python/309648/4
    normal = (v0 - v1).to_3d().cross((v0 - v2).to_3d())
    normal.normalize()
    return normal.to_tuple()


def project_vector_along_normal(translate_vector: list, normal_vector: list):
    """
    Projects a vector along a normal
    """
    # references https://stackoverflow.com/a/46979141
    vector = mathutils.Vector(translate_vector)
    normal = mathutils.Vector(normal_vector)
    # return translate_vector.dot(normal_vector) * normal_vector
    return vector.project(normal)
