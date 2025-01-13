from codetocad.core.point import Point


def cross_product(v1, v2) -> Point:
    x = v1[1] * v2[2] - v1[2] * v2[1]
    y = v1[2] * v2[0] - v1[0] * v2[2]
    z = v1[0] * v2[1] - v1[1] * v2[0]
    return Point(x, y, z)


def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])


def calculate_normal(point1: Point, point2: Point, point3: Point):
    vector1 = subtract_vectors(point1.to_list(), point2.to_list())
    vector2 = subtract_vectors(point3.to_list(), point1.to_list())

    cross_product_result = cross_product(vector1, vector2)

    length = (
        cross_product_result[0] ** 2
        + cross_product_result[1] ** 2
        + cross_product_result[2] ** 2
    ) ** 0.5

    if length != 0:
        normalized = Point(
            cross_product_result[0] / length,
            cross_product_result[1] / length,
            cross_product_result[2] / length,
        )
    else:
        normalized = cross_product_result

    return normalized
