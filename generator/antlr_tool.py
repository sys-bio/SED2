"""Runs the ANTLR4 tool (pinned version - see Design.md's Toolchain section,
"ANTLR is a deliberate exception to 'no pinned version numbers'") against
generator/math.g4 and writes the generated Python3 lexer/parser into a
target package's _antlr/ subpackage.

The ANTLR tool itself is a Java jar and is a build-time-only dependency of
the *generator*, never of any generated library (Design.md's Parser
Strategy) - callers of the generated libsed2 package only need the small
ANTLR4 Python runtime (antlr4-python3-runtime, the same pinned version),
which is declared as an ordinary pyproject.toml dependency, not fetched by
this module.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import urllib.request

# Pinned together with the antlr4-python3-runtime version in
# emit_python.py's pyproject.toml dependency list - see Design.md's
# Toolchain section on why these can't drift independently.
ANTLR_VERSION = "4.13.2"
ANTLR_JAR_URL = (
    f"https://repo1.maven.org/maven2/org/antlr/antlr4/{ANTLR_VERSION}/"
    f"antlr4-{ANTLR_VERSION}-complete.jar"
)
_DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "sed2-generator")
_JAR_NAME = f"antlr-{ANTLR_VERSION}-complete.jar"

GRAMMAR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "math.g4")


def ensure_antlr_jar(cache_dir: str | None = None) -> str:
    """Downloads the pinned ANTLR tool jar from Maven Central into a local
    cache dir (idempotent - reused across generate.py runs) and returns its
    path. Raises whatever urllib raises if the network is unreachable; there
    is no vendored fallback copy, matching every other unpinned dependency's
    "fetched at build time" treatment elsewhere in this project."""
    cache_dir = cache_dir or _DEFAULT_CACHE_DIR
    os.makedirs(cache_dir, exist_ok=True)
    jar_path = os.path.join(cache_dir, _JAR_NAME)
    if not os.path.isfile(jar_path) or os.path.getsize(jar_path) == 0:
        tmp_path = jar_path + ".tmp"
        urllib.request.urlretrieve(ANTLR_JAR_URL, tmp_path)
        os.replace(tmp_path, jar_path)
    return jar_path


def generate_python_math_parser(dest_pkg_dir: str, cache_dir: str | None = None) -> None:
    """Invokes the ANTLR tool on math.g4 for the Python3 target and writes
    mathLexer.py / mathParser.py / mathVisitor.py (plus a small __init__.py)
    into dest_pkg_dir - normally <package>/_antlr/ inside the generated
    Python package. Raises RuntimeError with the tool's own stdout/stderr on
    any grammar or tool-invocation failure."""
    jar_path = ensure_antlr_jar(cache_dir)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            "java", "-jar", jar_path,
            "-Dlanguage=Python3", "-visitor", "-no-listener",
            "-Xexact-output-dir",
            "-o", tmp,
            GRAMMAR_PATH,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                "ANTLR tool failed on generator/math.g4:\n"
                f"{result.stdout}\n{result.stderr}"
            )
        os.makedirs(dest_pkg_dir, exist_ok=True)
        for name in ("mathLexer.py", "mathParser.py", "mathVisitor.py"):
            shutil.copyfile(os.path.join(tmp, name), os.path.join(dest_pkg_dir, name))
    with open(os.path.join(dest_pkg_dir, "__init__.py"), "w") as f:
        f.write(
            '"""ANTLR4-generated math lexer/parser (see generator/math.g4). '
            'GENERATED - do not hand-edit; regenerate via generator/generate.py."""\n'
        )
