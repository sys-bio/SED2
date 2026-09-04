#pragma once

// Hand-written (unlike sed2_c_api.h, which codegen/generate_ctypes.py
// generates from codegen/spec_attributes/*.json): the cross-cutting parts
// of the C API that every generated function shares, plus the handful of
// SEDBase-level functions that don't need to be generated per class at all
// - see the big comment below.

// Windows needs explicit dllexport/dllimport since MSVC doesn't export
// symbols from a shared library by default (unlike GCC/Clang, where a
// symbol is visible unless hidden); SED2_C_BUILD is defined only while
// building this library itself (the sed2_c CMake target), so anything
// that merely links against the DLL sees the dllimport form instead -
// ctypes itself never reads this header either way, only the C++ shim
// does.
#if defined(_WIN32)
#ifdef SED2_C_BUILD
#define SED2_C_API extern "C" __declspec(dllexport)
#else
#define SED2_C_API extern "C" __declspec(dllimport)
#endif
#else
#define SED2_C_API extern "C" __attribute__((visibility("default")))
#endif

#include <string>

namespace sed2_c {

// Records the most recent exception message caught at the C boundary (see
// the SED2_TRY/SED2_CATCH_* macros below) - a C++ exception can never
// safely cross into Python through ctypes, so every sed2_*() function
// catches at its own boundary instead of letting one escape. Thread-local
// in Runtime.cpp, so concurrent calls on different threads don't stomp on
// each other's error text.
void setLastError(const char* message);

// Copies 's' into a freshly malloc'd, null-terminated buffer the caller
// owns and must eventually free via sed2_free_string() - always freed
// from *this* library (never by Python's own allocator), so there is
// never a cross-CRT mismatch between the alloc and the free. Every
// string-returning function in the C API (generated ones included) uses
// this, and returns 'char*' rather than 'const char*' as a signal that
// the caller owns it - sed2_get_last_error() is the one exception, since
// its storage is static and never meant to be freed.
char* allocString(const std::string& s);

}  // namespace sed2_c

// Wraps a generated function's body: SED2_TRY opens the try block:
//   SED2_C_API T sed2_Foo_bar(...) {
//       SED2_TRY
//       ... code that may throw ...
//       SED2_CATCH_RETURN(sentinel)
//   }
// catches whatever escapes, records it via setLastError (retrievable
// through sed2_get_last_error()), and returns 'sentinel'.
// SED2_CATCH_VOID is the same for a void-returning function. See
// codegen/generate_ctypes.py, which emits one or the other around every
// generated function's body.
#define SED2_TRY try {
#define SED2_CATCH_RETURN(sentinel)                    \
    }                                                   \
    catch (const std::exception& e) {                   \
        ::sed2_c::setLastError(e.what());                \
        return sentinel;                                  \
    }                                                       \
    catch (...) {                                           \
        ::sed2_c::setLastError("sed2: unknown error");        \
        return sentinel;                                        \
    }
#define SED2_CATCH_VOID                                \
    }                                                    \
    catch (const std::exception& e) {                     \
        ::sed2_c::setLastError(e.what());                   \
    }                                                         \
    catch (...) {                                             \
        ::sed2_c::setLastError("sed2: unknown error");           \
    }

// -- Cross-cutting SEDBase-level functions ---------------------------------
// Every generated class derives from sed2::SEDBase and inherits id/name/
// description/notes unchanged, and getTypeName/fromJSON/toJSON/validate
// are all declared virtual on SEDBase (see include/sed2/core/SEDBase.h) -
// so one implementation, dispatched through a bare SEDBase*, correctly
// covers every generated class (including sed2::SEDDocument's own
// overrides) without codegen having to repeat any of this per class.
// SEDBase's virtual destructor means even destroy() can be generic: only
// construction (sed2_<Class>_create, in the generated C API) needs to
// know which concrete type to `new`.
//
// Every 'handle' below is a sed2::SEDBase* smuggled through as void* -
// passing a handle whose object doesn't actually derive from SEDBase (it
// always will, for anything the C API itself produced) is undefined
// behavior, same as any other C API built on opaque pointers.

SED2_C_API const char* sed2_get_last_error(void);  // borrowed - do not free
SED2_C_API void sed2_free_string(char* s);

SED2_C_API void sed2_SEDBase_destroy(void* handle);
SED2_C_API char* sed2_SEDBase_getTypeName(void* handle);
SED2_C_API int sed2_SEDBase_fromJSON(void* handle, const char* jsonText);  // 0 ok, -1 failed (see sed2_get_last_error)
SED2_C_API char* sed2_SEDBase_toJSON(void* handle);
SED2_C_API char* sed2_SEDBase_validate(void* handle);  // a JSON array of {code,message,path,severity}
SED2_C_API void* sed2_SEDBase_getParent(void* handle);        // borrowed, may be NULL
SED2_C_API void* sed2_SEDBase_getSEDDocument(void* handle);   // borrowed, may be NULL

SED2_C_API char* sed2_SEDBase_getId(void* handle);
SED2_C_API void sed2_SEDBase_setId(void* handle, const char* value);
SED2_C_API int sed2_SEDBase_isSetId(void* handle);
SED2_C_API void sed2_SEDBase_unsetId(void* handle);

SED2_C_API char* sed2_SEDBase_getName(void* handle);
SED2_C_API void sed2_SEDBase_setName(void* handle, const char* value);
SED2_C_API int sed2_SEDBase_isSetName(void* handle);
SED2_C_API void sed2_SEDBase_unsetName(void* handle);

SED2_C_API char* sed2_SEDBase_getDescription(void* handle);
SED2_C_API void sed2_SEDBase_setDescription(void* handle, const char* value);
SED2_C_API int sed2_SEDBase_isSetDescription(void* handle);
SED2_C_API void sed2_SEDBase_unsetDescription(void* handle);

SED2_C_API char* sed2_SEDBase_getNotes(void* handle);
SED2_C_API void sed2_SEDBase_setNotes(void* handle, const char* value);
SED2_C_API int sed2_SEDBase_isSetNotes(void* handle);
SED2_C_API void sed2_SEDBase_unsetNotes(void* handle);
