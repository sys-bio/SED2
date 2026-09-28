"""LoopVariable-0004 (specsheets/auxiliary/LoopVariable/v1.0.0/validation/LoopVariable-0004.md):
"The subsequentValues of a LoopVariable must reference one of its enclosing
Loop's own subTasks, or an output of one." subsequentValues is the value
this loop variable takes on after each iteration, produced by one of the
loop's own subTasks - the one place a reference may point forward in file
order (subTasks is defined after loopVariables in the schema), which
AbstractTask-0003's own chronological check allows (it compares task-dict
membership, not field order within one task - a LoopVariable's own task-
chain position collapses to its enclosing Loop's own position, and a
subTask of that same Loop is always a legal deeper target for it - see
RUNTIME's _check_task_order/_task_chain).

subsequentValues is a plain SIdRef field, so it already gets full generic
SEDBase-0005 through -0015 reference checking via RUNTIME's own
_validate_own; this rule adds the "must be one of the enclosing Loop's own
subTasks" constraint on top, the same shape as Repeat-0008/-0009.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ok, *, value, id_value, location, make_problem):
    """The dispatcher (RUNTIME's _check_loop_variable_scope) has already
    resolved subsequentValues's own reference and checked whether its
    target's immediate parent is this LoopVariable's own enclosing Loop -
    ok is that outcome. This rule's own message template uses neither
    {class} nor {attr} (unlike every other SEDBase/Repeat-family rule here)
    - it always names the fixed "LoopVariable" class and the one field a
    LoopVariable can ever fail this way."""
    if ok:
        return []
    return [make_problem(
        "LoopVariable-0004", location, value=value,
        **{"class": "LoopVariable", "id": id_value})]
