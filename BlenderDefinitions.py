import bpy

from enum import Enum
import CodeToCAD.utilities as Utilities

class BlenderTypes(Enum):
    OBJECT = bpy.types.Object
    MESH = bpy.types.Mesh
    CURVE= bpy.types.Curve


# These are the units allowed in a Blender document:
class BlenderLength(Utilities.Units):
    #metric
    KILOMETERS = Utilities.LengthUnit.kilometer
    METERS = Utilities.LengthUnit.meter
    CENTIMETERS = Utilities.LengthUnit.centimeter
    MILLIMETERS = Utilities.LengthUnit.millimeter
    MICROMETERS = Utilities.LengthUnit.micrometer
    #imperial
    MILES = Utilities.LengthUnit.mile
    FEET = Utilities.LengthUnit.foot
    INCHES = Utilities.LengthUnit.inch
    THOU = Utilities.LengthUnit.thousandthInch
    
    # Blender internally uses this unit for everything:
    DEFAULT_BLENDER_UNIT = METERS

    def getSystem(self):
        if self == self.KILOMETERS or self == self.METERS or self == self.CENTIMETERS or self == self.MILLIMETERS or self == self.MICROMETERS:
            return'METRIC'
        else:
            return'IMPERIAL'


    # Convert a utilities LengthUnit to BlenderLength
    @staticmethod
    def fromLengthUnit(unit:Utilities.LengthUnit):

        [result] = list(filter(lambda b: b.value == unit, [b for b in BlenderLength]))

        return result
            
    # Takes in a list of Dimension and converts them to the `DEFAULT_BLENDER_UNIT`, which is the unit blender deals with, no matter what we set the document unit to. 
    @staticmethod
    def convertDimensionsToBlenderUnit(dimensions:list):
        return [
            BlenderLength.convertDimensionToBlenderUnit(dimension)
            
                if (dimension.value != None and dimension.unit != None and dimension.unit != BlenderLength.DEFAULT_BLENDER_UNIT.value)

                else dimension

                    for dimension in dimensions 
        ]

    # Takes in a Dimension object, converts it to the default blender unit, and returns a Dimension object.
    @staticmethod
    def convertDimensionToBlenderUnit(dimension:Utilities.Dimension):
        return  Utilities.Dimension(
                    float(
                        Utilities.convertToLengthUnit(
                            BlenderLength.DEFAULT_BLENDER_UNIT.value, dimension.value,
                            dimension.unit or BlenderLength.DEFAULT_BLENDER_UNIT.value
                        )
                    ),
                    BlenderLength.DEFAULT_BLENDER_UNIT.value
                ) \
                if (dimension.value != None and dimension.unit != None and dimension.unit != BlenderLength.DEFAULT_BLENDER_UNIT.value) \
                else dimension



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
    MIRROR = 3 # https://docs.blender.org/api/current/bpy.types.MirrorModifier.html
    SCREW = 4
    SOLIDIFY = 5
    CURVE = 6


# This is a list of Blender Constraint types that we have implemented:
class BlenderConstraintTypes(Utilities.EquittableEnum):
    LIMIT_LOCATION = Utilities.ConstraintTypes.Translation
    LIMIT_ROTATION = Utilities.ConstraintTypes.Rotation
    PIVOT = Utilities.ConstraintTypes.Pivot
    COPY_ROTATION = Utilities.ConstraintTypes.Gear

    def getDefaultBlenderName(self):
        if self == BlenderConstraintTypes.LIMIT_LOCATION:
            return "Limit Location"
        if self == BlenderConstraintTypes.LIMIT_ROTATION:
            return "Limit Rotation"
        if self == BlenderConstraintTypes.PIVOT:
            return "Pivot"
        if self == BlenderConstraintTypes.COPY_ROTATION:
            return "Copy Rotation"
    
    # Convert a utilities ConstraintTypes to BlenderConstraintTypes
    @staticmethod
    def fromConstraintTypes(constraintType:Utilities.ConstraintTypes):

        [result] = list(filter(lambda b: b.value == constraintType, [b for b in BlenderConstraintTypes]))

        return result


# These are a list of Blender Driver-related types that we have implemented:

# https://docs.blender.org/api/current/bpy.types.Driver.html#bpy.types.Driver.type
# [‘AVERAGE’, ‘SUM’, ‘SCRIPTED’, ‘MIN’, ‘MAX’]
BlenderDriverTypes = bpy.types.Driver.bl_rna.properties['type'].enum_items

# https://docs.blender.org/api/current/bpy.types.DriverVariable.html#bpy.types.DriverVariable.type
# [‘SINGLE_PROP’, ‘TRANSFORMS’, ‘ROTATION_DIFF’, ‘LOC_DIFF’]
BlenderDriverVariableTypes = bpy.types.DriverVariable.bl_rna.properties['type'].enum_items

# https://docs.blender.org/api/current/bpy.types.DriverTarget.html?highlight=transform_type#bpy.types.DriverTarget.transform_type
# [‘LOC_X’, ‘LOC_Y’, ‘LOC_Z’, ‘ROT_X’, ‘ROT_Y’, ‘ROT_Z’, ‘ROT_W’, ‘SCALE_X’, ‘SCALE_Y’, ‘SCALE_Z’, ‘SCALE_AVG’]
BlenderDriverVariableTransformTypes = bpy.types.DriverTarget.bl_rna.properties['transform_type'].enum_items

#https://docs.blender.org/api/current/bpy.types.DriverTarget.html?highlight=transform_type#bpy.types.DriverTarget.transform_space
#[‘WORLD_SPACE’, ‘TRANSFORM_SPACE’, ‘LOCAL_SPACE’]
BlenderDriverVariableTransformSpaces = bpy.types.DriverTarget.bl_rna.properties['transform_space'].enum_items


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
    def fromCurveTypes(curveType:Utilities.CurveTypes):

        [result] = list(filter(lambda b: b.value == curveType, [b for b in BlenderCurveTypes]))

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

    # Convert a utilities CurvePrimitiveTypes to BlenderCurvePrimitiveTypes
    @staticmethod
    def fromCurvePrimitiveTypes(curvePrimitiveType:Utilities.CurvePrimitiveTypes):

        [result] = list(filter(lambda b: b.value == curvePrimitiveType, [b for b in BlenderCurvePrimitiveTypes]))

        return result
            
    def getDefaultCurveType(self):
        if self == BlenderCurvePrimitiveTypes.Point:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.LineTo:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Distance:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Angle:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Circle:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Ellipse:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Sector:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Segment:
            return BlenderCurveTypes.BEZIER
        elif self == BlenderCurvePrimitiveTypes.Rectangle:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Rhomb:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Trapezoid:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Polygon:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Polygon_ab:
            return BlenderCurveTypes.NURBS
        elif self == BlenderCurvePrimitiveTypes.Arc:
            return BlenderCurveTypes.NURBS
        else:
            raise "Unknown primitive"