"""SEDBase-0012 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0012.md):
"A bracket index into a constant must match the structure of that
constant's literal value."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ok, bad_subvalue, resolved_value, *, value, class_name, id_value, attr, location, make_problem):
    """The dispatcher has already done the actual indexing (following one
    reference-hop first per SEDBase-0012.md: "A constant whose value is
    itself a reference is followed first" - outputs_shape.index_into_
    literal, catching NotIndexable) and hands this rule just the outcome:
    ok (whether every index in the chain applied cleanly), the specific
    index that failed (bad_subvalue, meaningful only when not ok), and
    resolved_value - the constant's own (post-dereference) literal value,
    pre-formatted as a compact string for the message's {resolved-value}."""
    if ok:
        return []
    return [make_problem(
        "SEDBase-0012", location, attr=attr, value=value, subvalue=bad_subvalue,
        **{"class": class_name, "id": id_value, "resolved-value": resolved_value},
    )]
