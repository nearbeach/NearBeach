"""Helpers for the `meta_data` JSON field that objects carry."""

import copy
import json
from typing import Any

# Maximum size of the serialised meta_data object, in bytes (UTF-8)
META_DATA_MAX_BYTES: int = 65536

MetaData = dict[str, Any]


def merge_meta_data(existing: MetaData, patch: MetaData) -> MetaData:
    """Merge `patch` into `existing` following JSON Merge Patch (RFC 7386).

    - Keys in `patch` are added or updated.
    - Keys not in `patch` are left untouched.
    - Objects merge recursively.
    - A value of `None` (JSON null) deletes the key; deleting a missing key is a no-op.
    - Anything else (including lists) replaces the existing value whole.

    Neither argument is modified; a new dict is returned.
    """
    result: MetaData = copy.deepcopy(existing)

    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict):
            current = result.get(key)
            result[key] = merge_meta_data(current if isinstance(current, dict) else {}, value)
        else:
            result[key] = copy.deepcopy(value)

    return result


def meta_data_size(value: MetaData) -> int:
    """Size in bytes of the compact JSON form of `value`."""
    return len(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
