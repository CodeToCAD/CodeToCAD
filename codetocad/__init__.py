"""CodeToCAD: one language to define your design.

Define parts and assemblies in Python; when you run ``codetocad``, your
script is federated to the modeling or design application automatically.
"""

from .units import (
    AngleRadians,
    AngleWithUnit,
    DensityKilogramsPerCubicMeter,
    DensityWithUnit,
    LengthMeters,
    LengthWithUnit,
    SomeUnit,
    WeightKilograms,
    WeightWithUnit,
)
from .vectors import Vec3, Vec4
from .location import (
    BoxLocations,
    CubeLocationExpr,
    CubeLocations,
    Location,
    LocationMixin,
    euler_to_quat,
    location,
)
from .topology import Edge, Face, Solid, Vertex
from .ledgers import AssemblyLedger, BooleanLedger
from .materials import (
    MaterialBase,
    MaterialMixin,
    aluminum_material,
    green_material,
    red_material,
    steel_material,
    white_material,
)
from .mixins import (
    BLDCMotorMixin,
    BooleanMixin,
    CameraMixin,
    DCMotorMixin,
    ECADMixin,
    GeometryAnalysisMixin,
    GeometryQueryMixin,
    IMUMixin,
    MicrophoneMixin,
)
from .assembly import Assembly2D, Assembly3D, AssemblyCommon
from .parts import Part2D, Part3D
from .primitives import (
    circle,
    cube,
    cylinder,
    import_file,
    rectangle,
    sphere,
    text,
)
from .ecad import ElectricalComponent, capacitor, led, resistor
from .fasteners import CommonFasteners
from .simulation import (
    CONSTRAINT_OPERATIONS,
    JointSpec,
    Lighting,
    LinkSpec,
    Simulation,
    extract_links,
)
from .fea import FEA, FEAResults
from .cli import main

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # units
    "SomeUnit",
    "LengthMeters",
    "AngleRadians",
    "WeightKilograms",
    "DensityKilogramsPerCubicMeter",
    "LengthWithUnit",
    "AngleWithUnit",
    "WeightWithUnit",
    "DensityWithUnit",
    # vectors
    "Vec3",
    "Vec4",
    # locations
    "Location",
    "CubeLocations",
    "BoxLocations",
    "CubeLocationExpr",
    "LocationMixin",
    "location",
    "euler_to_quat",
    # topology
    "Vertex",
    "Edge",
    "Face",
    "Solid",
    # ledgers
    "BooleanLedger",
    "AssemblyLedger",
    # materials
    "MaterialBase",
    "MaterialMixin",
    "white_material",
    "red_material",
    "green_material",
    "aluminum_material",
    "steel_material",
    # mixins
    "BooleanMixin",
    "GeometryQueryMixin",
    "GeometryAnalysisMixin",
    "ECADMixin",
    "CameraMixin",
    "IMUMixin",
    "MicrophoneMixin",
    "DCMotorMixin",
    "BLDCMotorMixin",
    # assemblies & parts
    "AssemblyCommon",
    "Assembly2D",
    "Assembly3D",
    "Part2D",
    "Part3D",
    # primitives
    "rectangle",
    "circle",
    "text",
    "cube",
    "cylinder",
    "sphere",
    "import_file",
    # ecad
    "ElectricalComponent",
    "led",
    "resistor",
    "capacitor",
    # fasteners
    "CommonFasteners",
    # simulation
    "Simulation",
    "Lighting",
    "LinkSpec",
    "JointSpec",
    "extract_links",
    "CONSTRAINT_OPERATIONS",
    # fea
    "FEA",
    "FEAResults",
    # cli
    "main",
]
