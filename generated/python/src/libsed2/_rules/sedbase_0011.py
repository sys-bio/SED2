"""SEDBase-0011 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0011.md):
"An integer or range index in a reference must fall within the size of the
dimension it indexes."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(dims_before, index_accessors, *, value, class_name, id_value, attr, location, make_problem):
    """dims_before is outputs_shape.resolve_output()'s own pre-index
    dimensions list, or None when the target's dimension count itself isn't
    static (see SEDBase-0009's own docstring). Per-dimension: only fires
    when THAT dimension's own "size" resolved to a concrete int (not None -
    SEDBase-0011.md: "Only fires when that dimension's size is 'static' and
    computable"; a size sourced as runtime/input-file resolves to None in
    outputs_shape and is SEDBase-0014's concern instead, not this rule's).
    Negative indices count from the end (Python-style): for size n, legal
    integer indices are -n..n-1; for a range [a:b], BOTH given ends must lie
    within -n..n (note the wider n, not n-1 - a range end can equal n), and
    the range must select at least one element once open ends (None) are
    filled in as 0/n and negative ends are normalized."""
    if dims_before is None:
        return []
    problems = []
    for i, idx in enumerate(index_accessors):
        if i >= len(dims_before):
            continue
        n = dims_before[i]["size"]
        if n is None:
            continue
        if idx.kind == "int":
            if idx.value < -n or idx.value > n - 1:
                problems.append(make_problem(
                    "SEDBase-0011", location, attr=attr, value=value, subvalue=idx.value,
                    **{"class": class_name, "id": id_value, "min": -n, "max": n - 1},
                ))
        elif idx.kind == "range":
            a, b = idx.value
            bad = False
            if a is not None and not (-n <= a <= n):
                bad = True
            if b is not None and not (-n <= b <= n):
                bad = True
            if not bad:
                ea = a if a is not None else 0
                eb = b if b is not None else n
                if ea < 0:
                    ea += n
                if eb < 0:
                    eb += n
                if ea >= eb:
                    bad = True
            if bad:
                subvalue = f"[{'' if a is None else a}:{'' if b is None else b}]"
                problems.append(make_problem(
                    "SEDBase-0011", location, attr=attr, value=value, subvalue=subvalue,
                    **{"class": class_name, "id": id_value, "min": -n, "max": n - 1},
                ))
    return problems
