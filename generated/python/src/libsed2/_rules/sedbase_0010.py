"""SEDBase-0010 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0010.md):
"A label index in a reference must name one of the labels of the dimension
it indexes."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(dims_before, index_accessors, *, value, class_name, id_value, attr, location, make_problem):
    """dims_before is outputs_shape.resolve_output()'s own pre-index
    dimensions list (each a {"size", "labels", "source", "min"} dict), or
    None when the target's dimension count itself isn't static (see
    SEDBase-0009's own docstring) - in which case there's nothing to check
    a label index against at all. Only checks index positions that fall
    within dims_before's own length; a label index beyond it is
    SEDBase-0009's concern, not this rule's, so it's skipped here rather
    than double-firing or raising."""
    if dims_before is None:
        return []
    problems = []
    for i, idx in enumerate(index_accessors):
        if idx.kind != "label" or i >= len(dims_before):
            continue
        labels = dims_before[i]["labels"]
        if labels is None:
            continue  # SEDBase-0010.md: "Only fires when that dimension's labels are static"
        if idx.value not in labels:
            problems.append(make_problem(
                "SEDBase-0010", location, attr=attr, value=value, subvalue=idx.value,
                **{"class": class_name, "id": id_value, "allowed": ", ".join(labels)},
            ))
    return problems
