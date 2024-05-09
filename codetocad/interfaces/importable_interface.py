# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from typing import Self


class ImportableInterface(metaclass=ABCMeta):
    """
    An entity that can be imported from a file.
    """

    @abstractmethod
    def create_from_file(self, file_path: "str", file_type: "str| None" = None) -> Self:
        """
        Imports geometry from a file.
        """

        print(
            "create_from_file is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
