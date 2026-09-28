"""SEDDocument-0011 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0011.md):
"The version of a SEDDocument should not be newer than the newest document
version this library knows." Version resolution picks the newest version
directory not greater than the document's own version, so a document
claiming a newer version than this library was generated to understand
would otherwise silently validate against the wrong (older) rule set with
no warning at all - this rule makes that visible.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations

import re

_VERSION_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def _version_tuple(value):
    m = _VERSION_RE.match(value) if isinstance(value, str) else None
    return tuple(int(g) for g in m.groups()) if m else None


def check(*, document, make_problem):
    """`document._MAX_KNOWN_DOCUMENT_VERSION` is a class-level constant the
    generator bakes in at generate time (the newest version directory this
    run's specsheets/ tree actually had for the document class - see
    spec.py's SpecModel.document_version). A document with no `version` set
    at all, or one that doesn't match the v#.#.# pattern, is already
    reported by SEDDocument's own required-field/pattern rules elsewhere -
    this rule only compares two well-formed versions, and stays silent
    otherwise rather than duplicating those."""
    max_v = document._MAX_KNOWN_DOCUMENT_VERSION
    if max_v is None or not document.is_set_version():
        return []
    value = document.get_version()
    vt, mt = _version_tuple(value), _version_tuple(max_v)
    if vt is None or mt is None or vt <= mt:
        return []
    return [make_problem("SEDDocument-0011", "/version", value=value, max=max_v)]
