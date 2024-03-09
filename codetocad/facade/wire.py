# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.wire_interface import WireInterface


class Wire:
    """
    This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(cls, *args, **kwds) -> WireInterface:
        return cls._provider(*args, **kwds)

    @classmethod
    def register(cls, provider: WireInterface):
        cls._provider = provider
