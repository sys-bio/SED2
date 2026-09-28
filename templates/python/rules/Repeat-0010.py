"""Repeat-0010 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0010.md):
"An entry in a Repeat's aggregateOutputVariables must not define
appliedDimensions." Stated in Repeat's own description.md - could instead
be expressed in the schema (a dedicated AggregationCalculation variant
without appliedDimensions) and get an x-rule-id, but is left hand-written
since the schema currently reuses AggregationCalculation as-is (which does
allow appliedDimensions everywhere else it's used).

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(defines_applied_dimensions, *, value, class_name, id_value, attr, location, make_problem):
    """The dispatcher (RUNTIME's _check_repeat_own_children) has already
    checked whether this aggregateOutputVariables entry's own JSON value
    defines 'appliedDimensions' at all - defines_applied_dimensions is that
    outcome; `value` is the appliedDimensions value itself, for the
    message's own {value} (via make_problem's usual 'value' kwarg, unused
    by this rule's own message template but harmless to always pass, same
    as every other rule here)."""
    if not defines_applied_dimensions:
        return []
    return [make_problem(
        "Repeat-0010", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value})]
