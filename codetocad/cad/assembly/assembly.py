from codetocad.cad.assembly.assembly_add import AssemblyAdd
from codetocad.cad.assembly.assembly_get import AssemblyGet
from codetocad.cad.part.part import Part


class Assembly:
    def __init__(self):
        self.parts: list[Part] = []

        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

    def __repr__(self):
        return f"<Assembly: {self.parts}>"
