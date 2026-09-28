"""SEDDocument-0010 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0010.md):
"A <prefix>@version attribute should not be declared for a namespace the
document never uses." A warning, not an error - harmless but likely a
leftover (see the rule's own body text).

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(*, prefix, location, make_problem):
    """Called once per declared-but-unused prefix - the caller
    (_check_namespace_usage_and_version) has already confirmed `prefix` has
    a "<prefix>@version" declared on the document but no usage site
    anywhere in the document tree; `location` is the declaration's own
    JSON pointer ("/<prefix>@version")."""
    return [make_problem("SEDDocument-0010", location, prefix=prefix, attr=f"{prefix}@version")]
