"""SEDBase-0006 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0006.md):
"Every colon-delimited segment of a reference must resolve to an existing
element." This is the check behind getSEDReference() returning null.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(parsed, resolved, resolved_prefix, *, class_name, id_value, attr, location, make_problem):
    """parsed is the field's own _runtime.ParsedReference; `resolved` and
    `resolved_prefix` are get_sed_reference(document, parsed)'s own return
    values - the dispatcher (_check_reference_field) has already called it
    once and passes both through here rather than resolving twice.

    resolved_prefix is None only when there was no document to walk at all
    (e.g. a class validated directly, never attached to a document) - not a
    genuine resolution failure, so this rule stays silent rather than firing
    on incomplete information. Otherwise, resolved is None iff resolution
    failed, and resolved_prefix is the longest prefix that DID resolve
    (SEDBase-0006.md's own note) - the {subvalue} this rule's message uses
    in place of {location}, which the message-placeholder table reserves
    everywhere else for the offending attribute's own JSON pointer.
    """
    if resolved_prefix is None or resolved is not None:
        return []
    return [make_problem(
        "SEDBase-0006", location, attr=attr, value=parsed.raw, subvalue=resolved_prefix,
        **{"class": class_name, "id": id_value},
    )]
