from functools import wraps

def enforce_with_context(cls):
    original_new = cls.__new__
    original_enter = cls.__enter__
    original_exit = cls.__exit__

    @wraps(original_new)
    def new_wrapper(cls, *args, **kwargs):
        instance = original_new(cls)
        instance._is_within_with_block = False
        return instance

    @wraps(original_enter)
    def enter_wrapper(self):
        self._is_within_with_block = True
        return original_enter(self)

    @wraps(original_exit)
    def exit_wrapper(self, exc_type, exc_value, traceback):
        self._is_within_with_block = True
        return original_exit(self, exc_type, exc_value, traceback)

    def method_wrapper(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self._is_within_with_block:
                raise RuntimeError(f"Methods of {cls.__name__} must be called inside a 'with' block.")
            return method(self, *args, **kwargs)
        return wrapper

    # Wrap all methods to enforce the check
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith('__'):
            setattr(cls, attr_name, method_wrapper(attr))

    cls.__new__ = new_wrapper
    cls.__enter__ = enter_wrapper
    cls.__exit__ = exit_wrapper

    return cls