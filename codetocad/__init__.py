"""CodeToCAD: one language to define your design.

Define parts and assemblies in Python; when you run ``codetocad``, your
script is federated to the modeling or design application automatically.
"""

from codetocad.units import (
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
from codetocad.vectors import Vec3, Vec4
from codetocad.location import (
    BoxLocations,
    CubeLocationExpr,
    CubeLocations,
    Location,
    LocationMixin,
    euler_to_quat,
    location,
)
from codetocad.topology import Edge, Face, Solid, Vertex
from codetocad.ledgers import AssemblyLedger, BooleanLedger
from codetocad.materials import (
    MaterialBase,
    MaterialMixin,
    aluminum_material,
    green_material,
    red_material,
    steel_material,
    white_material,
)
from codetocad.mixins import (
    ActuatorMixin,
    BLDCMotorMixin,
    BooleanMixin,
    CameraMixin,
    CurrentSensorMixin,
    DCMotorMixin,
    ECADMixin,
    EncoderMixin,
    GeometryAnalysisMixin,
    GeometryQueryMixin,
    IMUMixin,
    MicrophoneMixin,
    MotorMixin,
    SensorMixin,
    StepperMotorMixin,
)
from codetocad.assembly import Assembly2D, Assembly3D, AssemblyCommon
from codetocad.parts import Part2D, Part3D
from codetocad.primitives import (
    circle,
    cube,
    cylinder,
    import_file,
    rectangle,
    sphere,
    text,
)
from codetocad.ecad import (
    Circuit,
    CommonFootprints,
    ComponentType,
    ElectricalComponent,
    Footprint,
    Net,
    Pin,
    PinType,
    capacitor,
    current_source,
    diode,
    format_si,
    inductor,
    led,
    parse_si,
    resistor,
    voltage_source,
)
from codetocad.fasteners import CommonFasteners
from codetocad.simulation import (
    CONSTRAINT_OPERATIONS,
    JointSpec,
    Lighting,
    LinkSpec,
    Simulation,
    encode_png,
    extract_links,
)
from codetocad.fea import FEA, FEAResults
from codetocad.communication import (
    BluetoothCommunication,
    Communication,
    CommunicationMixin,
    EventStream,
    MqttCommunication,
    SerialCommunication,
    WifiCommunication,
)
from codetocad.signals import (
    LowPassFilter,
    MedianFilter,
    MovingAverageFilter,
    apply_filter,
)
from codetocad.microcontroller import (
    I2CBus,
    Microcontroller,
    MicrocontrollerBoard,
    MicrocontrollerRuntime,
    PinBinding,
    SPIBus,
    UARTBus,
)
from codetocad.apps import AppBase, Control, PythonApp, RerunApp, WebApp
from codetocad.emulation import (
    EmulatedCommunication,
    EmulatedMicrocontroller,
    EmulatedTransport,
)
from codetocad.cli import main

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
    "SensorMixin",
    "ActuatorMixin",
    "CameraMixin",
    "IMUMixin",
    "MicrophoneMixin",
    "EncoderMixin",
    "CurrentSensorMixin",
    "MotorMixin",
    "DCMotorMixin",
    "BLDCMotorMixin",
    "StepperMotorMixin",
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
    "Circuit",
    "Net",
    "Pin",
    "PinType",
    "ComponentType",
    "Footprint",
    "CommonFootprints",
    "led",
    "diode",
    "resistor",
    "capacitor",
    "inductor",
    "voltage_source",
    "current_source",
    "parse_si",
    "format_si",
    # fasteners
    "CommonFasteners",
    # simulation
    "Simulation",
    "Lighting",
    "LinkSpec",
    "JointSpec",
    "extract_links",
    "encode_png",
    "CONSTRAINT_OPERATIONS",
    # fea
    "FEA",
    "FEAResults",
    # communication
    "Communication",
    "CommunicationMixin",
    "EventStream",
    "SerialCommunication",
    "WifiCommunication",
    "BluetoothCommunication",
    "MqttCommunication",
    # signals
    "LowPassFilter",
    "MovingAverageFilter",
    "MedianFilter",
    "apply_filter",
    # microcontroller
    "Microcontroller",
    "MicrocontrollerBoard",
    "MicrocontrollerRuntime",
    "PinBinding",
    "I2CBus",
    "SPIBus",
    "UARTBus",
    # apps
    "AppBase",
    "Control",
    "PythonApp",
    "WebApp",
    "RerunApp",
    # emulation
    "EmulatedMicrocontroller",
    "EmulatedCommunication",
    "EmulatedTransport",
    # cli
    "main",
]
