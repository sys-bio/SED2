"""SEDBase-0014 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0014.md):
"An integer or range index into a dimension whose size is sourced as
runtime and documents a min should warn when the index requires more
entries than min guarantees."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(dims_before, index_accessors, *, value, class_name, id_value, attr, location, make_problem):
    """dims_before is outputs_shape.resolve_output()'s own pre-index
    dimensions list, or None when the target's dimension count itself
    isn't static. Per-dimension: only fires when that dimension's own
    "source" is "runtime" AND it carries a "min" (SEDBase-0014.md) - the
    complement of SEDBase-0011's own guard (which needs a concrete "size",
    never present here), so the two rules never both fire for the same
    index. A bare index n needs min > n (this also naturally never fires
    for a negative n, since min is always >= 0 - "at least min entries
    from the front" says nothing about how many exist from the end, so a
    from-the-end index can't be flagged as under-guaranteed this way,
    matching SEDBase-0014.md's own worked example, which only covers a
    bare non-negative n). A range [a:b] only checks the given end b
    (SEDBase-0014.md's own text: "a range [a:b] needs min >= b" - silent on
    a and on an open-ended b, so this only fires when b is an explicit,
    non-negative value)."""
    if dims_before is None:
        return []
    problems = []
    for i, idx in enumerate(index_accessors):
        if i >= len(dims_before):
            continue
        dim = dims_before[i]
        if dim["source"] != "runtime" or dim["min"] is None:
            continue
        m = dim["min"]
        if idx.kind == "int":
            if not (m > idx.value):
                problems.append(make_problem(
                    "SEDBase-0014", location, attr=attr, value=value, subvalue=idx.value,
                    **{"class": class_name, "id": id_value, "min": m},
                ))
        elif idx.kind == "range":
            a, b = idx.value
            if b is not None and b >= 0 and not (m >= b):
                subvalue = f"[{'' if a is None else a}:{b}]"
                problems.append(make_problem(
                    "SEDBase-0014", location, attr=attr, value=value, subvalue=subvalue,
                    **{"class": class_name, "id": id_value, "min": m},
                ))
    return problems
