"""AbstractTask-0003 (specsheets/tasks/AbstractTask/v1.0.0/validation/AbstractTask-0003.md):
"A task may only reference constants, tasks that appear earlier in the same
tasks dictionary, or (for a subTask) the elements listed in this rule's
explanation." core-spec.md Section 3's chronological rule, made checkable.

For a task at the top level of SEDDocument.tasks, a reference may target:
constants; or a task appearing earlier in SEDDocument.tasks.

For a subTask of a Repeat R, a reference may additionally target: an
earlier sibling subTask of R; anything R itself was allowed to reference
(recursively); or R itself, or any Repeat enclosing R, but only through
.range/.index or a loopVariables child (SEDBase-0013's own scoping still
separately governs THAT).

A task never references itself. Only ever checked for a `#tasks:...`
reference (references to constants are unconstrained by this rule; a
reference from an Output/Style element is likewise unconstrained, since
core-spec.md Section 3 says outputs always come chronologically after
every task).

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ok, *, value, class_name, id_value, attr, location, make_problem):
    """The dispatcher (RUNTIME's _check_task_order) has already walked both
    the referring element's own and the reference's resolved target's
    chronological position within SEDDocument.tasks (through any
    Repeat-family subTasks nesting) and compared them per this rule's own
    worked-out cases above - ok is that comparison's own outcome."""
    if ok:
        return []
    return [make_problem(
        "AbstractTask-0003", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value})]
