from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly import Assembly


class AssemblyPart:
    def __init__(self, assembly: "Assembly"):
        self.assembly = assembly

    def __getitem__(self, key: str | int):
        return self._get_parts(key)

    def __call__(self, key: str | int):
        return self._get_parts(key)

    def _get_parts(self, key: str | int):
        if not isinstance(key, (str, int)):
            raise TypeError(
                "You can query parts using their name (string) or their index. e.g. `assembly.parts['part_name']` or `assembly.parts[0]` or `assembly.parts[-1]`."
            )
        if isinstance(key, str):
            for part in self.assembly.parts:
                if part.name == key:
                    return part
            raise KeyError(f"No part found with the name '{key}'.")
        return self.assembly.parts[key]
