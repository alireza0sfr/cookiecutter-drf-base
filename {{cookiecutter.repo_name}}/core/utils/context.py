import threading

_thread_locals = threading.local()


class AppContext:
    @staticmethod
    def set(key, value):
        if not hasattr(_thread_locals, "context"):
            _thread_locals.context = {}
        _thread_locals.context[key] = value

    @staticmethod
    def get(key, default=None):
        if not hasattr(_thread_locals, "context"):
            return default
        return _thread_locals.context.get(key, default)

    @staticmethod
    def remove(key):
        if hasattr(_thread_locals, "context") and key in _thread_locals.context:
            del _thread_locals.context[key]

    @staticmethod
    def clear():
        if hasattr(_thread_locals, "context"):
            _thread_locals.context.clear()

    @staticmethod
    def has(key):
        if not hasattr(_thread_locals, "context"):
            return False
        return key in _thread_locals.context

    @staticmethod
    def all():
        if not hasattr(_thread_locals, "context"):
            return {}
        return dict(_thread_locals.context)
