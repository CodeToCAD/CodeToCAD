import bpy

from enum import Enum
from codetocad.codetocad_types import *


class BlenderTypes(Enum):
    OBJECT = bpy.types.Object
    MESH = bpy.types.Mesh
    CURVE = bpy.types.Curve
    TEXT = bpy.types.TextCurve
    POINT = bpy.types.SplinePoint | bpy.types.BezierSplinePoint


class BlenderObjectTypes(Enum):
    # References https://docs.blender.org/api/current/bpy_types_enum_items/object_type_items.html#rna-enum-object-type-items
    MESH = "MESH"
    EMPTY = "EMPTY"
    CURVE = "CURVE"
    LIGHT = "LIGHT"
    CAMERA = "CAMERA"
    FONT = "FONT"  # aka TEXT


class BlenderVersions(Enum):
    TWO_DOT_EIGHTY = (2, 80, 0)
    THREE_DOT_ONE = (3, 1, 0)

    @property
    def version(self):
        return ".".join([str(ver) for ver in self.value])


class BlenderLength(Units):
    # These are the units allowed in a Blender document:
    # metric
    KILOMETERS = LengthUnit.km
    METERS = LengthUnit.m
    CENTIMETERS = LengthUnit.cm
    MILLIMETERS = LengthUnit.mm
    MICROMETERS = LengthUnit.μm
    # imperial
    MILES = LengthUnit.mi
    FEET = LengthUnit.ft
    INCHES = LengthUnit.inch
    THOU = LengthUnit.thou

    # Blender internally uses this unit for everything:
    DEFAULT_BLENDER_UNIT = METERS

    def get_system(self):
        if (
            self == self.KILOMETERS
            or self == self.METERS
            or self == self.CENTIMETERS
            or self == self.MILLIMETERS
            or self == self.MICROMETERS
        ):
            return "METRIC"
        else:
            return "IMPERIAL"

    # Convert a utilities LengthUnit to BlenderLength

    @staticmethod
    def from_length_unit(unit: LengthUnit) -> "BlenderLength":
        [result] = list(filter(lambda b: b.value == unit, [b for b in BlenderLength]))

        return result

    # Takes in a list of Dimension and converts them to the `DEFAULT_BLENDER_UNIT`, which is the unit blender deals with, no matter what we set the document unit to.
    @staticmethod
    def convert_dimensions_to_blender_unit(
        dimensions: list[Dimension],
    ) -> list[Dimension]:
        return [
            (
                BlenderLength.convert_dimension_to_blender_unit(dimension)
                if (
                    dimension.value is not None
                    and dimension.unit is not None
                    and dimension.unit != BlenderLength.DEFAULT_BLENDER_UNIT.value
                )
                else dimension
            )
            for dimension in dimensions
        ]

    # Takes in a Dimension object, converts it to the default blender unit, and returns a Dimension object.
    @staticmethod
    def convert_dimension_to_blender_unit(dimension: Dimension):
        if (
            dimension.value is None
            or dimension.unit == BlenderLength.DEFAULT_BLENDER_UNIT.value
        ):
            return dimension
        if dimension.unit is None:
            dimension.unit = BlenderLength.DEFAULT_BLENDER_UNIT.value
            return dimension
        return dimension.convert_to_unit(BlenderLength.DEFAULT_BLENDER_UNIT.value)


# These are the rotation transformations supported by Blender:
class BlenderRotationTypes(Enum):
    EULER = "rotation_euler"
    DELTA_EULER = "delta_rotation_euler"
    QUATERNION = "rotation_quaternion"
    DELTA_QUATERNION = "delta_rotation_quaternion"


# These are the translation transformations supported by Blender:
class BlenderTranslationTypes(Enum):
    ABSOLUTE = "location"
    RELATIVE = "delta_location"


# Blender Modifiers we have implemented:
class BlenderBooleanTypes(Enum):
    UNION = 0
    DIFFERENCE = 1
    INTERSECT = 2


class BlenderModifiers(Enum):
    EDGE_SPLIT = 0
    SUBSURF = 1
    BOOLEAN = 2
    MIRROR = 3  # https://docs.blender.org/api/current/bpy.types.MirrorModifier.html
    SCREW = 4
    SOLIDIFY = 5
    CURVE = 6
    ARRAY = 7
    BEVEL = 8
    DECIMATE = 9


