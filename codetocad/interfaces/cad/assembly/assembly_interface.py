from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAddInterface
from codetocad.interfaces.cad.assembly.assembly_get import AssemblyGetInterface
from codetocad.interfaces.cad.part.part_interface import PartInterface


class AssemblyInterface:
    def __init__(self):
        self.parts: list[PartInterface] = []

        self.add = AssemblyAddInterface(self)
        self.get = AssemblyGetInterface(self)

    def __repr__(self):
        return f"<Assembly: {self.parts}>"
