from functools import wraps


def enforce_with_context(cls):
    original_new = cls.__new__
    original_aenter = cls.__aenter__
    original_aexit = cls.__aexit__

    @wraps(original_new)
    def new_wrapper(cls, *args, **kwargs):
        instance = original_new(cls)
        instance._is_within_with_block = False
        return instance

    @wraps(original_aenter)
    def aenter_wrapper(self):
        self._is_within_with_block = True
        return original_aenter(self)

    @wraps(original_aexit)
    def aexit_wrapper(self, exc_type, exc_value, traceback):
        self._is_within_with_block = True
        return original_aexit(self, exc_type, exc_value, traceback)

    def method_wrapper(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self._is_within_with_block:
                raise RuntimeError(
                    f"Methods of {cls.__name__} must be called inside a 'with' block."
                )
            return method(self, *args, **kwargs)

        return wrapper

    # Wrap all methods to enforce the check
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith("_"):
            setattr(cls, attr_name, method_wrapper(attr))

    cls.__new__ = new_wrapper
    cls.__aenter__ = aenter_wrapper
    cls.__aexit__ = aexit_wrapper

    return cls
