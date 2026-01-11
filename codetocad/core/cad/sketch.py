import math

from codetocad.core.dimensions.angle import Angle, AngleType
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.cad.shapes import CurveType, Edge, Vertex


class Draw:
    """Common edge generation methods."""

    def __new__(cls, *args, **kwargs):
        raise TypeError("Do not instantiate a Draw class, use its methods instead.")

    @staticmethod
    def line(v1: Vertex, v2: Vertex) -> Edge:
        """Create a straight line between two vertices."""
        return Edge(v1=v1, v2=v2)

    @staticmethod
    def rectangle(center: Vertex, width: LengthType, height: LengthType) -> Edge:
        """Create a rectangle centered at the given vertex."""
        start_x = LengthExp(width) / 2
        start_y = LengthExp(height) / 2
        line1 = Draw.line(
            Vertex(x=center._x - start_x, y=center._y - start_y, z=center._z),
            Vertex(x=center._x + start_x, y=center._y - start_y, z=center._z),
        )
        line2 = Draw.line(
            line1.v2,
            Vertex(x=center._x + start_x, y=center._y + start_y, z=center._z),
        )
        line3 = Draw.line(
            line2.v2,
            Vertex(x=center._x - start_x, y=center._y + start_y, z=center._z),
        )
        line4 = Draw.line(line3.v2, line1.v1)

        return Edge(v1=line1.v1, v2=line4.v2, sub_edges=[line1, line2, line3, line4])

    @staticmethod
    def polygon(
        center: Vertex, radius: LengthType, sides: int, rotation: AngleType = 0
    ) -> Edge:
        """Create a regular polygon with the given number of sides."""
        if sides < 3:
            raise ValueError("Polygon must have at least 3 sides")

        r = LengthExp(radius)
        rot = Angle(rotation).value
        angle_step = 2 * math.pi / sides

        vertices: list[Vertex] = []
        for i in range(sides):
            angle = rot + i * angle_step
            vertices.append(
                Vertex(
                    x=center._x + r * math.cos(angle),
                    y=center._y + r * math.sin(angle),
                    z=center._z,
                )
            )

        edges: list[Edge] = []
        for i in range(sides):
            edges.append(Draw.line(vertices[i], vertices[(i + 1) % sides]))

        return Edge(v1=vertices[0], v2=vertices[0], sub_edges=edges)

    @staticmethod
    def _bezier_arc_segment(
        center: Vertex,
        radius: LengthExp,
        start_angle: float,
        end_angle: float,
    ) -> Edge:
        """Create a single Bezier arc segment (max 90°)."""
        sweep = end_angle - start_angle
        if abs(sweep) > math.pi / 2 + 1e-9:
            raise ValueError("Bezier arc segment cannot exceed 90°")

        cos_start, sin_start = math.cos(start_angle), math.sin(start_angle)
        cos_end, sin_end = math.cos(end_angle), math.sin(end_angle)

        # Start and end points on the arc
        v1 = Vertex(
            x=center._x + radius * cos_start,
            y=center._y + radius * sin_start,
            z=center._z,
        )
        v2 = Vertex(
            x=center._x + radius * cos_end,
            y=center._y + radius * sin_end,
            z=center._z,
        )

        # Control point: intersection of tangent lines at start and end
        # For a circular arc, the control point lies along the angle bisector
        half_sweep = sweep / 2
        mid_angle = start_angle + half_sweep
        # Distance from center to control point for exact circular arc
        control_dist = radius.value / math.cos(half_sweep)

        control_point = Vertex(
            x=center._x.value + control_dist * math.cos(mid_angle),
            y=center._y.value + control_dist * math.sin(mid_angle),
            z=center._z.value,
        )

        # Weight for rational quadratic Bezier
        weight = math.cos(half_sweep)

        v1.handle_out = control_point
        v2.handle_in = control_point
        v2.weight = weight

        return Edge(v1=v1, v2=v2)

    @staticmethod
    def _nurbs_arc_segment(
        center: Vertex,
        radius: LengthExp,
        start_angle: float,
        end_angle: float,
    ) -> Edge:
        """Create a single NURBS arc segment (max 90°)."""
        sweep = end_angle - start_angle
        if abs(sweep) > math.pi / 2 + 1e-9:
            raise ValueError("NURBS arc segment cannot exceed 90°")

        cos_start, sin_start = math.cos(start_angle), math.sin(start_angle)
        cos_end, sin_end = math.cos(end_angle), math.sin(end_angle)

        v1 = Vertex(
            x=center._x + radius * cos_start,
            y=center._y + radius * sin_start,
            z=center._z,
            weight=1.0,
        )
        v2 = Vertex(
            x=center._x + radius * cos_end,
            y=center._y + radius * sin_end,
            z=center._z,
            weight=1.0,
        )

        # Control point for NURBS (same geometry as Bezier)
        half_sweep = sweep / 2
        mid_angle = start_angle + half_sweep
        control_dist = radius.value / math.cos(half_sweep)

        control_point = Vertex(
            x=center._x.value + control_dist * math.cos(mid_angle),
            y=center._y.value + control_dist * math.sin(mid_angle),
            z=center._z.value,
        )

        v1.handle_out = control_point
        v2.handle_in = control_point
        v2.weight = math.cos(half_sweep)

        # NURBS knot vector for degree 2 with 3 control points
        knots = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]

        return Edge(v1=v1, v2=v2, knots=knots)

    @staticmethod
    def arc(
        center: Vertex,
        radius: LengthType,
        start_angle: AngleType,
        end_angle: AngleType,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create an arc from center point with start and end angles."""
        r = LengthExp(radius)
        start_rad = Angle(start_angle).value
        end_rad = Angle(end_angle).value

        # Normalize sweep to be positive
        sweep = end_rad - start_rad
        if sweep < 0:
            sweep += 2 * math.pi

        # Split into segments of max 90°
        num_segments = max(1, math.ceil(sweep / (math.pi / 2)))
        segment_sweep = sweep / num_segments

        arc_func = (
            Draw._bezier_arc_segment
            if curve_type == CurveType.BEZIER
            else Draw._nurbs_arc_segment
        )

        segments: list[Edge] = []
        for i in range(num_segments):
            seg_start = start_rad + i * segment_sweep
            seg_end = seg_start + segment_sweep
            segments.append(arc_func(center, r, seg_start, seg_end))

        if len(segments) == 1:
            return segments[0]

        return Edge(v1=segments[0].v1, v2=segments[-1].v2, sub_edges=segments)

    @staticmethod
    def arc_3point(
        start: Vertex,
        mid: Vertex,
        end: Vertex,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create an arc passing through three points."""
        # Calculate the center and radius from three points
        # Using circumcenter formula
        ax, ay = start._x.value, start._y.value
        bx, by = mid._x.value, mid._y.value
        cx, cy = end._x.value, end._y.value

        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-10:
            raise ValueError("Points are collinear, cannot form an arc")

        ux = (
            (ax * ax + ay * ay) * (by - cy)
            + (bx * bx + by * by) * (cy - ay)
            + (cx * cx + cy * cy) * (ay - by)
        ) / d
        uy = (
            (ax * ax + ay * ay) * (cx - bx)
            + (bx * bx + by * by) * (ax - cx)
            + (cx * cx + cy * cy) * (bx - ax)
        ) / d

        center = Vertex(x=ux, y=uy, z=start._z.value)
        radius = math.sqrt((ax - ux) ** 2 + (ay - uy) ** 2)

        # Calculate angles
        start_angle = math.atan2(ay - uy, ax - ux)
        mid_angle = math.atan2(by - uy, bx - ux)
        end_angle = math.atan2(cy - uy, cx - ux)

        # Determine arc direction based on mid point
        def normalize_angle(a: float) -> float:
            while a < 0:
                a += 2 * math.pi
            while a >= 2 * math.pi:
                a -= 2 * math.pi
            return a

        start_angle = normalize_angle(start_angle)
        mid_angle = normalize_angle(mid_angle)
        end_angle = normalize_angle(end_angle)

        # Check if mid is between start and end going counterclockwise
        def is_between_ccw(start: float, mid: float, end: float) -> bool:
            if start <= end:
                return start <= mid <= end
            return mid >= start or mid <= end

        if not is_between_ccw(start_angle, mid_angle, end_angle):
            # Go the other way
            start_angle, end_angle = end_angle, start_angle

        return Draw.arc(center, radius, start_angle, end_angle, curve_type)

    @staticmethod
    def circle(
        center: Vertex,
        radius: LengthType,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create a full circle."""
        return Draw.arc(center, radius, 0, "360deg", curve_type)

    @staticmethod
    def spline(
        points: "list[Vertex]",
        closed: bool = False,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create a smooth spline through the given points."""
        if len(points) < 2:
            raise ValueError("Spline requires at least 2 points")

        if closed and points[0] != points[-1]:
            points = points + [points[0]]

        n = len(points)

        if curve_type == CurveType.BEZIER:
            # Catmull-Rom style: compute tangents and convert to Bezier handles
            segments: list[Edge] = []

            for i in range(n - 1):
                p0 = points[max(0, i - 1)]
                p1 = points[i]
                p2 = points[i + 1]
                p3 = points[min(n - 1, i + 2)]

                # Tangent at p1 (scaled for cubic Bezier)
                t1_x = (p2._x.value - p0._x.value) / 6
                t1_y = (p2._y.value - p0._y.value) / 6
                t1_z = (p2._z.value - p0._z.value) / 6

                # Tangent at p2
                t2_x = (p3._x.value - p1._x.value) / 6
                t2_y = (p3._y.value - p1._y.value) / 6
                t2_z = (p3._z.value - p1._z.value) / 6

                v1 = Vertex(
                    x=p1._x.value,
                    y=p1._y.value,
                    z=p1._z.value,
                    handle_out=Vertex(
                        x=p1._x.value + t1_x,
                        y=p1._y.value + t1_y,
                        z=p1._z.value + t1_z,
                    ),
                )
                v2 = Vertex(
                    x=p2._x.value,
                    y=p2._y.value,
                    z=p2._z.value,
                    handle_in=Vertex(
                        x=p2._x.value - t2_x,
                        y=p2._y.value - t2_y,
                        z=p2._z.value - t2_z,
                    ),
                )
                segments.append(Edge(v1=v1, v2=v2))

            if len(segments) == 1:
                return segments[0]
            return Edge(v1=segments[0].v1, v2=segments[-1].v2, sub_edges=segments)

        else:  # NURBS
            # Create a cubic NURBS curve through points
            # Using uniform knot vector with interpolation
            degree = 3
            n_ctrl = n
            n_knots = n_ctrl + degree + 1

            # Uniform knot vector with clamped ends
            knots: list[float] = []
            for i in range(n_knots):
                if i < degree + 1:
                    knots.append(0.0)
                elif i >= n_knots - degree - 1:
                    knots.append(1.0)
                else:
                    knots.append((i - degree) / (n_ctrl - degree))

            # For simplicity, use points directly as control points with unit weights
            # (This is an approximating spline, not interpolating)
            vertices = [
                Vertex(x=p._x.value, y=p._y.value, z=p._z.value, weight=1.0)
                for p in points
            ]

            if n == 2:
                return Edge(v1=vertices[0], v2=vertices[1], knots=knots)

            # Build sub-edges for each segment
            segments = []
            for i in range(n - 1):
                segments.append(Edge(v1=vertices[i], v2=vertices[i + 1], knots=knots))

            return Edge(v1=vertices[0], v2=vertices[-1], sub_edges=segments, knots=knots)
