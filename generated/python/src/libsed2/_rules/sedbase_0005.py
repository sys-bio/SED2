"""SEDBase-0005 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0005.md):
"The first segment of a reference must name one of SEDDocument's ID-keyed
collections: tasks, constants, outputs, or styles."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations

_KNOWN_COLLECTIONS = ("tasks", "constants", "outputs", "styles")


def check(parsed, *, class_name, id_value, attr, location, make_problem):
    """parsed is a _runtime.ParsedReference (see _parse_reference) for the
    field's own raw reference string. Fires once if parsed.collection isn't
    one of the four known root collections - including when the reference
    has no colon segment at all (parsed.collection is None)."""
    if parsed.collection not in _KNOWN_COLLECTIONS:
        return [make_problem(
            "SEDBase-0005", location, attr=attr, value=parsed.raw,
            **{"class": class_name, "id": id_value},
        )]
    return []
