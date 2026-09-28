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
        # ANTLR embeds whatever grammar-file argument it's given verbatim in
        # every generated file's "# Generated from <...> by ANTLR <ver>"
        # header comment. GRAMMAR_PATH is absolute (derived from this
        # module's own __file__), so passing it directly would bake in
        # wherever THIS repo happens to be checked out - different on every
        # machine/CI runner (e.g. /home/runner/work/SED2/SED2/... on GitHub
        # Actions vs. a contributor's own checkout path), producing a
        # spurious diff in the generated output on every regeneration even
        # when math.g4 itself hasn't changed. Passing just the grammar's
        # bare filename, with cwd set to its directory, makes that header
        # comment ("# Generated from math.g4 by ANTLR 4.13.2") identical
        # everywhere - see Design.md's determinism note on generated output
        # needing to be byte-identical across repeated/cross-machine runs.
        cmd = [
            "java", "-jar", jar_path,
            "-Dlanguage=Python3", "-visitor", "-no-listener",
            "-Xexact-output-dir",
            "-o", tmp,
            os.path.basename(GRAMMAR_PATH),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=os.path.dirname(GRAMMAR_PATH)
        )
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


def generate_java_math_parser(dest_pkg_dir: str, package: str, cache_dir: str | None = None) -> None:
    """Invokes the ANTLR tool on math.g4 for the Java target and writes
    mathLexer.java / mathParser.java / mathVisitor.java / mathBaseVisitor.java
    into dest_pkg_dir - normally <package-dir>/antlr/ inside the generated
    Java package (see emit_java.py's MathAst.java, which imports from
    <package>.antlr, mirroring generate_python_math_parser's ._antlr
    placement). `package` is the Java package declaration ANTLR bakes into
    each generated file's own `package ...;` line - callers pass
    "<java_package>.antlr" so these files compile as a subpackage of the
    caller's chosen package (see emit_java_package's java_package option).
    Raises RuntimeError with the tool's own stdout/stderr on any grammar or
    tool-invocation failure, same as generate_python_math_parser."""
    jar_path = ensure_antlr_jar(cache_dir)
    with tempfile.TemporaryDirectory() as tmp:
        # Same -Xexact-output-dir + bare-filename + cwd=grammar-dir trick as
        # generate_python_math_parser, for the same reason: a deterministic
        # "# Generated from math.g4 by ANTLR ..." header regardless of where
        # this repo is checked out. -package makes ANTLR emit `package
        # <package>;` in each file instead of leaving it off.
        cmd = [
            "java", "-jar", jar_path,
            "-Dlanguage=Java", "-visitor", "-no-listener",
            "-package", package,
            "-Xexact-output-dir",
            "-o", tmp,
            os.path.basename(GRAMMAR_PATH),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=os.path.dirname(GRAMMAR_PATH)
        )
        if result.returncode != 0:
            raise RuntimeError(
                "ANTLR tool failed on generator/math.g4 (Java target):\n"
                f"{result.stdout}\n{result.stderr}"
            )
        os.makedirs(dest_pkg_dir, exist_ok=True)
        for name in ("mathLexer.java", "mathParser.java", "mathVisitor.java", "mathBaseVisitor.java"):
            shutil.copyfile(os.path.join(tmp, name), os.path.join(dest_pkg_dir, name))


def generate_cpp_math_parser(dest_include_dir: str, dest_src_dir: str, namespace: str,
                              cache_dir: str | None = None) -> None:
    """Invokes the ANTLR tool on math.g4 for the Cpp target and splits its
    output the way the rest of the generated C++ library is laid out
    (headers under include/<ns>/antlr/, the one bit of actual compiled
    source under src/antlr/ - see emit_cpp.py's _cmake_lists, which links
    those .cpp files into a small static library alongside the fetched
    ANTLR4 C++ runtime, since ANTLR's C++ target has no header-only mode
    unlike this library's own hand-written headers). `namespace` is the
    C++ namespace ANTLR bakes into each generated file's own `namespace
    ...  { ... }` block - callers pass "<cpp_namespace>::antlr" so this
    nests as a subnamespace of the caller's chosen namespace (ANTLR's
    -package flag accepts "::"-separated C++ namespaces directly, same
    flag as generate_java_math_parser's dotted Java package). Raises
    RuntimeError with the tool's own stdout/stderr on any grammar or
    tool-invocation failure, same as the other two generate_*_math_parser
    functions."""
    jar_path = ensure_antlr_jar(cache_dir)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            "java", "-jar", jar_path,
            "-Dlanguage=Cpp", "-visitor", "-no-listener",
            "-package", namespace,
            "-Xexact-output-dir",
            "-o", tmp,
            os.path.basename(GRAMMAR_PATH),
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=os.path.dirname(GRAMMAR_PATH)
        )
        if result.returncode != 0:
            raise RuntimeError(
                "ANTLR tool failed on generator/math.g4 (Cpp target):\n"
                f"{result.stdout}\n{result.stderr}"
            )
        os.makedirs(dest_include_dir, exist_ok=True)
        os.makedirs(dest_src_dir, exist_ok=True)
        for base in ("mathLexer", "mathParser", "mathVisitor", "mathBaseVisitor"):
            shutil.copyfile(os.path.join(tmp, base + ".h"), os.path.join(dest_include_dir, base + ".h"))
            shutil.copyfile(os.path.join(tmp, base + ".cpp"), os.path.join(dest_src_dir, base + ".cpp"))
