# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


class ProjectableInterface(metaclass=ABCMeta):
    """
    This entity can be projected onto a surface or accept a projection
    """

    @abstractmethod
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        """
        Project another entity onto this one.
        """

        print("project is called in an abstract method. Please override this method.")

        raise NotImplementedError()
