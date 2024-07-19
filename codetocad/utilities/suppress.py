from contextlib import AbstractContextManager


class suppress(AbstractContextManager):
    """A modified vesion of contextlib.suppress"""

    def __init__(self, *exceptions, is_print_exception: bool = True):
        self._exceptions = exceptions
        self.is_print_exception = is_print_exception

    def __enter__(self):
        pass

    def _print_exception_and_suppress(self, exception):
        if self.is_print_exception:
            print(exception)
        return True

    def __exit__(self, exctype, excinst, exctb):
        if exctype is None:
            return
        if issubclass(exctype, self._exceptions):
            return self._print_exception_and_suppress(excinst)
        if issubclass(exctype, BaseExceptionGroup):
            match, rest = excinst.split(self._exceptions)
            if rest is None:
                return self._print_exception_and_suppress(excinst)
            raise rest
        return False
