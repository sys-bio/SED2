"""Repeat-0009 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0009.md):
"The input of every entry in a Repeat's aggregateOutputVariables must
reference one of that Repeat's own subTasks, or an output of one." Same
idea as Repeat-0008, for the AggregationCalculation entries that define
[id].aggregates - the entry's own `input` field (an AnyValueOrRef) already
gets full generic SEDBase-0005 through -0015 reference checking via the
"any"-kind branch in RUNTIME's own _validate_own (AggregationCalculation is
validated like any other class); this rule adds the Repeat-specific "must
be one of MY own subTasks" constraint on top.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ok, *, value, class_name, id_value, attr, location, make_problem):
    """The dispatcher (RUNTIME's _check_repeat_own_children) has already
    resolved the aggregateOutputVariables entry's own `input` reference and
    checked whether its target's immediate parent is this Repeat instance
    itself - ok is that outcome. `attr` is always 'input' here, per the
    message's own "has input '{value}'" wording."""
    if ok:
        return []
    return [make_problem(
        "Repeat-0009", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value})]
