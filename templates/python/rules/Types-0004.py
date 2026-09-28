"""Types-0004 (specsheets/core/Types/v1.0.0/validation/Types-0004.md): "Every
bare identifier in a math expression must be a predefined constant."

See Types-0001.py's module docstring for the shared conventions (fixed
`check` function name, no package-relative imports, copied verbatim into
every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(ast, *, class_name, id_value, attr, location, make_problem, constants):
    """Same ast contract as Types-0002.py's check() - see its docstring.
    `constants` is generator-compiled from schema/predefined-functions.json's
    "constants" array (see _predefined_functions.CONSTANTS): pi,
    exponentiale, true, false, notanumber, infinity.

    Fires once per bare NAME node (an identifier that isn't part of a
    function call - see math_ast.ASTNodeType.NAME) whose text isn't one of
    those constants: SED2 math has no free variables, so anything else must
    be written as a #reference instead (Types-0004.md's own note - this
    catches the common mistake of writing 'S1' instead of
    "#tasks:sim1['S1']").
    """
    problems = []
    for node in ast.walk():
        if node.is_name() and node.name not in constants:
            problems.append(make_problem(
                "Types-0004", location, attr=attr, value=node.name,
                **{"class": class_name, "id": id_value},
            ))
    return problems
