"""Types-0002 (specsheets/core/Types/v1.0.0/validation/Types-0002.md): "Every
function called in a math expression must be defined in the
predefined-functions registry."

See Types-0001.py's module docstring for the shared conventions (fixed
`check` function name, no package-relative imports, copied verbatim into
every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ast, *, class_name, id_value, attr, location, make_problem, functions):
    """ast is the already-parsed ASTNode tree for a math field's literal
    string value (Types-0001 has already run and found it well-formed - the
    dispatcher skips this rule otherwise, since there is nothing to walk).
    `functions` is generator-compiled from schema/predefined-functions.json
    (see emit_python.py's emit_predefined_functions_py / _predefined_functions.FUNCTIONS)
    - a dict of every callable name (the SBML L3 Core MathML subset's call
    forms, the 12 distrib functions, and sum) mapped to its allowed arity;
    only the keys matter here, arity is Types-0003's concern.

    Fires once per FUNCTION_CALL node in the tree whose name isn't a key of
    `functions` - this also catches every desugared operator (relational
    chains, &&/||, unary/infix !, infix % as rem()), since math_ast.py
    desugars all of those into FUNCTION_CALL nodes before this ever runs.
    """
    problems = []
    for node in ast.walk():
        if node.is_function_call() and node.name not in functions:
            problems.append(make_problem(
                "Types-0002", location, attr=attr, function=node.name,
                **{"class": class_name, "id": id_value},
            ))
    return problems
