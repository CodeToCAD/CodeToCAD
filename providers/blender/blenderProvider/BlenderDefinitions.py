import bpy

from enum import Enum
import codetocad.utilities as Utilities


class BlenderTypes(Enum):
    OBJECT = bpy.types.Object
    MESH = bpy.types.Mesh
    CURVE = bpy.types.Curve
    TEXT = bpy.types.TextCurve


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


class BlenderLength(Utilities.Units):
    # These are the units allowed in a Blender document:
    # metric
    KILOMETERS = Utilities.LengthUnit.km
    METERS = Utilities.LengthUnit.m
    CENTIMETERS = Utilities.LengthUnit.cm
    MILLIMETERS = Utilities.LengthUnit.mm
    MICROMETERS = Utilities.LengthUnit.μm
    # imperial
    MILES = Utilities.LengthUnit.mi
    FEET = Utilities.LengthUnit.ft
    INCHES = Utilities.LengthUnit.inch
    THOU = Utilities.LengthUnit.thou

    # Blender internally uses this unit for everything:
    DEFAULT_BLENDER_UNIT: Utilities.LengthUnit = METERS  # type: ignore

    def getSystem(self):
        if self == self.KILOMETERS or self == self.METERS or self == self.CENTIMETERS or self == self.MILLIMETERS or self == self.MICROMETERS:
            return 'METRIC'
        else:
            return 'IMPERIAL'

    # Convert a utilities LengthUnit to BlenderLength

    @staticmethod
    def fromLengthUnit(unit: Utilities.LengthUnit) -> 'BlenderLength':

        [result] = list(filter(lambda b: b.value == unit,
                        [b for b in BlenderLength]))

        return result

    # Takes in a list of Dimension and converts them to the `DEFAULT_BLENDER_UNIT`, which is the unit blender deals with, no matter what we set the document unit to.
    @staticmethod
    def convertDimensionsToBlenderUnit(dimensions: list) -> list[Utilities.Dimension]:
        return [
            BlenderLength.convertDimensionToBlenderUnit(dimension)

            if (dimension.value is not None and dimension.unit is not None and dimension.unit != BlenderLength.DEFAULT_BLENDER_UNIT.value)

            else dimension

            for dimension in dimensions
        ]

    # Takes in a Dimension object, converts it to the default blender unit, and returns a Dimension object.
    @staticmethod
    def convertDimensionToBlenderUnit(dimension: Utilities.Dimension):
        if dimension.value == None or dimension.unit == BlenderLength.DEFAULT_BLENDER_UNIT.value:
            return dimension
        if dimension.unit == None:
            dimension.unit = BlenderLength.DEFAULT_BLENDER_UNIT.value
            return dimension
        return dimension.convertToUnit(BlenderLength.DEFAULT_BLENDER_UNIT.value)


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
class BlenderConstraintTypes(Utilities.EquittableEnum):
    LIMIT_LOCATION = Utilities.ConstraintTypes.LimitLocation
    LIMIT_ROTATION = Utilities.ConstraintTypes.LimitRotation
    PIVOT = Utilities.ConstraintTypes.Pivot
    COPY_ROTATION = Utilities.ConstraintTypes.FixedRotation
    COPY_LOCATION = Utilities.ConstraintTypes.FixedPosition

    def getDefaultBlenderName(self):
        if self == BlenderConstraintTypes.LIMIT_LOCATION:
            return "Limit Location"
        if self == BlenderConstraintTypes.LIMIT_ROTATION:
            return "Limit Rotation"
        if self == BlenderConstraintTypes.PIVOT:
            return "Pivot"
        if self == BlenderConstraintTypes.COPY_ROTATION:
            return "Copy Rotation"
        if self == BlenderConstraintTypes.COPY_LOCATION:
            return "Copy Location"

    def formatConstraintName(self, objectName, relativeToObjectName):
        name = ""

        if self == BlenderConstraintTypes.LIMIT_LOCATION:
            name = "lim_loc"
        if self == BlenderConstraintTypes.LIMIT_ROTATION:
            name = "lim_rot"
        if self == BlenderConstraintTypes.PIVOT:
            name = "pivot"
        if self == BlenderConstraintTypes.COPY_ROTATION:
            name = "copy_rot"
        if self == BlenderConstraintTypes.COPY_LOCATION:
            name = "copy_loc"

        name += f"_{objectName}"

        if relativeToObjectName:
            name += f"_{relativeToObjectName}"

        return name

    # Convert a utilities ConstraintTypes to BlenderConstraintTypes

    @staticmethod
    def fromConstraintTypes(constraintType: Utilities.ConstraintTypes):

        [result] = list(filter(lambda b: b.value == constraintType, [
                        b for b in BlenderConstraintTypes]))

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

    def defaultNameInBlender(self):
        if self == BlenderObjectPrimitiveTypes.sphere:
            return "Icosphere"
        if self == BlenderObjectPrimitiveTypes.uvsphere:
            return "Sphere"
        # quick way to figure out the default names when a shape is added.
        # this is may come to bite later when the primitive name does not follow this rule:
        return self.name[0].upper() + self.name[1:]

    # a quick way to keep track of which primitives have meshes/curve data
    def hasData(self):
        if self == BlenderObjectPrimitiveTypes.empty:
            return False
        return True

