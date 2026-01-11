
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.cad.shapes import Edge, Vertex


class Draw:
    """Common edge generation methods."""
    def __new__(cls, *args, **kwargs):
        raise TypeError("Do not instantiate a Draw class, use its methods instead.")
    
    @staticmethod
    def line(v1: Vertex, v2: Vertex) -> Edge:
        return Edge(v1=v1, v2=v2)
    
    @staticmethod
    def rectangle(center: Vertex, width: LengthType, height: LengthType) -> Edge:
        start_x = LengthExp(width) /2
        start_y = LengthExp(height) /2
        line1 = Draw.line(
            Vertex(
                x=center._x - start_x,
                y=center._y - start_y,
                z=center._z,
            ),
            Vertex(
                x=center._x +start_x,
                y=center._y - start_y,
                z=center._z,
            ),
        )
        line2 = Draw.line(
            line1.v2,
            Vertex(
                x=center._x + start_x,
                y=center._y + start_y,
                z=center._z,
            ),
        )
        line3 = Draw.line(
            line2.v2,
            Vertex(
                x=center._x - start_x,
                y=center._y + start_y,
                z=center._z,
            ),
        )
        line4 = Draw.line(
            line3.v2,
            line1.v1,
        )

        return Edge(v1=line1.v1, v2=line4.v2, sub_edges=[line1, line2, line3, line4])
