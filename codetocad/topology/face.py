from dataclasses import dataclass
from typing import List

from codetocad.topology.wire import Wire


@dataclass
class Face:
    '''
    A collection of closed Wires
    '''
    wires: List[Wire]
