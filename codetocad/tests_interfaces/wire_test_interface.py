# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class WireTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_get_normal(self):

        pass

    @abstractmethod
    def test_get_edges(self):

        pass

    @abstractmethod
    def test_get_vertices(self):

        pass

    @abstractmethod
    def test_get_is_closed(self):

        pass

    @abstractmethod
    def test_loft(self):

        pass

    @abstractmethod
    def test_revolve(self):

        pass

    @abstractmethod
    def test_twist(self):

        pass

    @abstractmethod
    def test_extrude(self):

        pass

    @abstractmethod
    def test_sweep(self):

        pass

    @abstractmethod
    def test_offset(self):

        pass

    @abstractmethod
    def test_profile(self):

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
    def test_create_line_to(self):

        pass

    @abstractmethod
    def test_create_arc(self):

        pass
