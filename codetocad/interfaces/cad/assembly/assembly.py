from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAdd
from codetocad.interfaces.cad.assembly.assembly_get import AssemblyGet
from codetocad.interfaces.cad.part.part import Part


class Assembly:
    def __init__(self):
        self.parts: list[Part] = []

        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

    def __repr__(self):
        return f"<Assembly: {self.parts}>"
