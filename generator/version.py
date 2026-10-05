"""The library version, read from VERSION.txt at the repository root.

VERSION.txt is the single source of truth for the version of the generated
libraries (the Python wheel, the Java jar / Maven artifact, and the C++ CMake
project all take their version from it, via generate.py). It is NOT the SED2
document-format version (SEDDocument's "version" attribute, see Design.md's
Versioning section) - the two are independent.

The format is strictly MAJOR.MINOR.PATCH (digits only, no leading "v", no
pre-release suffix): that is the one shape valid unchanged in PEP 440 (Python),
Maven, and CMake's project(VERSION ...).
"""
import os
import re

VERSION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "VERSION.txt")

_VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def check_version(text: str, source: str = "version") -> str:
    """Return text stripped of surrounding whitespace if it is MAJOR.MINOR.PATCH,
    else raise ValueError naming source."""
    v = text.strip()
    if not _VERSION_RE.match(v):
        raise ValueError(
            f"{source} must be MAJOR.MINOR.PATCH (digits only, e.g. 0.1.0), got {v!r}")
    return v


def library_version(path: str = VERSION_FILE) -> str:
    """The library version recorded in VERSION.txt."""
    with open(path) as f:
        return check_version(f.read(), path)
