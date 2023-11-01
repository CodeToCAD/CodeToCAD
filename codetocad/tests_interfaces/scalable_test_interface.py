# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Scalable


class ScalableTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_scale_xyz(self):
        instance = Scalable()

        value = instance.scale_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_x(self):
        instance = Scalable()

        value = instance.scale_x("scale")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_y(self):
        instance = Scalable()

        value = instance.scale_y("scale")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_z(self):
        instance = Scalable()

        value = instance.scale_z("scale")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_x_by_factor(self):
        instance = Scalable()

        value = instance.scale_x_by_factor("scale_factor")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_y_by_factor(self):
        instance = Scalable()

        value = instance.scale_y_by_factor("scale_factor")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_z_by_factor(self):
        instance = Scalable()

        value = instance.scale_z_by_factor("scale_factor")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_keep_aspect_ratio(self):
        instance = Scalable()

        value = instance.scale_keep_aspect_ratio("scale", "axis")

        assert value, "Modify method failed."
