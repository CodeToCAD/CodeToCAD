"""
Cardinal directions for 3D geometry selection.

This module defines an enumeration for selecting points on 3D objects based on
cardinal directions. The coordinate system follows the standard right-handed
convention used in most CAD systems:

    - +X: Right
    - -X: Left
    - +Y: Front
    - -Y: Back
    - +Z: Up (Top)
    - -Z: Down (Bottom)

When viewing from the standard orientation (looking at the front face of an object):
    - "Front" is the face closest to the viewer (+Y direction)
    - "Back" is the face away from the viewer (-Y direction)
    - "Left" is the face on the viewer's left side (-X direction)
    - "Right" is the face on the viewer's right side (+X direction)
    - "Top" is the upper face (+Z direction)
    - "Bottom" is the lower face (-Z direction)

Each cardinal direction represents a point on or within the object's bounding box.
"""

from enum import Enum, auto

from codetocad.core.dimensions.length_expression import LengthExp, LengthType


class CardinalDirection(Enum):
    """
    Cardinal directions for selecting points on 3D geometry.

    The directions are organized by face/region of a bounding box:

    Top face (XY plane at +Z):
        TOP_CENTER, TOP_LEFT, TOP_RIGHT, TOP_FRONT, TOP_BACK,
        TOP_FRONT_LEFT, TOP_FRONT_RIGHT, TOP_BACK_LEFT, TOP_BACK_RIGHT

    Bottom face (XY plane at -Z):
        BOTTOM_CENTER, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM_FRONT, BOTTOM_BACK,
        BOTTOM_FRONT_LEFT, BOTTOM_FRONT_RIGHT, BOTTOM_BACK_LEFT, BOTTOM_BACK_RIGHT

    Front face (XZ plane at +Y):
        FRONT_CENTER, FRONT_LEFT, FRONT_RIGHT, FRONT_TOP, FRONT_BOTTOM
        (corners are covered by TOP/BOTTOM variants)

    Back face (XZ plane at -Y):
        BACK_CENTER, BACK_LEFT, BACK_RIGHT, BACK_TOP, BACK_BOTTOM

    Left face (YZ plane at -X):
        LEFT_CENTER, LEFT_FRONT, LEFT_BACK, LEFT_TOP, LEFT_BOTTOM

    Right face (YZ plane at +X):
        RIGHT_CENTER, RIGHT_FRONT, RIGHT_BACK, RIGHT_TOP, RIGHT_BOTTOM

    Special:
        CENTER - Center of the entire object's bounding box
    """

    # Center of the object
    CENTER = auto()

    # Top face (XY plane at +Z)
    TOP_CENTER = auto()
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    TOP_FRONT = auto()
    TOP_BACK = auto()
    TOP_FRONT_LEFT = auto()
    TOP_FRONT_RIGHT = auto()
    TOP_BACK_LEFT = auto()
    TOP_BACK_RIGHT = auto()

    # Bottom face (XY plane at -Z)
    BOTTOM_CENTER = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_FRONT = auto()
    BOTTOM_BACK = auto()
    BOTTOM_FRONT_LEFT = auto()
    BOTTOM_FRONT_RIGHT = auto()
    BOTTOM_BACK_LEFT = auto()
    BOTTOM_BACK_RIGHT = auto()

    # Front face (XZ plane at +Y) - edges only, corners covered by TOP/BOTTOM
    FRONT_CENTER = auto()
    FRONT_LEFT = auto()
    FRONT_RIGHT = auto()
    FRONT_TOP = auto()
    FRONT_BOTTOM = auto()

    # Back face (XZ plane at -Y) - edges only, corners covered by TOP/BOTTOM
    BACK_CENTER = auto()
    BACK_LEFT = auto()
    BACK_RIGHT = auto()
    BACK_TOP = auto()
    BACK_BOTTOM = auto()

    # Left face (YZ plane at -X) - edges only, corners covered by TOP/BOTTOM/FRONT/BACK
    LEFT_CENTER = auto()
    LEFT_FRONT = auto()
    LEFT_BACK = auto()
    LEFT_TOP = auto()
    LEFT_BOTTOM = auto()

    # Right face (YZ plane at +X) - edges only, corners covered by TOP/BOTTOM/FRONT/BACK
    RIGHT_CENTER = auto()
    RIGHT_FRONT = auto()
    RIGHT_BACK = auto()
    RIGHT_TOP = auto()
    RIGHT_BOTTOM = auto()

    @classmethod
    def from_string(cls, value: str) -> "CardinalDirection":
        """
        Create a CardinalDirection from a string representation.

        This method normalizes the input by converting to uppercase and removing
        underscores, spaces, and hyphens, allowing flexible input formats.

        Args:
            value: A string representing a cardinal direction. Accepts various formats:
                - Snake case: "top_left", "TOP_LEFT", "Top_Left"
                - No separators: "topleft", "TOPLEFT", "TopLeft"
                - With spaces: "top left", "TOP LEFT"
                - With hyphens: "top-left", "TOP-LEFT"

        Returns:
            The matching CardinalDirection enum instance.

        Raises:
            ValueError: If the string doesn't match any cardinal direction.

        Examples:
            >>> CardinalDirection.from_string("top_left")
            <CardinalDirection.TOP_LEFT: 3>
            >>> CardinalDirection.from_string("TOPLEFT")
            <CardinalDirection.TOP_LEFT: 3>
            >>> CardinalDirection.from_string("Top-Front-Right")
            <CardinalDirection.TOP_FRONT_RIGHT: 8>
            >>> CardinalDirection.from_string("center")
            <CardinalDirection.CENTER: 1>
        """
        # Normalize input: uppercase, remove separators
        normalized = value.upper().replace("_", "").replace(" ", "").replace("-", "")

        # Try to match against normalized enum member names
        for member in cls:
            member_normalized = member.name.replace("_", "")
            if normalized == member_normalized:
                return member

        # No match found - raise helpful error
        valid_options = [m.name for m in cls]
        raise ValueError(
            f"'{value}' is not a valid CardinalDirection. "
            f"Valid options are: {', '.join(valid_options)}"
        )


def offset(cardinal: CardinalDirection, distance: LengthType) -> str:
    """
    Create a string descriptor for an offset position from a cardinal point.

    This is useful for describing positions that are offset from a cardinal
    direction by a specific distance.

    Args:
        cardinal: The cardinal direction to offset from.
        distance: The distance to offset (accepts any LengthType: str, float, int, LengthExp).

    Returns:
        A string in the format "{cardinal_name}+{distance}" that can be parsed
        by position-aware functions.

    Examples:
        >>> offset(CardinalDirection.TOP_LEFT, "5mm")
        'TOP_LEFT+5mm'
        >>> offset(CardinalDirection.CENTER, 0.01)
        'CENTER+0.01'
        >>> offset(CardinalDirection.BOTTOM_FRONT, "2in + 1cm")
        'BOTTOM_FRONT+2in + 1cm'
    """
    # Convert distance to string representation
    if isinstance(distance, LengthExp):
        # Use the meter value for LengthExp objects
        distance_str = str(distance.value)
    else:
        distance_str = str(distance)

    return f"{cardinal.name}+{distance_str}"
