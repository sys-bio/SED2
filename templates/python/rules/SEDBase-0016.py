"""SEDBase-0016 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0016.md):
"A reference required to resolve to a model must resolve to a model."
Applies to every field whose schema property carries "x-ref-target": "model"
(FieldSpec.ref_target == "model"); the shared dispatcher in emit_python.py's
RUNTIME (_check_output_shape_and_ref_type / _check_constant_accessor) works
out what the reference resolved to and calls this.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(resolved_kind, resolved_description, *, value, class_name, id_value, attr, location, make_problem):
    """resolved_kind is "model", "annotatedData", "object", or None when
    what the reference resolves to is not statically known (nothing to
    say then, same "only fires when computable" convention as
    SEDBase-0008 through -0015). Only a model is acceptable."""
    if resolved_kind is None or resolved_kind == "model":
        return []
    return [make_problem(
        "SEDBase-0016", location, attr=attr, value=value,
        **{"class": class_name, "id": id_value, "resolved-value": resolved_description},
    )]
