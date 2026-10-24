from drf_spectacular.utils import extend_schema_view

from NearBeach.api_docs import extensions  # noqa: F401 - registers the custom field extensions
from drf_spectacular.utils import get_view_method_names


def apply_schema(schema):
    """Class decorator attaching a {method_name: extend_schema(...)} dict to a view.

    Unlike extend_schema_view alone, this also reaches methods registered with
    `@action(...).mapping.<verb>`, which drf-spectacular does not list as view methods.
    """
    def decorator(view):
        available = set(get_view_method_names(view))
        in_view = {k: v for k, v in schema.items() if k in available}
        extend_schema_view(**in_view)(view)
        for name, decorate in schema.items():
            if name not in available:
                decorate(getattr(view, name))
        return view

    return decorator
