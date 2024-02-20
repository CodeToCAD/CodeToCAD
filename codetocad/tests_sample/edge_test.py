# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import EdgeTestInterface


from codetocad import Edge, Entity, Vertex, Landmark


class EdgeTest(TestProviderCase, EdgeTestInterface):
    @skip("TODO")
    def test_offset(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.offset(distance=Dimension(0, "mm"))

        assert value, "Get method failed."

    @skip("TODO")
    def test_fillet(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.fillet(
            other_edge=Edge(
                v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                name="an edge",
            ),
            amount=Angle("90"),
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_set_is_construction(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.set_is_construction(is_construction=True)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_get_is_construction(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.get_is_construction()

        assert value, "Get method failed."

    @skip("TODO")
    def test_mirror(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.mirror(
            mirror_across_entity=__import__("codetocad").Part("an entity"),
            axis=x,
            resulting_mirrored_entity_name="String",
        )

        assert value.is_exists(), "Create method failed."

    @skip("TODO")
    def test_linear_pattern(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.linear_pattern(
            instance_count=0, offset=Dimension(0, "mm"), direction_axis="z"
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_circular_pattern(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.circular_pattern(
            instance_count=0,
            separation_angle=Angle("90"),
            center_entity_or_landmark=__import__("codetocad").Part("an entity"),
            normal_direction_axis="z",
        )

        assert value, "Modify method failed."

    @skip("TODO")
    def test_remesh(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.remesh(strategy="String", amount=0.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_subdivide(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.subdivide(amount=0.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_decimate(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.decimate(amount=0.0)

        assert value, "Modify method failed."

    @skip("TODO")
    def test_project(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.project(
            project_onto=__import__("codetocad").Sketch("a projected sketch")
        )

        assert value, "Get method failed."

    @skip("TODO")
    def test_create_landmark(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.create_landmark(
            landmark_name="String",
            x=Dimension(0, "mm"),
            y=Dimension(0, "mm"),
            z=Dimension(0, "mm"),
        )

        assert value, "Get method failed."

    @skip("TODO")
    def test_get_landmark(self):
        instance = Edge(
            name="String",
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            description="String",
            native_instance=value,
            parent_entity=__import__("codetocad").Part("an entity"),
        )

        value = instance.get_landmark(landmark_name=PresetLandmark.topLeft)

        assert value, "Get method failed."