# This is a list of Blender Constraint types that we have implemented:
class BlenderConstraintTypes(Enum):
    LIMIT_LOCATION = ConstraintTypes.LimitLocation
    LIMIT_ROTATION = ConstraintTypes.LimitRotation
    PIVOT = ConstraintTypes.Pivot
    COPY_ROTATION = ConstraintTypes.FixedRotation
    COPY_LOCATION = ConstraintTypes.FixedPosition

    def get_default_blender_name(self):
        if self.name == BlenderConstraintTypes.LIMIT_LOCATION.name:
            return "Limit Location"
        elif self.name == BlenderConstraintTypes.LIMIT_ROTATION.name:
            return "Limit Rotation"
        elif self.name == BlenderConstraintTypes.PIVOT.name:
            return "Pivot"
        elif self.name == BlenderConstraintTypes.COPY_ROTATION.name:
            return "Copy Rotation"
        elif self.name == BlenderConstraintTypes.COPY_LOCATION.name:
            return "Copy Location"

    def format_constraint_name(self, object_name, relative_to_object_name):
        name = ""

        if self.name == BlenderConstraintTypes.LIMIT_LOCATION.name:
            name = "lim_loc"
        elif self.name == BlenderConstraintTypes.LIMIT_ROTATION.name:
            name = "lim_rot"
        elif self.name == BlenderConstraintTypes.PIVOT.name:
            name = "pivot"
        elif self.name == BlenderConstraintTypes.COPY_ROTATION.name:
            name = "copy_rot"
        elif self.name == BlenderConstraintTypes.COPY_LOCATION.name:
            name = "copy_loc"

        name += f"_{object_name}"

        if relative_to_object_name:
            name += f"_{relative_to_object_name}"

        return name

    # Convert a utilities ConstraintTypes to BlenderConstraintTypes

    @staticmethod
    def from_constraint_types(constraint_type: ConstraintTypes):
        [result] = list(
            filter(
                lambda b: b.value == constraint_type,
                [b for b in BlenderConstraintTypes],
            )
        )

        return result


# These are a list of Blender Driver-related types that we have implemented:

# https://docs.blender.org/api/current/bpy.types.Driver.html#bpy.types.Driver.type
# [‘AVERAGE’, ‘SUM’, ‘SCRIPTED’, ‘MIN’, ‘MAX’]
# BlenderDriverTypes = bpy.types.Driver.bl_rna.properties['type'].enum_items

# https://docs.blender.org/api/current/bpy.types.DriverVariable.html#bpy.types.DriverVariable.type
# [‘SINGLE_PROP’, ‘TRANSFORMS’, ‘ROTATION_DIFF’, ‘LOC_DIFF’]
# BlenderDriverVariableTypes = bpy.types.DriverVariable.bl_rna.properties['type'].enum_items

# https://docs.blender.org/api/current/bpy.types.DriverTarget.html?highlight=transform_type#bpy.types.DriverTarget.transform_type
# [‘LOC_X’, ‘LOC_Y’, ‘LOC_Z’, ‘ROT_X’, ‘ROT_Y’, ‘ROT_Z’, ‘ROT_W’, ‘SCALE_X’, ‘SCALE_Y’, ‘SCALE_Z’, ‘SCALE_AVG’]
# BlenderDriverVariableTransformTypes = bpy.types.DriverTarget.bl_rna.properties[
# 'transform_type'].enum_items

# https://docs.blender.org/api/current/bpy.types.DriverTarget.html?highlight=transform_type#bpy.types.DriverTarget.transform_space
# [‘WORLD_SPACE’, ‘TRANSFORM_SPACE’, ‘LOCAL_SPACE’]
# BlenderDriverVariableTransformSpaces = bpy.types.DriverTarget.bl_rna.properties[
#     'transform_space'].enum_items