# This is a list of Blender Curve types that we have implemented:


class BlenderCurveTypes(Utilities.EquittableEnum):
    POLY = Utilities.CurveTypes.POLY
    NURBS = Utilities.CurveTypes.NURBS
    BEZIER = Utilities.CurveTypes.BEZIER

    # Convert a utilities CurveTypes to BlenderCurveTypes
    @staticmethod
    def fromCurveTypes(curveType: Utilities.CurveTypes):

        [result] = list(filter(lambda b: b.value == curveType,
                        [b for b in BlenderCurveTypes]))

        return result


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
class BlenderCurvePrimitiveTypes(Utilities.EquittableEnum):
    # These names should match the names in Blender
    Point = Utilities.CurvePrimitiveTypes.Point
    LineTo = Utilities.CurvePrimitiveTypes.LineTo
    Distance = Utilities.CurvePrimitiveTypes.Line
    Angle = Utilities.CurvePrimitiveTypes.Angle
    Circle = Utilities.CurvePrimitiveTypes.Circle
    Ellipse = Utilities.CurvePrimitiveTypes.Ellipse
    Sector = Utilities.CurvePrimitiveTypes.Sector
    Segment = Utilities.CurvePrimitiveTypes.Segment
    Rectangle = Utilities.CurvePrimitiveTypes.Rectangle
    Rhomb = Utilities.CurvePrimitiveTypes.Rhomb
    Trapezoid = Utilities.CurvePrimitiveTypes.Trapezoid
    Polygon = Utilities.CurvePrimitiveTypes.Polygon
    Polygon_ab = Utilities.CurvePrimitiveTypes.Polygon_ab
    Arc = Utilities.CurvePrimitiveTypes.Arc
    Spiral = Utilities.CurvePrimitiveTypes.Spiral

    # Convert a utilities CurvePrimitiveTypes to BlenderCurvePrimitiveTypes
    @staticmethod
    def fromCurvePrimitiveTypes(curvePrimitiveType: Utilities.CurvePrimitiveTypes):

        [result] = list(filter(lambda b: b.value == curvePrimitiveType, [
                        b for b in BlenderCurvePrimitiveTypes]))

        return result

    def getDefaultCurveType(self):
        return BlenderCurveTypes.NURBS


class RepeatMode(Enum):
    extend = 0,
    clip = 1,
    repeat = 2

    # references https://docs.blender.org/api/current/bpy.types.ImageTexture.html#bpy.types.ImageTexture.extension

    @property
    def getBlenderName(self):
        if self == RepeatMode.extend:
            return 'EXTEND'
        if self == RepeatMode.clip:
            return 'CLIP'
        if self == RepeatMode.repeat:
            return 'REPEAT'


class FileFormat(Enum):
    # References https://docs.blender.org/api/current/bpy_types_enum_items/image_type_items.html#rna-enum-image-type-items
    PNG = Utilities.FileFormats.PNG
    JPEG = Utilities.FileFormats.JPEG
    OPEN_EXR = Utilities.FileFormats.OPEN_EXR
    FFMPEG = Utilities.FileFormats.MP4

    @staticmethod
    def fromUtilitiesFileFormat(fileformat: Utilities.FileFormats):
        for format in FileFormat:
            if format.value == fileformat:
                return format

        raise NotImplementedError(f"{fileformat} is not implemented")


class RenderEngines(Enum):
    BLENDER_EEVEE = 0
    CYCLES = 1
    BLENDER_WORKBENCH = 2

    @staticmethod
    def fromString(name: str):
        name = name.lower()
        if name == "eevee":
            return RenderEngines.BLENDER_EEVEE
        if name == "cycle":
            return RenderEngines.CYCLES
        if name == "workbench":
            return RenderEngines.BLENDER_WORKBENCH

        raise TypeError(f"{name} is not a supported type.")
