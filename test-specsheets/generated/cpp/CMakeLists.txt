cmake_minimum_required(VERSION 3.16)
project(sed2test CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

set(JSONCONS_BUILD_TESTS OFF CACHE BOOL "" FORCE)
FetchContent_Declare(
  jsoncons
  GIT_REPOSITORY https://github.com/danielaparker/jsoncons.git
  GIT_TAG v0.176.0
)
FetchContent_MakeAvailable(jsoncons)

# Unlike the Python/Java ANTLR targets, ANTLR's Cpp target has no
# header-only runtime option, so it must be built from source here. Its
# own CMakeLists defaults ANTLR_BUILD_CPP_TESTS to ON, which pulls in an
# internal googletest fetch (a raw-archive URL, not the git-clone-style
# access our own googletest FetchContent below uses) that this project
# does not need and that can fail against a restrictive network egress
# policy - turned off along with the other targets this library has no
# use for (demo executable, install rules, shared lib).
set(WITH_DEMO OFF CACHE BOOL "" FORCE)
set(ANTLR4_INSTALL OFF CACHE BOOL "" FORCE)
set(ANTLR_BUILD_CPP_TESTS OFF CACHE BOOL "" FORCE)
set(ANTLR_BUILD_SHARED OFF CACHE BOOL "" FORCE)
set(ANTLR_BUILD_STATIC ON CACHE BOOL "" FORCE)
FetchContent_Declare(
  antlr4
  GIT_REPOSITORY https://github.com/antlr/antlr4.git
  GIT_TAG 4.13.2
  GIT_SHALLOW TRUE
  SOURCE_SUBDIR runtime/Cpp
)
FetchContent_MakeAvailable(antlr4)

# sed2test is otherwise header-only (see generator/emit_cpp.py's module
# docstring) - the one exception is the ANTLR-generated math lexer/parser,
# which ANTLR only emits as compiled .cpp/.h pairs (see
# antlr_tool.generate_cpp_math_parser). Those few files are built into
# this small static library instead of being force-fit into the
# header-only convention, and linked into the INTERFACE library below so
# consumers of sed2test pick them up transparently.
add_library(sed2test_math STATIC
  src/antlr/mathLexer.cpp
  src/antlr/mathParser.cpp
  src/antlr/mathVisitor.cpp
  src/antlr/mathBaseVisitor.cpp
)
target_include_directories(sed2test_math PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
# ANTLR's generated .cpp files #include their sibling headers by bare name
# (e.g. #include "mathLexer.h"), not by their include/sed2test/antlr/ path,
# so that directory needs to be on the include path too - PRIVATE since
# this is purely an artifact of how the generated .cpp files are written,
# not part of sed2test_math's own public interface.
target_include_directories(sed2test_math PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include/sed2test/antlr)
target_link_libraries(sed2test_math PUBLIC antlr4_static)

# sed2test is header-only (see generator/emit_cpp.py's module docstring),
# so it is exposed as an INTERFACE library: nothing to compile here, only
# include paths and its jsoncons/sed2test_math dependencies to propagate to
# consumers.
add_library(sed2test INTERFACE)
target_include_directories(sed2test INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(sed2test INTERFACE jsoncons sed2test_math)

option(SED2TEST_BUILD_TESTS "Build the fixture test suite" ON)
if(SED2TEST_BUILD_TESTS)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.15.2
  )
  FetchContent_MakeAvailable(googletest)

  enable_testing()
  add_executable(fixture_tests tests/FixtureTest.cpp)
  target_link_libraries(fixture_tests PRIVATE sed2test GTest::gtest_main)
  # fixtures/ always lives two levels up from this file's own directory
  # (see generate.py: fixtures/ is written under dirname(--out), and cpp
  # sources under --out/cpp) - baked in here, at configure time, rather
  # than guessed at run time from the test binary's working directory
  # (which gtest_discover_tests/ctest don't guarantee the same way across
  # generators). See templates/cpp/tests/FixtureTest.cpp's fixtures_dir().
  target_compile_definitions(fixture_tests PRIVATE
    SED2_FIXTURES_DIR_DEFAULT="${CMAKE_CURRENT_SOURCE_DIR}/../../fixtures")
  include(GoogleTest)
  gtest_discover_tests(fixture_tests)
endif()
