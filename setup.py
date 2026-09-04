"""Makes 'pip install .' produce a working 'sed2' Python package.

sed2 has no source of its own in Python - what gets installed is exactly
what CMake's own INSTALL target already produces (see CMakeLists.txt's
install() calls): a python/sed2/ directory holding __init__.py (the
generated sed2.py, renamed) and the sed2_c native library it loads,
sitting side by side (sed2.py's own loader looks for the library next to
itself - see _find_library() in the generated file). BuildPy below drives
`cmake --build` then `cmake --install` into a scratch prefix and copies
that whole directory into the installed package; python_stub/sed2/
__init__.py is just a placeholder setuptools needs to recognize 'sed2' as
a real package before BuildPy overwrites it with the generated content.
(CMake's install() also drops a second, simpler setup.py - see
python_stub/installed_setup.py - next to that same python/sed2/
directory, for packaging an already-built install tree with no rebuild;
this one is for building from source.)

Not wired up for editable installs (`pip install -e .`) - those skip the
build step this depends on.
"""
import os
import shutil
import subprocess
from pathlib import Path

from setuptools import Distribution, setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        """sed2_c is loaded via ctypes, not linked as a CPython extension,
        so the wheel isn't actually tied to the Python version/ABI that
        built it - only to the OS/architecture the native library was
        compiled for. Without this override, has_ext_modules()=True above
        (needed so pip picks a platform-specific wheel at all) also makes
        bdist_wheel tag it to the current interpreter, e.g.
        cp312-cp312-win_amd64, which is needlessly narrow: py3-none-
        win_amd64 installs under any CPython 3."""

        def get_tag(self):
            _python, _abi, plat = super().get_tag()
            return "py3", "none", plat

except ImportError:  # wheel isn't installed - only bdist_wheel needs it
    bdist_wheel = None

ROOT = Path(__file__).parent.resolve()
CMAKE_BUILD_DIR = ROOT / "build" / "python-package"
CMAKE_INSTALL_DIR = CMAKE_BUILD_DIR / "install"


class BuildPy(_build_py):
    def run(self):
        super().run()  # copies the python_stub/sed2/__init__.py placeholder into build_lib
        self._build_and_install_native()
        self._copy_into_package(Path(self.build_lib) / "sed2")

    def _build_and_install_native(self):
        cmake = shutil.which("cmake")
        if not cmake:
            raise RuntimeError(
                "cmake was not found on PATH - it's required to build sed2's "
                "C++ core and C API shim. Install it (and a C++17 compiler) "
                "and re-run pip install."
            )
        CMAKE_BUILD_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.check_call([
            cmake, "-S", str(ROOT), "-B", str(CMAKE_BUILD_DIR),
            "-DCMAKE_BUILD_TYPE=Release",
            "-DSED2_BUILD_TESTS=OFF",
        ])
        subprocess.check_call([
            cmake, "--build", str(CMAKE_BUILD_DIR),
            "--target", "sed2_c",
            "--config", "Release",
            "-j", str(os.cpu_count() or 2),
        ])
        subprocess.check_call([
            cmake, "--install", str(CMAKE_BUILD_DIR),
            "--prefix", str(CMAKE_INSTALL_DIR),
            "--config", "Release",
        ])

    def _copy_into_package(self, dest):
        installed = CMAKE_INSTALL_DIR / "python" / "sed2"
        shutil.copytree(installed, dest, dirs_exist_ok=True)


class BinaryDistribution(Distribution):
    """Marks the wheel as platform-specific (e.g. win_amd64) rather than
    a pure-Python 'any' wheel, since it bundles a compiled native library."""

    def has_ext_modules(self):
        return True


_cmdclass = {"build_py": BuildPy}
if bdist_wheel is not None:
    _cmdclass["bdist_wheel"] = bdist_wheel

setup(
    name="sed2",
    version="0.1.0",
    description="Python bindings for the SED2 C++ library",
    packages=["sed2"],
    package_dir={"sed2": "python_stub/sed2"},
    distclass=BinaryDistribution,
    cmdclass=_cmdclass,
    zip_safe=False,
    python_requires=">=3.8",
)
