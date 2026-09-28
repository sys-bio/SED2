"""Types-0003 (specsheets/core/Types/v1.0.0/validation/Types-0003.md): "Every
function called in a math expression must be given a number of arguments
its registry entry allows."

See Types-0001.py's module docstring for the shared conventions (fixed
`check` function name, no package-relative imports, copied verbatim into
every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def _arity_ok(spec: tuple, count: int) -> bool:
    """spec is one _predefined_functions.FUNCTIONS value: ('set', {2, 4})
    for a fixed handful of allowed counts (an exact arity normalizes to a
    one-element set), or ('range', min, max) with max possibly None for
    unbounded (e.g. min/max/sum's {"min": 1, "max": null})."""
    if spec[0] == "set":
        return count in spec[1]
    _kind, lo, hi = spec
    return count >= lo and (hi is None or count <= hi)


def _format_arity(spec: tuple) -> str:
    """Renders a FUNCTIONS arity spec for the rule's {expected-count}
    placeholder - "2 or 4", "1", "1 or more", "2 to 4"."""
    if spec[0] == "set":
        return " or ".join(str(n) for n in sorted(spec[1]))
    _kind, lo, hi = spec
    if hi is None:
        return f"{lo} or more"
    if lo == hi:
        return str(lo)
    return f"{lo} to {hi}"


def check(ast, *, class_name, id_value, attr, location, make_problem, functions):
    """Same ast/functions contract as Types-0002.py's check() - see its
    docstring. Skips a call whose name isn't in `functions` at all (that's
    Types-0002's concern, not this rule's, and re-flagging it here would be
    a duplicate diagnosis of the same underlying mistake)."""
    problems = []
    for node in ast.walk():
        if not node.is_function_call():
            continue
        spec = functions.get(node.name)
        if spec is None:
            continue
        count = node.get_num_children()
        if not _arity_ok(spec, count):
            problems.append(make_problem(
                "Types-0003", location, attr=attr, function=node.name, count=count,
                **{"class": class_name, "id": id_value, "expected-count": _format_arity(spec)},
            ))
    return problems
