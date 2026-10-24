"""drf-spectacular post-processing hooks."""

# Read-only fields that are only filled in on some responses. drf-spectacular lists every read-only
# field as required, so remove the conditional ones from the components they are conditional in.
CONDITIONAL_FIELDS = {
    # user_list is only added when a single project is retrieved - not on list or create
    "Project": {"user_list"},
}


def make_conditional_fields_optional(result, generator, request, public):
    schemas = result.get("components", {}).get("schemas", {})
    for name, fields in CONDITIONAL_FIELDS.items():
        schema = schemas.get(name)
        if schema is None or "required" not in schema:
            continue

        schema["required"] = [field for field in schema["required"] if field not in fields]
        if not schema["required"]:
            del schema["required"]

    return result
