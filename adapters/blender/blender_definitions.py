import bpy

from enum import Enum


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


class BlenderLength(Enum):
    # These are the units allowed in a Blender document:
    # metric
    KILOMETERS = 0
    METERS = 1
    CENTIMETERS = 2
    MILLIMETERS = 3
    MICROMETERS = 4
    # imperial
    MILES = 5
    FEET = 6
    INCHES = 7
    THOU = 8

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


class BlenderVersions(Enum):
    TWO_DOT_EIGHTY = (2, 80, 0)
    THREE_DOT_ONE = (3, 1, 0)

    @property
    def version(self):
        return ".".join([str(ver) for ver in self.value])


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
    LIMIT_LOCATION = 0
    LIMIT_ROTATION = 1
    PIVOT = 2
    COPY_ROTATION = 3
    COPY_LOCATION = 4

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
    POLY = 0
    NURBS = 1
    BEZIER = 2


# assumes add_curve_extra_objects is enabled
# https://github.com/blender/blender-addons/blob/master/add_curve_extra_objects/add_curve_simple.py
class BlenderCurvePrimitiveTypes(Enum):
    # These names should match the names in Blender
    Point = 0
    LineTo = 1
    Distance = 2
    Angle = 3
    Circle = 4
    Ellipse = 5
    Sector = 6
    Segment = 7
    Rectangle = 8
    Rhomb = 9
    Trapezoid = 10
    Polygon = 11
    Polygon_ab = 12
    Arc = 13
    Spiral = 14

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
    PNG = 0
    JPEG = 1
    OPEN_EXR = 2
    FFMPEG = 3


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
