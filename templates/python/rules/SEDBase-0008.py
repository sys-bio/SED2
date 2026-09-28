"""SEDBase-0008 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0008.md):
"A dot-accessor in a reference must be one the target declares valid."

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(accessor_ok, dot_name, *, value, class_name, id_value, attr, location, make_problem):
    """accessor_ok is the dispatcher's own (outputs_shape.resolve_output(),
    or its own constants/styles/loopVariables handling) resolution of
    whether this reference's suffix is a declared-valid output of its
    target - True, False, or None. Fires only on an outright False; None
    means the dispatcher couldn't determine this statically (a "valid"
    expr that depends on something not knowable ahead of time), which
    SEDBase-0008.md's own text says should leave the rule silent, same as
    False would for any of its dependent rules (SEDBase-0009 through
    -0015) - so None is deliberately NOT treated as "invalid" here."""
    if accessor_ok is not False:
        return []
    return [make_problem(
        "SEDBase-0008", location, attr=attr, value=value, subvalue=dot_name or "",
        **{"class": class_name, "id": id_value},
    )]
