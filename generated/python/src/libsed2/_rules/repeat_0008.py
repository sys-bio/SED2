"""Repeat-0008 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0008.md):
"Every value in a Repeat's outputVariableMap must reference one of that
Repeat's own subTasks, or an output of one." outputVariableMap defines the
columns of the Repeat's [id] output, each collected from a subTask per
iteration; the reference's own accessor/index chain is checked as usual by
SEDBase-0008 through -0011 (already wired generically for every reference-
capable field - see RUNTIME's own DictOrRef-entries branch in
_validate_own). This rule only adds the one thing that's specific to
Repeat: the reference's ultimate task-level target must be one of THIS
Repeat's own direct subTasks.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ok, *, value, class_name, id_value, attr, location, make_problem):
    """The dispatcher (RUNTIME's _check_repeat_own_children) has already
    resolved the entry's own reference and checked whether its target's
    immediate parent is this Repeat instance itself (get_parent() is self)
    - ok is that outcome. `attr` here is the outputVariableMap ENTRY's own
    key (the message's own "Entry '{attr}'" wording), not the field name
    "outputVariableMap" itself."""
    if ok:
        return []
    return [make_problem(
        "Repeat-0008", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value})]
