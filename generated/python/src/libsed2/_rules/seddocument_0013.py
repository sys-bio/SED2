"""SEDDocument-0013 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0013.md):
"A constant may only reference constants that appear before it in the
constants dictionary." constants is described as coming before tasks in
file order, so a constant referencing a later (or nonexistent) constant, or
itself, would break that chronological execution principle -
AbstractTask-0003 applies the same idea to tasks (not yet implemented -
see Task #10's tracked scope, which needs a per-origin-class dispatch
mechanism this rule doesn't, since SEDDocument is a real generated class).

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(*, document, make_problem, is_reference, parse_reference):
    """`is_reference`/`parse_reference` are passed in rather than imported
    (this file never imports its own package) - the same shape as every
    other handwritten rule's collaborator-injection convention (see
    _check_math_field's own docstring for why). Only a constant whose own
    value IS a reference (AnyValueOrRef's SIdRef-substitution case) is in
    scope; a plain JSON value constant has nothing to check. A reference
    that isn't even shaped like '#constants:...', or whose target constant
    doesn't precede this one in `document`'s own insertion order (including
    one that doesn't exist as a constant at all, or names this same
    constant) is "not an earlier constant" by this rule's own wording,
    without a separate resolution check first."""
    problems = []
    ids = document.get_constants()
    for i, cid in enumerate(ids):
        value = document.get_constants_item(cid)
        if not is_reference(value):
            continue
        parsed = parse_reference(value)
        if parsed.collection is None:
            continue
        if parsed.collection != "constants":
            # A reference into any other collection (for example a task) is
            # by definition not an earlier constant.
            problems.append(make_problem(
                "SEDDocument-0013", f"/constants/{cid}", attr=cid, value=value))
            continue
        if not parsed.path:
            continue
        target = parsed.path[0]
        if target not in ids[:i]:
            problems.append(make_problem(
                "SEDDocument-0013", f"/constants/{cid}", attr=cid, value=value))
    return problems
