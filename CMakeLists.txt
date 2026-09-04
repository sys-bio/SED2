cmake_minimum_required(VERSION 3.16)
project(sed2 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# sed2 is a static library but also gets linked into the sed2_c shared
# library below, which needs every object in it built as position-independent
# code (no-op for MSVC, where this distinction doesn't apply).
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
  set(SED2_IS_TOP_LEVEL ON)
else()
  set(SED2_IS_TOP_LEVEL OFF)
endif()

option(SED2_BUILD_TESTS "Build the sed2 unit test suite" ${SED2_IS_TOP_LEVEL})

include(FetchContent)

# ---------------------------------------------------------------------------
# Dependencies (Design.md: nlohmann::json for the JSON DOM,
# pboettch/json-schema-validator for schema validation, both pulled via
# FetchContent so no separate compiled dependency has to be installed by
# hand on Windows/MSVC).
# ---------------------------------------------------------------------------

FetchContent_Declare(
  nlohmann_json
  GIT_REPOSITORY https://github.com/nlohmann/json.git
  GIT_TAG v3.11.3
)
FetchContent_MakeAvailable(nlohmann_json)

set(JSON_VALIDATOR_INSTALL OFF CACHE BOOL "" FORCE)
set(JSON_VALIDATOR_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(JSON_VALIDATOR_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(JSON_VALIDATOR_SHARED_LIBS OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
  json_schema_validator
  GIT_REPOSITORY https://github.com/pboettch/json-schema-validator.git
  GIT_TAG 2.4.0
)
FetchContent_MakeAvailable(json_schema_validator)

# ---------------------------------------------------------------------------
# Codegen: each file in codegen/spec_attributes/ describes one SED2 class
# (its attributes, whether each is required/a list/an owned sub-object).
# generate_classes.py turns those into include/sed2/generated/<Class>.h and
# src/generated/<Class>.cpp. Re-running happens automatically on build
# whenever a table or the generator script changes, so adding a class later
# is a data change, not a hand-written one.
# ---------------------------------------------------------------------------

find_package(Python3 COMPONENTS Interpreter REQUIRED)

file(GLOB SED2_ATTRIBUTE_TABLES CONFIGURE_DEPENDS
     "${CMAKE_CURRENT_SOURCE_DIR}/codegen/spec_attributes/*.json")

set(SED2_GENERATED_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(SED2_GENERATED_HEADERS "")
# Registrations.cpp has no attribute table of its own (generate_classes.py
# rewrites it in full on every run, aggregating whichever classes the rest
# of that run just produced), so it's listed explicitly here rather than
# derived from the codegen/spec_attributes/*.json glob below.
set(SED2_GENERATED_SOURCES "${SED2_GENERATED_DIR}/src/Registrations.cpp")
foreach(table ${SED2_ATTRIBUTE_TABLES})
  get_filename_component(class_name ${table} NAME_WE)
  list(APPEND SED2_GENERATED_HEADERS "${SED2_GENERATED_DIR}/include/sed2/generated/${class_name}.h")
  list(APPEND SED2_GENERATED_SOURCES "${SED2_GENERATED_DIR}/src/${class_name}.cpp")
endforeach()

# generate_classes.py also emits one gtest source per table into
# .../generated/tests/ (built as the separate sed2_generated_tests target -
# see tests/CMakeLists.txt), except for a "generateBaseOnly" class
# (SEDDocument today - see generate_test()'s own docstring), which has no
# test file to list here.
set(SED2_GENERATED_TEST_SOURCES "")
foreach(table ${SED2_ATTRIBUTE_TABLES})
  get_filename_component(class_name ${table} NAME_WE)
  file(READ ${table} _sed2_table_content)
  if(NOT _sed2_table_content MATCHES "\"generateBaseOnly\"[ \t]*:[ \t]*true")
    list(APPEND SED2_GENERATED_TEST_SOURCES "${SED2_GENERATED_DIR}/tests/test_${class_name}.cpp")
  endif()
  unset(_sed2_table_content)
endforeach()

add_custom_command(
  OUTPUT ${SED2_GENERATED_HEADERS} ${SED2_GENERATED_SOURCES} ${SED2_GENERATED_TEST_SOURCES}
  COMMAND ${Python3_EXECUTABLE}
          "${CMAKE_CURRENT_SOURCE_DIR}/codegen/generate_classes.py"
          --tables-dir "${CMAKE_CURRENT_SOURCE_DIR}/codegen/spec_attributes"
          --out-dir "${SED2_GENERATED_DIR}"
  DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/codegen/generate_classes.py" ${SED2_ATTRIBUTE_TABLES}
  COMMENT "sed2: generating classes and generated tests from codegen/spec_attributes"
  VERBATIM
)
add_custom_target(sed2_generate_classes DEPENDS ${SED2_GENERATED_HEADERS} ${SED2_GENERATED_SOURCES} ${SED2_GENERATED_TEST_SOURCES})

# ---------------------------------------------------------------------------
# Library
# ---------------------------------------------------------------------------

add_library(sed2
  src/core/SEDBase.cpp
  src/core/SEDDocument.cpp
  src/core/RawElement.cpp
  src/core/TypeRegistry.cpp
  src/core/AttributeTypes.cpp
  src/math/ASTNode.cpp
  src/math/Lexer.cpp
  src/math/Parser.cpp
  src/math/FunctionTable.cpp
  src/validation/SchemaValidator.cpp
  ${SED2_GENERATED_SOURCES}
)
add_dependencies(sed2 sed2_generate_classes)

target_include_directories(sed2 PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/include"
  "${SED2_GENERATED_DIR}/include"
)
target_link_libraries(sed2 PUBLIC nlohmann_json::nlohmann_json nlohmann_json_schema_validator)
target_compile_features(sed2 PUBLIC cxx_std_17)

if(MSVC)
  target_compile_options(sed2 PRIVATE /W4)
else()
  target_compile_options(sed2 PRIVATE -Wall -Wextra)
endif()

target_compile_definitions(sed2 PUBLIC
  SED2_SCHEMA_PATH="${CMAKE_CURRENT_SOURCE_DIR}/spec/sed2.schema.json"
)

# ---------------------------------------------------------------------------
# C API shim + Python ctypes bindings: codegen/generate_ctypes.py reads the
# same codegen/spec_attributes/*.json tables as generate_classes.py above,
# but binds them to a small extern "C" API (opaque handles - see
# include/sed2_c/Runtime.h for why: ctypes can't call a C++ class directly)
# and a matching sed2.py that wraps that API in one Pythonic class per SED2
# class. A separate custom command/target from sed2_generate_classes: this
# one only needs the tables themselves (not the generated C++ headers'
# content) to run, though the resulting sed2_c_api.cpp does need them to
# compile, which add_dependencies below on sed2_generate_classes ensures.
# ---------------------------------------------------------------------------

set(SED2_C_API_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated_c")
set(SED2_C_API_HEADER "${SED2_C_API_DIR}/include/sed2_c_api.h")
set(SED2_C_API_SOURCE "${SED2_C_API_DIR}/src/sed2_c_api.cpp")
set(SED2_PYTHON_BINDINGS "${SED2_C_API_DIR}/python/sed2.py")

add_custom_command(
  OUTPUT ${SED2_C_API_HEADER} ${SED2_C_API_SOURCE} ${SED2_PYTHON_BINDINGS}
  COMMAND ${Python3_EXECUTABLE}
          "${CMAKE_CURRENT_SOURCE_DIR}/codegen/generate_ctypes.py"
          --tables-dir "${CMAKE_CURRENT_SOURCE_DIR}/codegen/spec_attributes"
          --out-dir "${SED2_C_API_DIR}"
  DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/codegen/generate_ctypes.py"
          "${CMAKE_CURRENT_SOURCE_DIR}/codegen/generate_classes.py"
          ${SED2_ATTRIBUTE_TABLES}
  COMMENT "sed2: generating the C API shim and Python ctypes bindings"
  VERBATIM
)
add_custom_target(sed2_generate_ctypes DEPENDS ${SED2_C_API_HEADER} ${SED2_C_API_SOURCE} ${SED2_PYTHON_BINDINGS})

add_library(sed2_c SHARED
  src/c_api/Runtime.cpp
  ${SED2_C_API_SOURCE}
)
# sed2_c_api.cpp #includes the generated C++ class headers (sed2/generated/
# *.h) to bind against, so it needs those to exist too, not just its own
# generated files.
add_dependencies(sed2_c sed2_generate_ctypes sed2_generate_classes)

target_include_directories(sed2_c PRIVATE
  "${CMAKE_CURRENT_SOURCE_DIR}/include"
  "${SED2_GENERATED_DIR}/include"
  "${SED2_C_API_DIR}/include"
)
target_link_libraries(sed2_c PRIVATE sed2)
target_compile_features(sed2_c PRIVATE cxx_std_17)
# Only while *building* this library - see Runtime.h's dllexport/dllimport
# switch.
target_compile_definitions(sed2_c PRIVATE SED2_C_BUILD)

# Copies sed2.py next to the built sed2_c.dll/.so/.dylib so `import sed2`
# just works from that one directory (see sed2.py's own _find_library(),
# which looks next to itself first) rather than requiring a separate copy
# step by hand.
add_custom_command(TARGET sed2_c POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
          "${SED2_PYTHON_BINDINGS}" "$<TARGET_FILE_DIR:sed2_c>/sed2.py"
  COMMENT "sed2: copying sed2.py next to the built sed2_c library"
)

# ---------------------------------------------------------------------------
# Install: `cmake --install` (an INSTALL target in IDEs that generate one,
# like Visual Studio) puts the C++ library + headers under the usual
# GNUInstallDirs layout, and separately assembles <prefix>/python into a
# ready-to-package sed2 Python distribution: sed2_c's shared library and
# sed2.py (renamed to __init__.py) both land in <prefix>/python/sed2 -
# still "next to each other" the way sed2.py's own _find_library() needs
# (it looks beside itself first), just one level deeper than the build
# tree's POST_BUILD copy - and installed_setup.py lands beside that
# directory as <prefix>/python/setup.py, so `cd <prefix>/python &&
# pip install .` packages this already-built tree with no rebuild and no
# C++ toolchain required. The root setup.py's pip build reads from this
# same layout (via `cmake --install --prefix <tmp dir>`) instead of
# searching the build tree by hand.
# ---------------------------------------------------------------------------

include(GNUInstallDirs)

install(TARGETS sed2
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY "${SED2_GENERATED_DIR}/include/" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES "${SED2_C_API_HEADER}" DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS sed2_c
  RUNTIME DESTINATION python/sed2
  LIBRARY DESTINATION python/sed2
  ARCHIVE DESTINATION python/sed2
)
install(FILES "${SED2_PYTHON_BINDINGS}" DESTINATION python/sed2 RENAME __init__.py)
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/python_stub/installed_setup.py" DESTINATION python RENAME setup.py)

if(SED2_BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()
