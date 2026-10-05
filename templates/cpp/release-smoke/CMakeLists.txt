# Release smoke test for the C++ source package (see the release-cpp job in
# .github/workflows/ci.yml). Hand-written, never regenerated.
#
# Consumes the extracted release package exactly the way a user would -
# add_subdirectory() of the package root, link the libsed2::libsed2 target -
# so it proves the package is self-contained: no dependence on this
# repository's layout, no fixtures/ or tests/ directory, and the fixture test
# suite (and its googletest fetch) stays off because the package is not the
# top-level project.
#
#   cmake -S templates/cpp/release-smoke -B build \
#         -DLIBSED2_DIR=<extracted package root> -DEXPECTED_VERSION=<VERSION.txt>
cmake_minimum_required(VERSION 3.16)
project(libsed2_release_smoke CXX)

set(LIBSED2_DIR "" CACHE PATH "Root of the extracted libsed2 C++ release package")
set(EXPECTED_VERSION "" CACHE STRING "Version the package's CMakeLists.txt must declare")
if(NOT EXISTS "${LIBSED2_DIR}/CMakeLists.txt")
  message(FATAL_ERROR "LIBSED2_DIR must point at the extracted release package (got '${LIBSED2_DIR}')")
endif()

add_subdirectory("${LIBSED2_DIR}" libsed2)

get_directory_property(_pkg_version DIRECTORY "${LIBSED2_DIR}" DEFINITION libsed2_VERSION)
message(STATUS "libsed2 package declares version '${_pkg_version}'")
if(EXPECTED_VERSION AND NOT _pkg_version STREQUAL EXPECTED_VERSION)
  message(FATAL_ERROR "package declares version '${_pkg_version}', expected '${EXPECTED_VERSION}'")
endif()
if(TARGET libsed2_fixture_tests OR TARGET fixture_tests)
  message(FATAL_ERROR "the fixture test target must not be built when libsed2 is consumed as a subdirectory")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(smoke main.cpp)
target_link_libraries(smoke PRIVATE libsed2::libsed2)
