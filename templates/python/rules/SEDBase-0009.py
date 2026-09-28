"""SEDBase-0009 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0009.md):
"A reference must not apply more bracket indices than its target has
dimensions."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(dims_before, index_accessors, *, value, class_name, id_value, attr, location, make_problem):
    """dims_before is outputs_shape.resolve_output()'s own pre-index
    dimensions list, or None whenever the target's dimension COUNT itself
    isn't statically known (a whole-shape runtime/input-file source, or no
    "dimensions" at all - a "model"-typed suffix) - SEDBase-0009.md: "Only
    fires when the target's dimension count is static... A 'runtime' or
    'input-file' dimension count never fires this rule." Note this is about
    the ARRAY's own length being fixed, not each dimension's individual
    size - an array-form "dimensions" always has a static count even when
    some entries' own sizes are themselves runtime/input-file (see
    SEDBase-0011/-0014 for those)."""
    if dims_before is None:
        return []
    count = len(index_accessors)
    expected = len(dims_before)
    if count <= expected:
        return []
    return [make_problem(
        "SEDBase-0009", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value, "count": count, "expected-count": expected},
    )]
