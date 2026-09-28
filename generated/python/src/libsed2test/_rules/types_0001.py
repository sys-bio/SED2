"""Types-0001 (specsheets/core/Types/v1.0.0/validation/Types-0001.md): "A math
expression must be a well-formed expression under the SED2 infix grammar."

Hand-written per Design.md's Validation section: each
templates/<lang>/rules/<RuleID>.* file defines one function, named `check`
by this project's fixed function-name convention, called by name from the
generated per-field math-rule dispatcher (_check_math_field in the
generated _runtime.py - see emit_python.py). This file is copied verbatim
into every generated Python package's ._rules/ subpackage at generate time
(generator/emit_python.py's _copy_handwritten_rules_py), so it must not
import anything from that package itself - every collaborator it needs
(the parser, the exception type, the ValidationProblem constructor) comes
in as a keyword argument, which also keeps `check` callable and testable in
complete isolation, with no package assembly required.
"""
from __future__ import annotations


def check(value, *, class_name, id_value, attr, location, make_problem, math_parse, MathSyntaxError):
    """value is the field's own raw string - never a reference: the shared
    dispatcher (_check_math_field) only calls here for a literal string
    value, per this rule's own scope note (see Types-0001.md: "When the
    math attribute is itself a reference, this and the following math
    rules... apply only if the reference resolves statically to a string
    constant", out of scope until reference resolution exists).

    Returns [] if `value` parses under the SED2 math grammar (math.g4);
    otherwise a single ValidationProblem for Types-0001, with the parser's
    own error text filling the rule's {parse-message} placeholder.
    """
    try:
        math_parse(value)
    except MathSyntaxError as e:
        return [make_problem(
            "Types-0001", location, attr=attr, expr=value,
            **{"class": class_name, "id": id_value, "parse-message": str(e)},
        )]
    return []
