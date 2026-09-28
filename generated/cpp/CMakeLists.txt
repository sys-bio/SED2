cmake_minimum_required(VERSION 3.16)
project(libsed2 CXX)

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

# libsed2 is header-only (see generator/emit_cpp.py's module docstring),
# so it is exposed as an INTERFACE library: nothing to compile here, only
# include paths and its jsoncons dependency to propagate to consumers.
add_library(libsed2 INTERFACE)
target_include_directories(libsed2 INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(libsed2 INTERFACE jsoncons)

option(LIBSED2_BUILD_TESTS "Build the fixture test suite" ON)
if(LIBSED2_BUILD_TESTS)
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
  target_link_libraries(fixture_tests PRIVATE libsed2 GTest::gtest_main)
  include(GoogleTest)
  gtest_discover_tests(fixture_tests)
endif()
