from BlenderProvider import injectBlenderProvider


def test_injectBlenderProvider():
    # NOTE: if you're running this test locally, you might need `pip install fake-bpy-module-latest` or Blender API added to python path
    injectBlenderProvider()


if __name__ == "__main__":
    print("Started test_provider_compliance")
    test_injectBlenderProvider()
    print("Completed test_provider_compliance")
