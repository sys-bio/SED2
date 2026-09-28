"""SEDBase-0013 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0013.md):
"A reference to a Repeat's subTasks, its .range/.index outputs, or one of
its loop variables is only legal when the element holding the reference is
that Repeat itself, or lies within that Repeat's own subTasks (at any
depth, including through a nested Repeat)."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(in_scope, target_repeat_id, *, value, class_name, id_value, location, make_problem):
    """The dispatcher has already worked out which Repeat (if any) scopes
    this reference and whether the referring element (self, in
    _validate_own) is that Repeat itself or lies within its own subTasks at
    any depth (in_scope) - a plain containment-tree ancestor walk, nothing
    here depends on outputs.json/shape at all. Fires once when a scoped
    reference reaches outside its Repeat; target_repeat_id feeds the
    message's {resolved-value} (SEDBase-0013.md's own message template
    doesn't use {attr}, unlike every other SEDBase rule, since the
    violation is about the reference's LOCATION relative to the Repeat, not
    about which attribute happened to carry it)."""
    if in_scope:
        return []
    return [make_problem(
        "SEDBase-0013", location, value=value,
        **{"class": class_name, "id": id_value, "resolved-value": target_repeat_id},
    )]