# This is a list of Blender primitives that we have implemented:
class BlenderObjectPrimitiveTypes(Enum):
    cube = 0
    cone = 1
    cylinder = 2
    torus = 3
    sphere = 4
    uvsphere = 5
    circle = 6
    grid = 7
    monkey = 8
    empty = 9
    plane = 10

    def default_name_in_blender(self):
        if self == BlenderObjectPrimitiveTypes.sphere:
            return "Icosphere"
        if self == BlenderObjectPrimitiveTypes.uvsphere:
            return "Sphere"
        # quick way to figure out the default names when a shape is added.
        # this is may come to bite later when the primitive name does not follow this rule:
        return self.name[0].upper() + self.name[1:]

    # a quick way to keep track of which primitives have meshes/curve data
    def has_data(self):
        if self == BlenderObjectPrimitiveTypes.empty:
            return False
        return True


# This is a list of Blender Curve types that we have implemented:


class BlenderCurveTypes(Enum):
    POLY = CurveTypes.POLY
    NURBS = CurveTypes.NURBS
    BEZIER = CurveTypes.BEZIER

    # Convert a utilities CurveTypes to BlenderCurveTypes
    @staticmethod
    def from_curve_types(curve_type: CurveTypes):
        [result] = list(
            filter(lambda b: b.value == curve_type, [b for b in BlenderCurveTypes])
        )

        return result


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
class BlenderCurvePrimitiveTypes(Enum):
    # These names should match the names in Blender
    Point = CurvePrimitiveTypes.Point
    LineTo = CurvePrimitiveTypes.LineTo
    Distance = CurvePrimitiveTypes.Line
    Angle = CurvePrimitiveTypes.Angle
    Circle = CurvePrimitiveTypes.Circle
    Ellipse = CurvePrimitiveTypes.Ellipse
    Sector = CurvePrimitiveTypes.Sector
    Segment = CurvePrimitiveTypes.Segment
    Rectangle = CurvePrimitiveTypes.Rectangle
    Rhomb = CurvePrimitiveTypes.Rhomb
    Trapezoid = CurvePrimitiveTypes.Trapezoid
    Polygon = CurvePrimitiveTypes.Polygon
    Polygon_ab = CurvePrimitiveTypes.Polygon_ab
    Arc = CurvePrimitiveTypes.Arc
    Spiral = CurvePrimitiveTypes.Spiral

    # Convert a utilities CurvePrimitiveTypes to BlenderCurvePrimitiveTypes
    @staticmethod
    def from_curve_primitive_types(curve_primitive_type: CurvePrimitiveTypes):
        [result] = list(
            filter(
                lambda b: b.value == curve_primitive_type,
                [b for b in BlenderCurvePrimitiveTypes],
            )
        )

        return result

    def get_default_curve_type(self):
        return BlenderCurveTypes.NURBS


class RepeatMode(Enum):
    extend = (0,)
    clip = (1,)
    repeat = 2

    # references https://docs.blender.org/api/current/bpy.types.ImageTexture.html#bpy.types.ImageTexture.extension

    @property
    def get_blender_name(self):
        if self == RepeatMode.extend:
            return "EXTEND"
        if self == RepeatMode.clip:
            return "CLIP"
        if self == RepeatMode.repeat:
            return "REPEAT"


class FileFormat(Enum):
    # References https://docs.blender.org/api/current/bpy_types_enum_items/image_type_items.html#rna-enum-image-type-items
    PNG = FileFormats.PNG
    JPEG = FileFormats.JPEG
    OPEN_EXR = FileFormats.OPEN_EXR
    FFMPEG = FileFormats.MP4

    @staticmethod
    def from_utilities_file_format(fileformat: FileFormats):
        for format in FileFormat:
            if format.value == fileformat:
                return format

        raise NotImplementedError(f"{fileformat} is not implemented")


class RenderEngines(Enum):
    BLENDER_EEVEE = 0
    CYCLES = 1
    BLENDER_WORKBENCH = 2

    @staticmethod
    def from_string(name: str):
        name = name.lower()
        if name == "eevee":
            return RenderEngines.BLENDER_EEVEE
        if name == "cycle":
            return RenderEngines.CYCLES
        if name == "workbench":
            return RenderEngines.BLENDER_WORKBENCH

        raise TypeError(f"{name} is not a supported type.")
