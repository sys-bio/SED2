"""SEDBase-0017 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0017.md):
"A reference required to resolve to AnnotatedData must resolve to
AnnotatedData." Applies to every field whose schema property carries
"x-ref-target": "annotatedData" (FieldSpec.ref_target == "annotatedData").
A scalar constant (number, string, boolean) and an array constant are
AnnotatedData (an array is unlabeled AnnotatedData); an object constant and
a model are not.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(resolved_kind, resolved_description, *, value, class_name, id_value, attr, location, make_problem):
    """resolved_kind is "annotatedData", "model", "object", or None when
    what the reference resolves to is not statically known (silent then).
    Only AnnotatedData is acceptable."""
    if resolved_kind is None or resolved_kind == "annotatedData":
        return []
    return [make_problem(
        "SEDBase-0017", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value, "resolved-value": resolved_description},
    )]
