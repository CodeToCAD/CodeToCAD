# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class SketchTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_clone(self):

        pass

    @abstractmethod
    def test_create_text(self):

        pass

    @abstractmethod
    def test_create_from_vertices(self):

        pass

    @abstractmethod
    def test_create_point(self):

        pass

    @abstractmethod
    def test_create_line(self):

        pass

    @abstractmethod
    def test_create_circle(self):

        pass

    @abstractmethod
    def test_create_ellipse(self):

        pass

    @abstractmethod
    def test_create_arc(self):

        pass

    @abstractmethod
    def test_create_rectangle(self):

        pass

    @abstractmethod
    def test_create_polygon(self):

        pass

    @abstractmethod
    def test_create_trapezoid(self):

        pass

    @abstractmethod
    def test_create_spiral(self):

        pass
