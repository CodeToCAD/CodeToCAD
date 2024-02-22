try:
    # Only Python >12 has override.
    override = __import__("typing").override
except:  # noqa

    def override(interface_class):
        # references https://stackoverflow.com/a/8313042
        def overrider(method):
            assert method.__name__ in dir(interface_class)
            return method

        return overrider
