try:
    # Only Python >12 has override.
    override = __import__("typing").override
except:  # noqa

    def override(method):
        return method
