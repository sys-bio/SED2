# Emscripten build of the libsed2 C++ library: one self-contained libsed2.js with the
# WebAssembly embedded. GENERATED - do not hand-edit; regenerate via
# generator/generate.py (generator/emit_js.py; the pattern is libantimonyjs's).
#
#   emcmake cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
#   cmake --build build            # -> build/libsed2.js
#
# The C++ library is pulled in from ../cpp (add_subdirectory, so its fixture
# test target stays off); its own FetchContent dependencies (jsoncons, the
# ANTLR4 C++ runtime) are built for WebAssembly along with it.
cmake_minimum_required(VERSION 3.16)
project(libsed2_js VERSION 0.1.0 LANGUAGES CXX)

if(NOT EMSCRIPTEN)
  message(FATAL_ERROR "Build this project with Emscripten: emcmake cmake -S . -B build")
endif()

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
set(CMAKE_CXX_FLAGS_RELEASE "-Oz -DNDEBUG")

# The C++ library, jsoncons and the ANTLR runtime all use C++ exceptions, so
# they are enabled for every target, including the FetchContent'd ones.
add_compile_options(-fexceptions)
add_link_options(-fexceptions)

add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/../cpp" cpp)

# The target is libsed2_js because libsed2 is already the C++ library's own target.
add_executable(libsed2_js src/api.cpp src/generated_api.cpp)
target_link_libraries(libsed2_js PRIVATE libsed2::libsed2)
set_target_properties(libsed2_js PROPERTIES OUTPUT_NAME libsed2 SUFFIX ".js")
target_link_options(libsed2_js PRIVATE
  -sDISABLE_EXCEPTION_CATCHING=0
  -sMODULARIZE=1
  -sSINGLE_FILE=1
  -sEXPORT_NAME=libsed2
  -sALLOW_MEMORY_GROWTH=1
  -sEXPORTED_FUNCTIONS=_sed2_library_version,_sed2_document_version,_sed2_class_names,_sed2_direct_only_keys,_sed2_rule_catalog,_sed2_validate_document,_sed2_validate_object,_sed2_normalize_document,_sed2_check_math,_malloc,_free
  -sEXPORTED_RUNTIME_METHODS=cwrap,ccall,UTF8ToString,stringToUTF8,lengthBytesUTF8
)
