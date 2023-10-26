# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Entity


class EntityTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_create_from_file(self):
        instance = Part("name", "description")

        value = instance.create_from_file("file_path", "file_type")

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_is_exists(self):
        instance = Part("name", "description")

        value = instance.is_exists("")

        assert value, "Get method failed."

    @abstractmethod
    def test_rename(self):
        instance = Part("name", "description")

        value = instance.rename("new_name", "renamelinked_entities_and_landmarks")

        assert value, "Modify method failed."

    @abstractmethod
    def test_delete(self):
        instance = Part("name", "description")

        value = instance.delete("remove_children")

    @abstractmethod
    def test_is_visible(self):
        instance = Part("name", "description")

        value = instance.is_visible("")

        assert value, "Get method failed."

    @abstractmethod
    def test_set_visible(self):
        instance = Part("name", "description")

        value = instance.set_visible("is_visible")

    @abstractmethod
    def test_apply(self):
        instance = Part("name", "description")

        value = instance.apply("rotation", "scale", "location", "modifiers")

        assert value, "Modify method failed."

    @abstractmethod
    def test_get_native_instance(self):
        instance = Part("name", "description")

        value = instance.get_native_instance("")

        assert value, "Get method failed."

    @abstractmethod
    def test_get_location_world(self):
        instance = Part("name", "description")

        value = instance.get_location_world("")

        assert value, "Get method failed."

    @abstractmethod
    def test_get_location_local(self):
        instance = Part("name", "description")

        value = instance.get_location_local("")

        assert value, "Get method failed."

    @abstractmethod
    def test_select(self):
        instance = Part("name", "description")

        value = instance.select("")

    @abstractmethod
    def test_export(self):
        instance = Part("name", "description")

        value = instance.export("file_path", "overwrite", "scale")

    @abstractmethod
    def test_mirror(self):
        instance = Part("name", "description")

        value = instance.mirror(
            "mirror_across_entity_or_landmark", "axis", "resulting_mirrored_entity_name"
        )

        assert value.is_exists(), "Create method failed."

    @abstractmethod
    def test_linear_pattern(self):
        instance = Part("name", "description")

        value = instance.linear_pattern("instance_count", "offset", "direction_axis")

        assert value, "Modify method failed."

    @abstractmethod
    def test_circular_pattern(self):
        instance = Part("name", "description")

        value = instance.circular_pattern(
            "instance_count",
            "separation_angle",
            "center_entity_or_landmark",
            "normal_direction_axis",
        )

        assert value, "Modify method failed."

    @abstractmethod
    def test_translate_xyz(self):
        instance = Part("name", "description")

        value = instance.translate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @abstractmethod
    def test_translate_x(self):
        instance = Part("name", "description")

        value = instance.translate_x("amount")

        assert value, "Modify method failed."

    @abstractmethod
    def test_translate_y(self):
        instance = Part("name", "description")

        value = instance.translate_y("amount")

        assert value, "Modify method failed."

    @abstractmethod
    def test_translate_z(self):
        instance = Part("name", "description")

        value = instance.translate_z("amount")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_xyz(self):
        instance = Part("name", "description")

        value = instance.scale_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_x(self):
        instance = Part("name", "description")

        value = instance.scale_x("scale")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_y(self):
        instance = Part("name", "description")

        value = instance.scale_y("scale")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_z(self):
        instance = Part("name", "description")

        value = instance.scale_z("scale")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_x_by_factor(self):
        instance = Part("name", "description")

        value = instance.scale_x_by_factor("scale_factor")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_y_by_factor(self):
        instance = Part("name", "description")

        value = instance.scale_y_by_factor("scale_factor")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_z_by_factor(self):
        instance = Part("name", "description")

        value = instance.scale_z_by_factor("scale_factor")

        assert value, "Modify method failed."

    @abstractmethod
    def test_scale_keep_aspect_ratio(self):
        instance = Part("name", "description")

        value = instance.scale_keep_aspect_ratio("scale", "axis")

        assert value, "Modify method failed."

    @abstractmethod
    def test_rotate_xyz(self):
        instance = Part("name", "description")

        value = instance.rotate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @abstractmethod
    def test_rotate_x(self):
        instance = Part("name", "description")

        value = instance.rotate_x("rotation")

        assert value, "Modify method failed."

    @abstractmethod
    def test_rotate_y(self):
        instance = Part("name", "description")

        value = instance.rotate_y("rotation")

        assert value, "Modify method failed."

    @abstractmethod
    def test_rotate_z(self):
        instance = Part("name", "description")

        value = instance.rotate_z("rotation")

        assert value, "Modify method failed."

    @abstractmethod
    def test_twist(self):
        instance = Part("name", "description")

        value = instance.twist("angle", "screw_pitch", "interations", "axis")

        assert value, "Modify method failed."

    @abstractmethod
    def test_remesh(self):
        instance = Part("name", "description")

        value = instance.remesh("strategy", "amount")

        assert value, "Modify method failed."

    @abstractmethod
    def test_create_landmark(self):
        instance = Part("name", "description")

        value = instance.create_landmark("landmark_name", "x", "y", "z")

        assert value, "Get method failed."

    @abstractmethod
    def test_get_bounding_box(self):
        instance = Part("name", "description")

        value = instance.get_bounding_box("")

        assert value, "Get method failed."

    @abstractmethod
    def test_get_dimensions(self):
        instance = Part("name", "description")

        value = instance.get_dimensions("")

        assert value, "Get method failed."

    @abstractmethod
    def test_get_landmark(self):
        instance = Part("name", "description")

        value = instance.get_landmark("landmark_name")

        assert value, "Get method failed."
