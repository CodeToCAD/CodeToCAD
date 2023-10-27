from dataclasses import dataclass
from typing import List

from codetocad.topology.face import Face


@dataclass
class Shell:
    '''
    A collection of connected faces.
    '''
    faces: List[Face]
