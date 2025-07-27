from codetocad.cad.assembly.assembly_add import AssemblyAdd
from codetocad.cad.assembly.assembly_get import AssemblyGet


class Assembly:
    def __init__(self):
        self.parts = []

        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

    def __repr__(self):
        return f"<Assembly: {self.parts}>"
