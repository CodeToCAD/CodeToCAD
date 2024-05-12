from functools import wraps

try:
    # Only Python >12 has override.
    override = __import__("typing").override
except:  # noqa

    def override(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
