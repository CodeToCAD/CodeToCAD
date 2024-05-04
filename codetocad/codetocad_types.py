from typing import TypeAlias, Union

from codetocad.core.angle import Angle
from codetocad.core.dimension import Dimension
from codetocad.core.dimensions import Dimensions
from codetocad.core.point import Point
from codetocad.core.boundary_box import BoundaryBox  # noqa
from codetocad.core.boundary_axis import BoundaryAxis  # noqa
from codetocad.enums.angle_unit import AngleUnit  # noqa
from codetocad.enums.axis import Axis
from codetocad.enums.constraint_types import ConstraintTypes  # noqa
from codetocad.enums.curve_primitive_types import CurvePrimitiveTypes  # noqa
from codetocad.enums.curve_types import CurveTypes  # noqa
from codetocad.enums.length_unit import LengthUnit
from codetocad.enums.preset_landmark import PresetLandmark
from codetocad.enums.file_formats import FileFormats  # noqa
from codetocad.enums.length_unit import LengthUnit  # noqa
from codetocad.enums.preset_landmark import PresetLandmark  # noqa
from codetocad.enums.preset_material import PresetMaterial
from codetocad.enums.scaling_methods import ScalingMethods  # noqa
from codetocad.enums.units import Units  # noqa
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.interfaces.camera_interface import CameraInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.exportable_interface import ExportableInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.landmarkable_interface import LandmarkableInterface
from codetocad.interfaces.material_interface import MaterialInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.interfaces.vertex_interface import VertexInterface
