from typing import List

from codetocad.core.point import Point


def clip_points_roi(
    points_to_clip: List[Point],
    min_point: Point,
    max_point: Point,
    is_flip: bool = False,
) -> List[Point]:
    """
    Given a list of points, return the points bounded by the region of interest.

    NOTE: The order of items in the list may get changed, so do not use this function if you care about the original sorting of the list.
    """

    clipped_points = []
    clipped_points_flipped = []

    for point in points_to_clip:
        if (point >= min_point) and (point <= max_point):
            clipped_points.append(point)
        else:
            clipped_points_flipped.append(point)

    clipped_points = clipped_points if not is_flip else clipped_points_flipped

    return clipped_points


def clip_spline_points(
    points_to_clip: List[Point],
    point1: Point,
    point2: Point,
    is_flip: bool = False,
    is_include_points: bool = True,
) -> List[Point]:
    """
    Given a list of connected 2D spline points, return the points bounded by two points tangent to the spline.

    If is_include_points flag is True, point1 and point2 will be inserted where the clipping occurs.
    """

    min_point1_distance = float("inf")
    min_point2_distance = float("inf")

    min_point1_index = None
    min_point2_index = None

    for index, point in enumerate(points_to_clip):
        point1_distance = point.distance_to(point1)
        point2_distance = point.distance_to(point2)

        if point1_distance <= min_point1_distance:
            min_point1_distance = point1_distance
            min_point1_index = index

        if point2_distance <= min_point2_distance:
            min_point2_distance = point2_distance
            min_point2_index = index

    min_point = point1
    max_point = point2

    if (min_point1_index or min_point2_index or 0) > (
        min_point2_index or min_point1_index or 0
    ):
        min_point = point2
        max_point = point1

    end_index = len(points_to_clip) - 1
    min_index = min(
        min_point1_index or min_point2_index or 0,
        min_point2_index or min_point1_index or 0,
    )
    max_index = max(
        min_point1_index or min_point2_index or end_index,
        min_point2_index or min_point1_index or end_index,
    )

    clipped_points = points_to_clip[min_index:max_index]

    if is_flip:
        clipped_points = points_to_clip[0:min_index] + points_to_clip[max_index:]

    if is_include_points and is_flip:
        min_index_point = clipped_points[min_index]
        min_index_plus_1_point = clipped_points[min_index + 1]

        if not min_point.is_touching(min_index_point):
            clipped_points.insert(min_index, min_point)
        if not max_point.is_touching(min_index_plus_1_point):
            clipped_points.insert(min_index + 1, max_point)

    elif is_include_points:
        if not min_point.is_touching(clipped_points[0]):
            clipped_points.insert(0, min_point)
        if not max_point.is_touching(clipped_points[-1]):
            clipped_points.append(max_point)

    return clipped_points
