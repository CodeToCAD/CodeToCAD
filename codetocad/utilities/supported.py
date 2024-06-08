from functools import wraps

from codetocad.enums.support_level import SupportLevel


def supported(
    supportedLevel: SupportLevel,
    notes: str | None = None,
    versions: list[str] | None = None,
):
    """
    Marks a method's SupportLevel in a Provider implementation.
    """

    def supported_wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if supportedLevel.value < SupportLevel.PARTIAL.value:
                raise Exception("This method is not supported yet.")
            return func(*args, **kwargs)

        return wrapper

    return supported_wrap
