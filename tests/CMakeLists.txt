include(FetchContent)

set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)  # match sed2's CRT on MSVC

FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.15.2
)
FetchContent_MakeAvailable(googletest)

add_executable(sed2_tests
  unit/test_SEDBase.cpp
  unit/test_SEDDocument.cpp
  unit/test_ExplicitODESimulation.cpp
  unit/test_Report.cpp
  unit/test_lexer.cpp
  unit/test_parser.cpp
  unit/test_cross_references.cpp
  unit/test_schema_validation.cpp
  unit/test_simulations.cpp
  unit/test_tasks_import_data.cpp
  unit/test_repeats.cpp
  unit/test_outputs.cpp
)
target_link_libraries(sed2_tests PRIVATE sed2 GTest::gtest_main)
target_compile_features(sed2_tests PRIVATE cxx_std_17)
target_compile_definitions(sed2_tests PRIVATE
  SED2_TEST_VALID_DOCS_DIR="${CMAKE_CURRENT_SOURCE_DIR}/valid_documents"
  SED2_TEST_INVALID_DOCS_DIR="${CMAKE_CURRENT_SOURCE_DIR}/invalid_documents"
)

include(GoogleTest)
gtest_discover_tests(sed2_tests)

# One gtest source per (non-generateBaseOnly) attribute table, generated
# by codegen/generate_classes.py alongside the classes themselves - see
# SED2_GENERATED_TEST_SOURCES in the root CMakeLists.txt. Kept as its own
# target/binary, separate from the hand-written tests above, per its own
# GoogleTest discovery pass and its own failure output.
if(SED2_GENERATED_TEST_SOURCES)
  # SED2_GENERATED_TEST_SOURCES are OUTPUTs of the custom command defined
  # in the root CMakeLists.txt (a different directory than this one), so
  # their GENERATED property isn't visible here automatically without
  # raising cmake_minimum_required to 3.20+ (CMP0118) - marking it
  # explicitly avoids that requirement.
  set_source_files_properties(${SED2_GENERATED_TEST_SOURCES} PROPERTIES GENERATED TRUE)
  add_executable(sed2_generated_tests ${SED2_GENERATED_TEST_SOURCES})
  add_dependencies(sed2_generated_tests sed2_generate_classes)
  target_link_libraries(sed2_generated_tests PRIVATE sed2 GTest::gtest_main)
  target_compile_features(sed2_generated_tests PRIVATE cxx_std_17)
  gtest_discover_tests(sed2_generated_tests)
endif()
