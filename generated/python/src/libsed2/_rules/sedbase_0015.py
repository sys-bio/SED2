"""SEDBase-0015 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0015.md):
"A reference required to resolve to a scalar value must apply enough
non-range indices to reduce its target's shape to zero remaining
dimensions." Backs every "must be a reference to a number/string/..."
field-level (check: ref-type) rule - see _check_ref_type in
emit_python.py's RUNTIME, which only proceeds to compare the resolved
scalar's own type once THIS rule has confirmed the shape actually reduced
to a scalar in the first place.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(dims_after, expected_type, *, value, class_name, id_value, attr, location, make_problem):
    """dims_after is outputs_shape.resolve_output()'s own post-index
    dimensions list (only ever computed here for a field whose declared
    kind requires a scalar - NumberOrRef/StringOrRef/IntegerOrRef/
    BooleanOrRef; ArrayOrRef/DictOrRef fields never call this rule, since
    they don't require scalar reduction in the first place). None means
    the shape wasn't statically known at all - nothing to say either way,
    so this stays silent, same as SEDBase-0009 through -0011's own "only
    fires when computable" convention. expected_type is the field's own
    declared scalar kind, in the message's own vocabulary ("number",
    "string", "integer", "boolean")."""
    if dims_after is None:
        return []
    count = len(dims_after)
    if count == 0:
        return []
    return [make_problem(
        "SEDBase-0015", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value, "expected-type": expected_type, "count": count},
    )]
