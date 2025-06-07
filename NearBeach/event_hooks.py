from collections import defaultdict, namedtuple
from itertools import zip_longest


ValueTypes = namedtuple("ValueTypes", ("expected", "got"))

class Registry(defaultdict):
    """A registy of event types and the hooks to call when they are emitted"""

    def __init__(self, init=None, /, *args, **kwargs):
        super().__init__(init, *args, **kwargs)
        self._types = {}

    def register_func(self, event_type):
        """register function against event type"""
        def wrapper(func):
            self[event_type].append(func)
            return func

        return wrapper

    def register_event_type(self, event_type, *value_type):
        # Use dict keys to register event types
        if event_type in self:
            if self._types[event_type] != value_type:
                raise ValueError(f"event with same name '{event_type}' but different types {self._types[event_type]} != {value_type}")
        else:
            self[event_type]
            self._types[event_type] = value_type

    def _check_value_types(self, event_type, values):
        types = []
        incorrect_found=False
        for v, t in zip_longest(values, self._types[event_type]):
            types.append(ValueTypes(expected=t, got=v))
            if v is None and t is None:
                continue

            if (
                (v is None and t is not None) or
                (v is not None and t is None) or
                not isinstance(v, t)
            ):
                incorrect_found = True

        if incorrect_found:
            value_types = [
                f"(expected={v.expected}, got={v.got}({type(v.got)}))"
                for v in types
            ]
            # TODO: log error
            print(f"ERROR: Emit for event {event_type} submitted with an incorrect type submitted values [{', '.join(value_types)}]")
            return False
        return True

    def emit(self, event_type, *values):
        """call registered functions for a given event type"""

        if not self._check_value_types(event_type, values):
            return

        for func in self.get(event_type, []):
            func(*values)

_registry = Registry(list)

# Hide registry via proxy functions

def register_event_type(event_type, value_type):
    return _registry.register_event_type(event_type, value_type)

def emit(event_type, value):
    return _registry.emit(event_type, value)

def register_func(event_type):
    return _registry.register_func(event_type)


EventType = namedtuple("EventType", ("name", "types"))

def list_event_types():
    return [
        EventType(name=event_name, types=_registry._types[event_name])
        for event_name in _registry.keys()
    ]

