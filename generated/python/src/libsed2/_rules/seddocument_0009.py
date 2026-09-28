"""SEDDocument-0009 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0009.md):
"For every namespace prefix used anywhere in the document, SEDDocument must
declare a <prefix>@version attribute." Enforces Design.md's Namespaces
section: a used namespace's schema can evolve on its own timeline, so a
document must pin which version of it was written against.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(*, prefix, location, make_problem):
    """Called once per usage site of an undeclared-version namespace prefix
    (an attribute key or _type value of the form prefix@identifier) - the
    caller (_check_namespace_usage_and_version, a whole-document scan) has
    already determined `prefix` has no matching "<prefix>@version" on the
    document and found this one `location` where it's used; `location` is
    that usage's own JSON pointer, not the (missing) declaration's."""
    return [make_problem("SEDDocument-0009", location, prefix=prefix)]
