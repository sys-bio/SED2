"""SEDBase-0007 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0007.md):
"A reference must not target an AbstractOutput, or anything contained in
one." Enforces core-spec.md Section 6: an AbstractOutput is always a final
stage and is never an input to anything else.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(parsed, *, class_name, id_value, attr, location, make_problem):
    """parsed is a _runtime.ParsedReference. 'outputs' is deliberately kept
    a syntactically legal collection name by SEDBase-0005 (see its own
    note); this rule is what actually rejects using it - and it can do so
    purely from the collection name, with no containment-tree walk needed,
    since 'outputs' is the only root collection whose every member (and
    everything nested inside one) is AbstractOutput-rooted.
    """
    if parsed.collection == "outputs":
        return [make_problem(
            "SEDBase-0007", location, attr=attr, value=parsed.raw,
            **{"class": class_name, "id": id_value},
        )]
    return []
