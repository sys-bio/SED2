#!/usr/bin/env python3
"""Generates a C API shim (extern "C" functions over opaque handles) and a
matching Python ctypes binding module from the same codegen/
spec_attributes/*.json tables generate_classes.py turns into C++ classes.

Why a shim at all: ctypes can only call plain C functions - a C++ class's
methods aren't part of the C ABI (name mangling, virtual dispatch, and
non-POD parameter/return types like std::string, std::vector, or
std::unique_ptr all fall outside it). So every generated C++ class gets a
small set of extern "C" functions wrapping it behind a `void*` handle, and
that C API is what the generated Python module actually calls through
ctypes.CDLL - see include/sed2_c/Runtime.h for the hand-written parts this
generated code builds on (the SED2_C_API export macro, the SED2_TRY/
SED2_CATCH_* exception-boundary macros, and the SEDBase-level functions
that are the same for every class and so don't need to be generated at
all - getTypeName/fromJSON/toJSON/validate are virtual, and the destructor
is too, so one implementation dispatched through a bare SEDBase* covers
every generated class).

Ownership crosses the C boundary as raw pointers with two different
lifetimes, matching the two different kinds of pointer the C++ side
already has:
  - "owned": a handle from sed2_<Class>_create() (or sed2_SEDDocument_
    fromFile/fromJSONString), which the caller must eventually pass to
    sed2_SEDBase_destroy() - unless it hands the handle to a C++ parent
    through an owning setter/add (an "owned"/"ownedArray"/"polymorphicList"
    attribute), at which point the *parent* owns it and destroying it
    again would double-free. The generated Python wrapper tracks this with
    an `_owns` flag (see SED2BASE_PY below) rather than leaving it to the
    caller to get right.
  - "borrowed": a handle returned by a getter for one of those same
    attribute kinds (or by getParent()/getSEDDocument()) - valid only as
    long as the owning object is, and never destroyed by the caller.

A scalar/scalarList/map attribute crosses as a JSON string instead of a
typed value: nlohmann already has to_json/from_json for every cppType this
generator uses (std::string, double, bool, int64_t, Json itself, and
ValueOrRef<T> - see AttributeTypes.h), so marshaling everything through
one JSON-text convention avoids a combinatorial explosion of per-type C
functions, at the cost of one dump()/parse() per call - fine for a
bindings layer.

Every string a C function *returns* is heap-allocated (via sed2_c::
allocString, itself using plain malloc/memcpy) and the caller must free it
with sed2_free_string() - always from *this* library, so there's never a
cross-CRT mismatch between the allocation and the free. See Runtime.h/.cpp
for the one exception (sed2_get_last_error(), whose storage is static).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_classes as gc  # noqa: E402  (path insert must come first)


# -- naming ------------------------------------------------------------------

def snake(name):
    """camelCase/PascalCase -> snake_case, for Python method/parameter
    names (kisaoID -> kisao_id, outputVariableMap -> output_variable_map).
    The C API keeps the C++ method names as-is (sed2_Report_getData) since
    it's an implementation detail most callers only ever see through the
    Python wrapper.
    """
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    return s.lower()


def c_func(class_name, suffix):
    return f"sed2_{class_name}_{suffix}"


# -- C shim: per-attribute emitters ------------------------------------------
# Each returns (header_decls: list[str], source_defs: list[str]).
# 'cpp' is the fully-qualified C++ type this table's class binds to
# (sed2::<ClassName>, or sed2::SEDDocument for the one generateBaseOnly
# table - see cpp_qualified_for() below); 'obj' is the C++ expression for
# "the object this handle names", already cast and ready to call methods
# on.

BASE_STRING_ATTRS_PY_ONLY = ("id", "name", "description", "notes")  # handled by Runtime.h, not generated


def _string_getter(fn, obj, expr):
    return [
        f"SED2_C_API char* {fn}(void* handle) {{",
        "    SED2_TRY",
        f"    auto* obj = {obj};",
        f"    return sed2_c::allocString({expr});",
        "    SED2_CATCH_RETURN(nullptr)",
        "}",
    ]


def emit_scalar(cpp, class_name, attr):
    m, T = attr.method, attr.cpp_type
    get_fn, set_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"set{m}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls, defs = [], []

    if T == "std::string":
        decls += [f"SED2_C_API char* {get_fn}(void* handle);", f"SED2_C_API void {set_fn}(void* handle, const char* value);"]
        defs += _string_getter(get_fn, f"static_cast<{cpp}*>(handle)", f"obj->get{m}()")
        defs += [
            f"SED2_C_API void {set_fn}(void* handle, const char* value) {{",
            "    SED2_TRY",
            f"    static_cast<{cpp}*>(handle)->set{m}(value ? value : \"\");",
            "    SED2_CATCH_VOID",
            "}",
        ]
    elif T == "Json":
        decls += [f"SED2_C_API char* {get_fn}(void* handle);", f"SED2_C_API void {set_fn}(void* handle, const char* jsonValue);"]
        defs += _string_getter(get_fn, f"static_cast<{cpp}*>(handle)", f"obj->get{m}().dump()")
        defs += [
            f"SED2_C_API void {set_fn}(void* handle, const char* jsonValue) {{",
            "    SED2_TRY",
            f"    static_cast<{cpp}*>(handle)->set{m}(sed2::Json::parse(jsonValue));",
            "    SED2_CATCH_VOID",
            "}",
        ]
    elif T in gc.VALUE_OR_REF_TYPES:
        u = gc.VALUE_OR_REF_UNDERLYING[T]
        c_u = {"double": "double", "int64_t": "int64_t", "bool": "int"}[u]
        isref_fn, val_fn, ref_fn = c_func(class_name, f"get{m}_isRef"), c_func(class_name, f"get{m}_value"), c_func(class_name, f"get{m}_refValue")
        setval_fn, setref_fn = c_func(class_name, f"set{m}_value"), c_func(class_name, f"set{m}_ref")
        decls += [
            f"SED2_C_API int {isref_fn}(void* handle);",
            f"SED2_C_API {c_u} {val_fn}(void* handle);",
            f"SED2_C_API char* {ref_fn}(void* handle);",
            f"SED2_C_API void {setval_fn}(void* handle, {c_u} value);",
            f"SED2_C_API void {setref_fn}(void* handle, const char* ref);",
        ]
        cast_val = "" if u != "bool" else ""
        defs += [
            f"SED2_C_API int {isref_fn}(void* handle) {{",
            "    SED2_TRY",
            f"    return static_cast<{cpp}*>(handle)->get{m}().isRef ? 1 : 0;",
            "    SED2_CATCH_RETURN(0)",
            "}",
            f"SED2_C_API {c_u} {val_fn}(void* handle) {{",
            "    SED2_TRY",
            f"    return static_cast<{c_u}>(static_cast<{cpp}*>(handle)->get{m}().value);",
            "    SED2_CATCH_RETURN(0)",
            "}",
        ]
        defs += _string_getter(ref_fn, f"static_cast<{cpp}*>(handle)", f"obj->get{m}().refValue")
        defs += [
            f"SED2_C_API void {setval_fn}(void* handle, {c_u} value) {{",
            "    SED2_TRY",
            f"    static_cast<{cpp}*>(handle)->set{m}(static_cast<{u}>(value));",
            "    SED2_CATCH_VOID",
            "}",
            f"SED2_C_API void {setref_fn}(void* handle, const char* ref) {{",
            "    SED2_TRY",
            f"    static_cast<{cpp}*>(handle)->set{m}(sed2::{T.split('::')[1]}::fromReference(ref ? ref : \"\"));",
            "    SED2_CATCH_VOID",
            "}",
        ]
        del cast_val
    else:  # double, bool, int64_t
        c_t = {"double": "double", "bool": "int", "int64_t": "int64_t"}[T]
        decls += [f"SED2_C_API {c_t} {get_fn}(void* handle);", f"SED2_C_API void {set_fn}(void* handle, {c_t} value);"]
        ret = f"obj->get{m}() ? 1 : 0" if T == "bool" else f"obj->get{m}()"
        defs += [
            f"SED2_C_API {c_t} {get_fn}(void* handle) {{",
            "    SED2_TRY",
            f"    auto* obj = static_cast<{cpp}*>(handle);",
            f"    return {ret};",
            "    SED2_CATCH_RETURN(0)",
            "}",
        ]
        set_val = "value != 0" if T == "bool" else "value"
        defs += [
            f"SED2_C_API void {set_fn}(void* handle, {c_t} value) {{",
            "    SED2_TRY",
            f"    static_cast<{cpp}*>(handle)->set{m}({set_val});",
            "    SED2_CATCH_VOID",
            "}",
        ]

    decls += [f"SED2_C_API int {isset_fn}(void* handle);", f"SED2_C_API void {unset_fn}(void* handle);"]
    defs += [
        f"SED2_C_API int {isset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->isSet{m}() ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {unset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->unset{m}();",
        "    SED2_CATCH_VOID",
        "}",
    ]
    return decls, defs


def emit_scalar_list(cpp, class_name, attr):
    m, im, T = attr.method, attr.item_method, attr.cpp_type
    # attr.cpp_type is bare ("Json") for types that actually live in namespace
    # sed2 (see cpp_qualified_for()) - .get<T>() below needs the qualified
    # form since sed2_c_api.cpp has no "using namespace sed2".
    T = "sed2::Json" if T == "Json" else T
    get_fn, getnum_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"getNum{m}")
    add_fn, insert_fn, remove_fn = c_func(class_name, f"add{im}"), c_func(class_name, f"insert{im}"), c_func(class_name, f"remove{im}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")

    decls = [
        f"SED2_C_API char* {get_fn}(void* handle);",
        f"SED2_C_API size_t {getnum_fn}(void* handle);",
        f"SED2_C_API void {add_fn}(void* handle, const char* jsonValue);",
        f"SED2_C_API void {insert_fn}(void* handle, size_t index, const char* jsonValue);",
        f"SED2_C_API int {remove_fn}(void* handle, const char* jsonValue);",
        f"SED2_C_API int {isset_fn}(void* handle);",
        f"SED2_C_API void {unset_fn}(void* handle);",
    ]
    defs = _string_getter(get_fn, f"static_cast<{cpp}*>(handle)", f"sed2::Json(obj->get{m}()).dump()")
    defs += [
        f"SED2_C_API size_t {getnum_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->getNum{m}();",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {add_fn}(void* handle, const char* jsonValue) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->add{im}(sed2::Json::parse(jsonValue).get<{T}>());",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API void {insert_fn}(void* handle, size_t index, const char* jsonValue) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->insert{im}(index, sed2::Json::parse(jsonValue).get<{T}>());",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API int {remove_fn}(void* handle, const char* jsonValue) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->remove{im}(sed2::Json::parse(jsonValue).get<{T}>()) ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API int {isset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->isSet{m}() ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {unset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->unset{m}();",
        "    SED2_CATCH_VOID",
        "}",
    ]

    if attr.single_ref_allowed:
        isref_fn, getref_fn, setref_fn = c_func(class_name, f"isSet{m}Reference"), c_func(class_name, f"get{m}Reference"), c_func(class_name, f"set{m}Reference")
        decls += [
            f"SED2_C_API int {isref_fn}(void* handle);",
            f"SED2_C_API char* {getref_fn}(void* handle);",
            f"SED2_C_API void {setref_fn}(void* handle, const char* ref);",
        ]
        defs += [
            f"SED2_C_API int {isref_fn}(void* handle) {{",
            "    SED2_TRY",
            f"    return static_cast<{cpp}*>(handle)->isSet{m}Reference() ? 1 : 0;",
            "    SED2_CATCH_RETURN(0)",
            "}",
        ]
        defs += _string_getter(getref_fn, f"static_cast<{cpp}*>(handle)", f"obj->get{m}Reference()")
        defs += [
            f"SED2_C_API void {setref_fn}(void* handle, const char* ref) {{",
            "    SED2_TRY",
            f"    static_cast<{cpp}*>(handle)->set{m}Reference(ref ? ref : \"\");",
            "    SED2_CATCH_VOID",
            "}",
        ]
    return decls, defs


def emit_map(cpp, class_name, attr):
    m = attr.method
    get_fn, set_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"set{m}")
    has_fn, remove_fn = c_func(class_name, f"has{m}"), c_func(class_name, f"remove{m}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        f"SED2_C_API char* {get_fn}(void* handle);",
        f"SED2_C_API void {set_fn}(void* handle, const char* key, const char* jsonValue);",
        f"SED2_C_API int {has_fn}(void* handle, const char* key);",
        f"SED2_C_API int {remove_fn}(void* handle, const char* key);",
        f"SED2_C_API int {isset_fn}(void* handle);",
        f"SED2_C_API void {unset_fn}(void* handle);",
    ]
    defs = _string_getter(get_fn, f"static_cast<{cpp}*>(handle)", "obj->get" + m + "().dump()")
    defs += [
        f"SED2_C_API void {set_fn}(void* handle, const char* key, const char* jsonValue) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->set{m}(key, sed2::Json::parse(jsonValue));",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API int {has_fn}(void* handle, const char* key) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->has{m}(key) ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API int {remove_fn}(void* handle, const char* key) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->remove{m}(key) ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API int {isset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->isSet{m}() ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {unset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->unset{m}();",
        "    SED2_CATCH_VOID",
        "}",
    ]
    return decls, defs


def emit_owned(cpp, class_name, attr):
    m = attr.method
    get_fn, set_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"set{m}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        f"SED2_C_API void* {get_fn}(void* handle);",
        f"SED2_C_API void {set_fn}(void* handle, void* child);",
        f"SED2_C_API int {isset_fn}(void* handle);",
        f"SED2_C_API void {unset_fn}(void* handle);",
    ]
    defs = [
        f"SED2_C_API void* {get_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->get{m}();",
        "    SED2_CATCH_RETURN(nullptr)",
        "}",
        f"SED2_C_API void {set_fn}(void* handle, void* child) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->set{m}(std::unique_ptr<sed2::SEDBase>(static_cast<sed2::SEDBase*>(child)));",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API int {isset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->isSet{m}() ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {unset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->unset{m}();",
        "    SED2_CATCH_VOID",
        "}",
    ]
    return decls, defs


def emit_owned_array(cpp, class_name, attr):
    m, im, it = attr.method, attr.item_method, attr.item_type
    getall_fn, getnum_fn = c_func(class_name, f"get{m}All"), c_func(class_name, f"getNum{m}")
    add_fn, insert_fn, removeat_fn = c_func(class_name, f"add{im}"), c_func(class_name, f"insert{im}"), c_func(class_name, f"remove{im}At")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        f"SED2_C_API size_t {getnum_fn}(void* handle);",
        f"SED2_C_API size_t {getall_fn}(void* handle, void** outArray, size_t maxCount);",
        f"SED2_C_API void {add_fn}(void* handle, void* item);",
        f"SED2_C_API void {insert_fn}(void* handle, size_t index, void* item);",
        f"SED2_C_API int {removeat_fn}(void* handle, size_t index);",
        f"SED2_C_API int {isset_fn}(void* handle);",
        f"SED2_C_API void {unset_fn}(void* handle);",
    ]
    defs = [
        f"SED2_C_API size_t {getnum_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->getNum{m}();",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API size_t {getall_fn}(void* handle, void** outArray, size_t maxCount) {{",
        "    SED2_TRY",
        f"    auto items = static_cast<{cpp}*>(handle)->get{m}();",
        "    size_t n = items.size();",
        "    size_t toCopy = n < maxCount ? n : maxCount;",
        "    for (size_t i = 0; i < toCopy; ++i) outArray[i] = items[i];",
        "    return n;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {add_fn}(void* handle, void* item) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->add{im}(std::unique_ptr<sed2::{it}>(static_cast<sed2::{it}*>(item)));",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API void {insert_fn}(void* handle, size_t index, void* item) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->insert{im}(index, std::unique_ptr<sed2::{it}>(static_cast<sed2::{it}*>(item)));",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API int {removeat_fn}(void* handle, size_t index) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->remove{im}At(index) ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API int {isset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->isSet{m}() ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {unset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->unset{m}();",
        "    SED2_CATCH_VOID",
        "}",
    ]
    return decls, defs


def emit_polymorphic_list(cpp, class_name, attr):
    m, im = attr.method, attr.item_method
    getall_fn, getnum_fn, getitem_fn = c_func(class_name, f"get{m}All"), c_func(class_name, f"getNum{m}"), c_func(class_name, f"get{im}")
    add_fn, insert_fn, remove_fn = c_func(class_name, f"add{im}"), c_func(class_name, f"insert{im}"), c_func(class_name, f"remove{im}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        f"SED2_C_API size_t {getnum_fn}(void* handle);",
        f"SED2_C_API size_t {getall_fn}(void* handle, void** outArray, size_t maxCount);",
        f"SED2_C_API void* {getitem_fn}(void* handle, const char* id);",
        f"SED2_C_API void {add_fn}(void* handle, void* item);",
        f"SED2_C_API void {insert_fn}(void* handle, size_t index, void* item);",
        f"SED2_C_API int {remove_fn}(void* handle, const char* id);",
        f"SED2_C_API int {isset_fn}(void* handle);",
        f"SED2_C_API void {unset_fn}(void* handle);",
    ]
    defs = [
        f"SED2_C_API size_t {getnum_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->getNum{m}();",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API size_t {getall_fn}(void* handle, void** outArray, size_t maxCount) {{",
        "    SED2_TRY",
        f"    auto items = static_cast<{cpp}*>(handle)->get{m}();",
        "    size_t n = items.size();",
        "    size_t toCopy = n < maxCount ? n : maxCount;",
        "    for (size_t i = 0; i < toCopy; ++i) outArray[i] = items[i];",
        "    return n;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void* {getitem_fn}(void* handle, const char* id) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->get{im}(id ? id : \"\");",
        "    SED2_CATCH_RETURN(nullptr)",
        "}",
        f"SED2_C_API void {add_fn}(void* handle, void* item) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->add{im}(std::unique_ptr<sed2::SEDBase>(static_cast<sed2::SEDBase*>(item)));",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API void {insert_fn}(void* handle, size_t index, void* item) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->insert{im}(index, std::unique_ptr<sed2::SEDBase>(static_cast<sed2::SEDBase*>(item)));",
        "    SED2_CATCH_VOID",
        "}",
        f"SED2_C_API int {remove_fn}(void* handle, const char* id) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->remove{im}(id ? id : \"\") ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API int {isset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    return static_cast<{cpp}*>(handle)->isSet{m}() ? 1 : 0;",
        "    SED2_CATCH_RETURN(0)",
        "}",
        f"SED2_C_API void {unset_fn}(void* handle) {{",
        "    SED2_TRY",
        f"    static_cast<{cpp}*>(handle)->unset{m}();",
        "    SED2_CATCH_VOID",
        "}",
    ]
    return decls, defs


ATTR_EMITTERS = {
    "scalar": emit_scalar,
    "scalarList": emit_scalar_list,
    "map": emit_map,
    "owned": emit_owned,
    "ownedArray": emit_owned_array,
    "polymorphicList": emit_polymorphic_list,
}


# -- Python: per-attribute emitters ------------------------------------------
# Each returns (decl_specs: list[(func_name, "[argtypes]", "restype")],
# method_lines: list[str]). decl_specs feed the _decl(...) calls emitted
# once per class (see write_python() below); method_lines are indented
# ready to drop into the class body.

def py_scalar(class_name, attr):
    m, T, py = attr.method, attr.cpp_type, snake(attr.name)
    get_fn, set_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"set{m}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        (isset_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
        (unset_fn, "[ctypes.c_void_p]", None),
    ]
    lines = []

    if T == "std::string":
        decls += [(get_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"), (set_fn, "[ctypes.c_void_p, ctypes.c_char_p]", None)]
        lines += [
            f"    def get_{py}(self):",
            f"        return _take_string(_lib.{get_fn}(self._handle))",
            f"    def set_{py}(self, value):",
            f"        _lib.{set_fn}(self._handle, value.encode('utf-8'))",
        ]
    elif T == "Json":
        decls += [(get_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"), (set_fn, "[ctypes.c_void_p, ctypes.c_char_p]", None)]
        lines += [
            f"    def get_{py}(self):",
            f"        return json.loads(_take_string(_lib.{get_fn}(self._handle)))",
            f"    def set_{py}(self, value):",
            f"        _lib.{set_fn}(self._handle, json.dumps(value).encode('utf-8'))",
        ]
    elif T in gc.VALUE_OR_REF_TYPES:
        u = gc.VALUE_OR_REF_UNDERLYING[T]
        c_u = {"double": "ctypes.c_double", "int64_t": "ctypes.c_int64", "bool": "ctypes.c_int"}[u]
        isref_fn, val_fn, ref_fn = c_func(class_name, f"get{m}_isRef"), c_func(class_name, f"get{m}_value"), c_func(class_name, f"get{m}_refValue")
        setval_fn, setref_fn = c_func(class_name, f"set{m}_value"), c_func(class_name, f"set{m}_ref")
        decls += [
            (isref_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
            (val_fn, "[ctypes.c_void_p]", c_u),
            (ref_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"),
            (setval_fn, f"[ctypes.c_void_p, {c_u}]", None),
            (setref_fn, "[ctypes.c_void_p, ctypes.c_char_p]", None),
        ]
        value_expr = f"bool(_lib.{val_fn}(self._handle))" if u == "bool" else f"_lib.{val_fn}(self._handle)"
        set_val_expr = "(1 if value else 0)" if u == "bool" else "value"
        lines += [
            f"    def get_{py}(self):",
            f"        \"\"\"Either the literal value, or (if this is a reference) the",
            f"        reference string - mirrors how the C++ side's ValueOrRef<T> and",
            f"        its JSON (de)serialization both fold isRef/value/refValue into",
            f"        one value already (see AttributeTypes.h).\"\"\"",
            f"        if _lib.{isref_fn}(self._handle):",
            f"            return _take_string(_lib.{ref_fn}(self._handle))",
            f"        return {value_expr}",
            f"    def set_{py}(self, value):",
            "        \"\"\"Pass a literal (matching this attribute's type) or a '#...'",
            "        reference string.\"\"\"",
            "        if isinstance(value, str):",
            f"            _lib.{setref_fn}(self._handle, value.encode('utf-8'))",
            "        else:",
            f"            _lib.{setval_fn}(self._handle, {set_val_expr})",
        ]
    else:  # double, bool, int64_t
        c_t = {"double": "ctypes.c_double", "bool": "ctypes.c_int", "int64_t": "ctypes.c_int64"}[T]
        decls += [(get_fn, "[ctypes.c_void_p]", c_t), (set_fn, f"[ctypes.c_void_p, {c_t}]", None)]
        get_expr = f"bool(_lib.{get_fn}(self._handle))" if T == "bool" else f"_lib.{get_fn}(self._handle)"
        set_expr = "(1 if value else 0)" if T == "bool" else "value"
        lines += [
            f"    def get_{py}(self):",
            f"        return {get_expr}",
            f"    def set_{py}(self, value):",
            f"        _lib.{set_fn}(self._handle, {set_expr})",
        ]

    lines += [
        f"    def is_set_{py}(self):",
        f"        return bool(_lib.{isset_fn}(self._handle))",
        f"    def unset_{py}(self):",
        f"        _lib.{unset_fn}(self._handle)",
    ]
    return decls, lines


def py_scalar_list(class_name, attr):
    m, im, py, ipy = attr.method, attr.item_method, snake(attr.name), _unpascal_item(attr)
    get_fn, getnum_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"getNum{m}")
    add_fn, insert_fn, remove_fn = c_func(class_name, f"add{im}"), c_func(class_name, f"insert{im}"), c_func(class_name, f"remove{im}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        (get_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"),
        (getnum_fn, "[ctypes.c_void_p]", "ctypes.c_size_t"),
        (add_fn, "[ctypes.c_void_p, ctypes.c_char_p]", None),
        (insert_fn, "[ctypes.c_void_p, ctypes.c_size_t, ctypes.c_char_p]", None),
        (remove_fn, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_int"),
        (isset_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
        (unset_fn, "[ctypes.c_void_p]", None),
    ]
    lines = [
        f"    def get_{py}(self):",
        f"        return json.loads(_take_string(_lib.{get_fn}(self._handle)))",
        f"    def get_num_{py}(self):",
        f"        return _lib.{getnum_fn}(self._handle)",
        f"    def add_{ipy}(self, value):",
        f"        _lib.{add_fn}(self._handle, json.dumps(value).encode('utf-8'))",
        f"    def insert_{ipy}(self, index, value):",
        f"        _lib.{insert_fn}(self._handle, index, json.dumps(value).encode('utf-8'))",
        f"    def remove_{ipy}(self, value):",
        f"        return bool(_lib.{remove_fn}(self._handle, json.dumps(value).encode('utf-8')))",
        f"    def is_set_{py}(self):",
        f"        return bool(_lib.{isset_fn}(self._handle))",
        f"    def unset_{py}(self):",
        f"        _lib.{unset_fn}(self._handle)",
    ]
    if attr.single_ref_allowed:
        isref_fn, getref_fn, setref_fn = c_func(class_name, f"isSet{m}Reference"), c_func(class_name, f"get{m}Reference"), c_func(class_name, f"set{m}Reference")
        decls += [
            (isref_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
            (getref_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"),
            (setref_fn, "[ctypes.c_void_p, ctypes.c_char_p]", None),
        ]
        lines += [
            f"    def is_set_{py}_reference(self):",
            f"        return bool(_lib.{isref_fn}(self._handle))",
            f"    def get_{py}_reference(self):",
            f"        return _take_string(_lib.{getref_fn}(self._handle))",
            f"    def set_{py}_reference(self, ref):",
            f"        _lib.{setref_fn}(self._handle, ref.encode('utf-8'))",
        ]
    return decls, lines


def _unpascal_item(attr):
    # attr.item_method is Pascal-cased (pascal(itemName), e.g. "OutputVariable");
    # snake() on it gives the same result as snake-casing the original
    # camelCase itemName would, since pascal() only touches the first
    # character.
    return snake(attr.item_method)


def py_map(class_name, attr):
    m, py = attr.method, snake(attr.name)
    get_fn, set_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"set{m}")
    has_fn, remove_fn = c_func(class_name, f"has{m}"), c_func(class_name, f"remove{m}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        (get_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"),
        (set_fn, "[ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]", None),
        (has_fn, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_int"),
        (remove_fn, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_int"),
        (isset_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
        (unset_fn, "[ctypes.c_void_p]", None),
    ]
    lines = [
        f"    def get_{py}(self):",
        f"        return json.loads(_take_string(_lib.{get_fn}(self._handle)))",
        f"    def set_{py}(self, key, value):",
        f"        _lib.{set_fn}(self._handle, key.encode('utf-8'), json.dumps(value).encode('utf-8'))",
        f"    def has_{py}(self, key):",
        f"        return bool(_lib.{has_fn}(self._handle, key.encode('utf-8')))",
        f"    def remove_{py}(self, key):",
        f"        return bool(_lib.{remove_fn}(self._handle, key.encode('utf-8')))",
        f"    def is_set_{py}(self):",
        f"        return bool(_lib.{isset_fn}(self._handle))",
        f"    def unset_{py}(self):",
        f"        _lib.{unset_fn}(self._handle)",
    ]
    return decls, lines


def _wrap_expr(attr):
    """The Python expression (as a string, 'handle' already bound) that
    wraps a borrowed child pointer for this owned/polymorphicList
    attribute: the fixed wrapper class directly when itemType/testItemType
    names one, or the generic typeName-dispatching factory otherwise (see
    _wrap_sedbase in the generated preamble)."""
    t = attr.item_type or attr.test_item_type
    if t:
        return f"_wrap_or_none({t}, handle)"
    return "_wrap_sedbase(handle)"


def py_owned(class_name, attr):
    m, py = attr.method, snake(attr.name)
    get_fn, set_fn = c_func(class_name, f"get{m}"), c_func(class_name, f"set{m}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        (get_fn, "[ctypes.c_void_p]", "ctypes.c_void_p"),
        (set_fn, "[ctypes.c_void_p, ctypes.c_void_p]", None),
        (isset_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
        (unset_fn, "[ctypes.c_void_p]", None),
    ]
    lines = [
        f"    def get_{py}(self):",
        f"        handle = _lib.{get_fn}(self._handle)",
        f"        return {_wrap_expr(attr)}",
        f"    def set_{py}(self, value):",
        "        handle = 0",
        "        if value is not None:",
        "            _require_owned(value)",
        "            handle = value._handle",
        f"        _lib.{set_fn}(self._handle, handle)",
        "        if value is not None:",
        "            value._release()",
        f"    def is_set_{py}(self):",
        f"        return bool(_lib.{isset_fn}(self._handle))",
        f"    def unset_{py}(self):",
        f"        _lib.{unset_fn}(self._handle)",
    ]
    return decls, lines


def py_owned_array(class_name, attr):
    m, im, it, py, ipy = attr.method, attr.item_method, attr.item_type, snake(attr.name), _unpascal_item(attr)
    getall_fn, getnum_fn = c_func(class_name, f"get{m}All"), c_func(class_name, f"getNum{m}")
    add_fn, insert_fn, removeat_fn = c_func(class_name, f"add{im}"), c_func(class_name, f"insert{im}"), c_func(class_name, f"remove{im}At")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        (getnum_fn, "[ctypes.c_void_p]", "ctypes.c_size_t"),
        (getall_fn, "[ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_size_t]", "ctypes.c_size_t"),
        (add_fn, "[ctypes.c_void_p, ctypes.c_void_p]", None),
        (insert_fn, "[ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]", None),
        (removeat_fn, "[ctypes.c_void_p, ctypes.c_size_t]", "ctypes.c_int"),
        (isset_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
        (unset_fn, "[ctypes.c_void_p]", None),
    ]
    lines = [
        f"    def get_{py}(self):",
        f"        n = _lib.{getnum_fn}(self._handle)",
        "        if n == 0:",
        "            return []",
        "        arr = (ctypes.c_void_p * n)()",
        f"        _lib.{getall_fn}(self._handle, arr, n)",
        f"        return [{it}(_handle=arr[i]) for i in range(n)]",
        f"    def get_num_{py}(self):",
        f"        return _lib.{getnum_fn}(self._handle)",
        f"    def add_{ipy}(self, value):",
        "        _require_owned(value)",
        f"        _lib.{add_fn}(self._handle, value._handle)",
        "        value._release()",
        f"    def insert_{ipy}(self, index, value):",
        "        _require_owned(value)",
        f"        _lib.{insert_fn}(self._handle, index, value._handle)",
        "        value._release()",
        f"    def remove_{ipy}_at(self, index):",
        f"        return bool(_lib.{removeat_fn}(self._handle, index))",
        f"    def is_set_{py}(self):",
        f"        return bool(_lib.{isset_fn}(self._handle))",
        f"    def unset_{py}(self):",
        f"        _lib.{unset_fn}(self._handle)",
    ]
    return decls, lines


def py_polymorphic_list(class_name, attr):
    m, im, py, ipy = attr.method, attr.item_method, snake(attr.name), _unpascal_item(attr)
    getall_fn, getnum_fn, getitem_fn = c_func(class_name, f"get{m}All"), c_func(class_name, f"getNum{m}"), c_func(class_name, f"get{im}")
    add_fn, insert_fn, remove_fn = c_func(class_name, f"add{im}"), c_func(class_name, f"insert{im}"), c_func(class_name, f"remove{im}")
    isset_fn, unset_fn = c_func(class_name, f"isSet{m}"), c_func(class_name, f"unset{m}")
    decls = [
        (getnum_fn, "[ctypes.c_void_p]", "ctypes.c_size_t"),
        (getall_fn, "[ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_size_t]", "ctypes.c_size_t"),
        (getitem_fn, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_void_p"),
        (add_fn, "[ctypes.c_void_p, ctypes.c_void_p]", None),
        (insert_fn, "[ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]", None),
        (remove_fn, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_int"),
        (isset_fn, "[ctypes.c_void_p]", "ctypes.c_int"),
        (unset_fn, "[ctypes.c_void_p]", None),
    ]
    wrap = _wrap_expr(attr)
    lines = [
        f"    def get_{py}(self):",
        f"        n = _lib.{getnum_fn}(self._handle)",
        "        if n == 0:",
        "            return []",
        "        arr = (ctypes.c_void_p * n)()",
        f"        _lib.{getall_fn}(self._handle, arr, n)",
        "        result = []",
        "        for i in range(n):",
        "            handle = arr[i]",
        f"            result.append({wrap})",
        "        return result",
        f"    def get_num_{py}(self):",
        f"        return _lib.{getnum_fn}(self._handle)",
        f"    def get_{ipy}(self, item_id):",
        f"        handle = _lib.{getitem_fn}(self._handle, item_id.encode('utf-8'))",
        f"        return {wrap}",
        f"    def add_{ipy}(self, value):",
        "        _require_owned(value)",
        f"        _lib.{add_fn}(self._handle, value._handle)",
        "        value._release()",
        f"    def insert_{ipy}(self, index, value):",
        "        _require_owned(value)",
        f"        _lib.{insert_fn}(self._handle, index, value._handle)",
        "        value._release()",
        f"    def remove_{ipy}(self, item_id):",
        f"        return bool(_lib.{remove_fn}(self._handle, item_id.encode('utf-8')))",
        f"    def is_set_{py}(self):",
        f"        return bool(_lib.{isset_fn}(self._handle))",
        f"    def unset_{py}(self):",
        f"        _lib.{unset_fn}(self._handle)",
    ]
    return decls, lines


PY_ATTR_EMITTERS = {
    "scalar": py_scalar,
    "scalarList": py_scalar_list,
    "map": py_map,
    "owned": py_owned,
    "ownedArray": py_owned_array,
    "polymorphicList": py_polymorphic_list,
}


# -- per-class assembly -------------------------------------------------------

def cpp_qualified_for(class_name):
    # SEDDocument is "generateBaseOnly" (see generate_classes.py's module
    # docstring): the real, usable class is the hand-written sed2::
    # SEDDocument subclass (include/sed2/core/SEDDocument.h), not the
    # generated sed2::generated::SEDDocument it wraps - so the C API binds
    # to that one, the same way tests/unit/test_SEDDocument.cpp does.
    if class_name == "SEDDocument":
        return "sed2::SEDDocument"
    return f"sed2::{class_name}"


def cpp_include_for(class_name):
    if class_name == "SEDDocument":
        return "sed2/core/SEDDocument.h"
    return f"sed2/generated/{class_name}.h"


def generate_c_for_class(class_name, table):
    cpp = cpp_qualified_for(class_name)
    attributes = gc.ATTRIBUTE_TABLES[class_name]
    create_fn = c_func(class_name, "create")

    decls = [f"SED2_C_API void* {create_fn}(void);"]
    defs = [
        f"SED2_C_API void* {create_fn}(void) {{",
        "    SED2_TRY",
        f"    return new {cpp}();",
        "    SED2_CATCH_RETURN(nullptr)",
        "}",
    ]
    for attr in attributes:
        d, f = ATTR_EMITTERS[attr.kind](cpp, class_name, attr)
        decls += d
        defs += f

    if class_name == "SEDDocument":
        decls += [
            f"SED2_C_API void* {c_func('SEDDocument', 'fromFile')}(const char* path, char** errorOut);",
            f"SED2_C_API void* {c_func('SEDDocument', 'fromJSONString')}(const char* text, char** errorOut);",
            f"SED2_C_API int {c_func('SEDDocument', 'toFile')}(void* handle, const char* path);",
            f"SED2_C_API void* {c_func('SEDDocument', 'getSEDReference')}(void* handle, const char* ref);",
        ]
        defs += [
            f"SED2_C_API void* {c_func('SEDDocument', 'fromFile')}(const char* path, char** errorOut) {{",
            "    SED2_TRY",
            "    std::string err;",
            "    auto* doc = new sed2::SEDDocument(sed2::SEDDocument::fromFile(path ? path : \"\", &err));",
            "    if (errorOut) *errorOut = err.empty() ? nullptr : sed2_c::allocString(err);",
            "    return doc;",
            "    SED2_CATCH_RETURN(nullptr)",
            "}",
            f"SED2_C_API void* {c_func('SEDDocument', 'fromJSONString')}(const char* text, char** errorOut) {{",
            "    SED2_TRY",
            "    std::string err;",
            "    auto* doc = new sed2::SEDDocument(sed2::SEDDocument::fromJSONString(text ? text : \"\", &err));",
            "    if (errorOut) *errorOut = err.empty() ? nullptr : sed2_c::allocString(err);",
            "    return doc;",
            "    SED2_CATCH_RETURN(nullptr)",
            "}",
            f"SED2_C_API int {c_func('SEDDocument', 'toFile')}(void* handle, const char* path) {{",
            "    SED2_TRY",
            "    return static_cast<sed2::SEDDocument*>(handle)->toFile(path ? path : \"\") ? 1 : 0;",
            "    SED2_CATCH_RETURN(0)",
            "}",
            f"SED2_C_API void* {c_func('SEDDocument', 'getSEDReference')}(void* handle, const char* ref) {{",
            "    SED2_TRY",
            "    return const_cast<sed2::SEDBase*>(static_cast<sed2::SEDDocument*>(handle)->getSEDReference(ref ? ref : \"\"));",
            "    SED2_CATCH_RETURN(nullptr)",
            "}",
        ]

    return decls, defs, cpp_include_for(class_name)


PY_PREAMBLE = '''"""Generated by codegen/generate_ctypes.py from
codegen/spec_attributes/*.json (the same tables generate_classes.py turns
into C++ classes). Do not hand-edit this file; edit the attribute table
and rebuild - CMake reruns the generator automatically whenever a table or
either generator script changes.

Loads the sed2_c shared library (built from the generated C API shim
alongside this file - see include/sed2_c/Runtime.h and CMakeLists.txt's
sed2_c target) via ctypes, and wraps its functions in one Python class per
SED2 class, mirroring the C++ get/set/isSet/unset (and, for list
attributes, add/insert/remove) pattern with Pythonic snake_case names.

Object identity and ownership work the way they do in the C++ library:
constructing a class (e.g. Report()) allocates a new C++ object this
wrapper owns and will destroy when garbage-collected; passing one wrapper
into another's owning setter/add (e.g. report.set_data(...) is a plain
value, but doc.add_task(model_import) is not) transfers ownership to the
new parent, and the child wrapper must not be used to destroy it again
(this is tracked automatically - see SEDBase._release() below). A getter
for an owned/ownedArray/polymorphicList attribute returns a *borrowed*
wrapper: valid only as long as its parent is, never destroyed by the
caller.
"""
import ctypes
import json
import os
import platform


class Sed2Error(RuntimeError):
    """Raised when a C API call reports failure - see sed2_get_last_error()
    in include/sed2_c/Runtime.h. The C++ exception that caused it (if any)
    never crosses into Python directly; its message is copied into this
    instead."""


def _find_library():
    override = os.environ.get("SED2_C_LIBRARY")
    if override:
        return override
    system = platform.system()
    if system == "Windows":
        names = ["sed2_c.dll"]
    elif system == "Darwin":
        names = ["libsed2_c.dylib"]
    else:
        names = ["libsed2_c.so"]
    here = os.path.dirname(os.path.abspath(__file__))
    for name in names:
        candidate = os.path.join(here, name)
        if os.path.exists(candidate):
            return candidate
    # Not found next to this file - fall back to the OS loader's normal
    # search path (SED2_C_LIBRARY above is the escape hatch if that fails
    # too).
    return names[0]


_lib = ctypes.CDLL(_find_library())


def _decl(name, argtypes, restype):
    fn = getattr(_lib, name)
    fn.argtypes = argtypes
    fn.restype = restype
    return fn


_decl("sed2_get_last_error", [], ctypes.c_char_p)
_decl("sed2_free_string", [ctypes.c_void_p], None)
_decl("sed2_SEDBase_destroy", [ctypes.c_void_p], None)
_decl("sed2_SEDBase_getTypeName", [ctypes.c_void_p], ctypes.c_void_p)
_decl("sed2_SEDBase_fromJSON", [ctypes.c_void_p, ctypes.c_char_p], ctypes.c_int)
_decl("sed2_SEDBase_toJSON", [ctypes.c_void_p], ctypes.c_void_p)
_decl("sed2_SEDBase_validate", [ctypes.c_void_p], ctypes.c_void_p)
_decl("sed2_SEDBase_getParent", [ctypes.c_void_p], ctypes.c_void_p)
_decl("sed2_SEDBase_getSEDDocument", [ctypes.c_void_p], ctypes.c_void_p)
for _base_attr in ("Id", "Name", "Description", "Notes"):
    _decl(f"sed2_SEDBase_get{_base_attr}", [ctypes.c_void_p], ctypes.c_void_p)
    _decl(f"sed2_SEDBase_set{_base_attr}", [ctypes.c_void_p, ctypes.c_char_p], None)
    _decl(f"sed2_SEDBase_isSet{_base_attr}", [ctypes.c_void_p], ctypes.c_int)
    _decl(f"sed2_SEDBase_unset{_base_attr}", [ctypes.c_void_p], None)


def _last_error():
    msg = _lib.sed2_get_last_error()
    return msg.decode("utf-8") if msg else "sed2: unknown error"


def _take_string(ptr):
    """ptr is the raw address (ctypes.c_void_p-typed restype) of a
    freshly allocated, caller-owned C string - decodes it to a Python str
    and immediately frees it via sed2_free_string() (always from the same
    library that allocated it - see allocString() in Runtime.h)."""
    if not ptr:
        return ""
    s = ctypes.cast(ptr, ctypes.c_char_p).value.decode("utf-8")
    _lib.sed2_free_string(ctypes.cast(ptr, ctypes.c_void_p))
    return s


def _require_owned(value):
    if value is None or not getattr(value, "_owns", False):
        raise Sed2Error(
            "this object does not own its handle (it is either borrowed from "
            "a parent, or was already attached elsewhere) - construct a new "
            "instance to attach here"
        )


_TYPE_NAME_TO_CLASS = {}  # populated at the bottom of this file, once every class exists


def _wrap_sedbase(handle):
    """Wraps a borrowed SEDBase* handle in the correct generated wrapper
    class by asking the object itself what it is (getTypeName() is
    virtual - see Runtime.h) and looking that up against every
    registerType:true class's own typeName, the same dispatch
    TypeRegistry does on the C++ side. Falls back to the generic SEDBase
    wrapper for a handle whose runtime type isn't one of those (e.g. a
    RawElement, the fallback for an unrecognized "_type")."""
    if not handle:
        return None
    type_name = _take_string(_lib.sed2_SEDBase_getTypeName(handle))
    cls = _TYPE_NAME_TO_CLASS.get(type_name, SEDBase)
    return cls(_handle=handle)


def _wrap_or_none(cls, handle):
    if not handle:
        return None
    return cls(_handle=handle)


class SEDBase:
    """Base wrapper for every generated class - handle/ownership tracking,
    and the id/name/description/notes attributes and getTypeName/
    fromJSON/toJSON/validate methods every SED2 class has (see
    include/sed2/core/SEDBase.h), all implemented once here since the C
    API's own SEDBase-level functions already dispatch virtually rather
    than needing to be generated per class - see Runtime.h."""

    def __init__(self, _handle=None):
        if _handle is None:
            _handle = self._create()
            self._owns = True
        else:
            self._owns = False
        self._handle = _handle

    def _create(self):
        raise NotImplementedError("SEDBase is abstract - construct a concrete subclass instead")

    def __del__(self):
        handle = getattr(self, "_handle", None)
        if handle and getattr(self, "_owns", False):
            _lib.sed2_SEDBase_destroy(handle)
        self._handle = None

    def _release(self):
        """Marks this wrapper as no longer owning its handle - called after
        the handle is handed to a C++ parent through an owning setter/add
        (see e.g. SEDBase's own set_x pattern in a generated owned
        attribute); the wrapper still refers to the same object, but must
        not destroy it anymore."""
        self._owns = False

    def get_type_name(self):
        return _take_string(_lib.sed2_SEDBase_getTypeName(self._handle))

    def from_json(self, data):
        """Accepts either a dict (as returned by to_json()) or a raw JSON
        string, so the two methods round-trip symmetrically."""
        text = data if isinstance(data, str) else json.dumps(data)
        rc = _lib.sed2_SEDBase_fromJSON(self._handle, text.encode("utf-8"))
        if rc != 0:
            raise Sed2Error(_last_error())

    def to_json(self):
        return json.loads(_take_string(_lib.sed2_SEDBase_toJSON(self._handle)))

    def validate(self):
        """A list of {"code", "message", "path", "severity"} dicts -
        'severity' is 0=Info, 1=Warning, 2=Error, 3=SchemaViolation,
        matching sed2::ValidationSeverity (see include/sed2/validation/
        ValidationError.h)."""
        return json.loads(_take_string(_lib.sed2_SEDBase_validate(self._handle)))

    def get_parent(self):
        return _wrap_sedbase(_lib.sed2_SEDBase_getParent(self._handle))

    def get_sed_document(self):
        return _wrap_sedbase(_lib.sed2_SEDBase_getSEDDocument(self._handle))

    def get_id(self):
        return _take_string(_lib.sed2_SEDBase_getId(self._handle))
    def set_id(self, value):
        _lib.sed2_SEDBase_setId(self._handle, value.encode("utf-8"))
    def is_set_id(self):
        return bool(_lib.sed2_SEDBase_isSetId(self._handle))
    def unset_id(self):
        _lib.sed2_SEDBase_unsetId(self._handle)

    def get_name(self):
        return _take_string(_lib.sed2_SEDBase_getName(self._handle))
    def set_name(self, value):
        _lib.sed2_SEDBase_setName(self._handle, value.encode("utf-8"))
    def is_set_name(self):
        return bool(_lib.sed2_SEDBase_isSetName(self._handle))
    def unset_name(self):
        _lib.sed2_SEDBase_unsetName(self._handle)

    def get_description(self):
        return _take_string(_lib.sed2_SEDBase_getDescription(self._handle))
    def set_description(self, value):
        _lib.sed2_SEDBase_setDescription(self._handle, value.encode("utf-8"))
    def is_set_description(self):
        return bool(_lib.sed2_SEDBase_isSetDescription(self._handle))
    def unset_description(self):
        _lib.sed2_SEDBase_unsetDescription(self._handle)

    def get_notes(self):
        return _take_string(_lib.sed2_SEDBase_getNotes(self._handle))
    def set_notes(self, value):
        _lib.sed2_SEDBase_setNotes(self._handle, value.encode("utf-8"))
    def is_set_notes(self):
        return bool(_lib.sed2_SEDBase_isSetNotes(self._handle))
    def unset_notes(self):
        _lib.sed2_SEDBase_unsetNotes(self._handle)

    def __repr__(self):
        ident = self.get_id() if self.is_set_id() else "?"
        return f"<{type(self).__name__} id={ident!r}>"
'''


def generate_python_for_class(class_name, table):
    type_name = table["typeName"]
    register_type = bool(table.get("registerType", True))
    attributes = gc.ATTRIBUTE_TABLES[class_name]
    create_fn = c_func(class_name, "create")

    decl_specs = [(create_fn, "[]", "ctypes.c_void_p")]
    method_lines = []
    for attr in attributes:
        d, lines = PY_ATTR_EMITTERS[attr.kind](class_name, attr)
        decl_specs += d
        method_lines += lines

    extra_class_lines = []
    if class_name == "SEDDocument":
        ff, fjs = c_func("SEDDocument", "fromFile"), c_func("SEDDocument", "fromJSONString")
        tf, gsr = c_func("SEDDocument", "toFile"), c_func("SEDDocument", "getSEDReference")
        decl_specs += [
            (ff, "[ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]", "ctypes.c_void_p"),
            (fjs, "[ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]", "ctypes.c_void_p"),
            (tf, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_int"),
            (gsr, "[ctypes.c_void_p, ctypes.c_char_p]", "ctypes.c_void_p"),
        ]
        extra_class_lines += [
            "    @classmethod",
            "    def from_file(cls, path):",
            '        """Returns (SEDDocument, error): error is None on success, or a',
            "        message string on failure (in which case the document is empty) -",
            "        mirrors sed2::SEDDocument::fromFile's out-parameter exactly rather",
            '        than raising, since a parse failure there is an expected outcome,',
            '        not a bug in the caller\'s use of this binding.\"\"\"',
            "        err_ptr = ctypes.c_void_p()",
            f"        handle = _lib.{ff}(path.encode('utf-8'), ctypes.byref(err_ptr))",
            "        error = _take_string(err_ptr.value) if err_ptr.value else None",
            "        return cls(_handle=handle), (error or None)",
            "    @classmethod",
            "    def from_json_string(cls, text):",
            '        """Same as from_file, but from an already-loaded JSON string."""',
            "        err_ptr = ctypes.c_void_p()",
            f"        handle = _lib.{fjs}(text.encode('utf-8'), ctypes.byref(err_ptr))",
            "        error = _take_string(err_ptr.value) if err_ptr.value else None",
            "        return cls(_handle=handle), (error or None)",
            "    def to_file(self, path):",
            '        """Writes to_json() to \'path\', pretty-printed. Returns False if',
            '        the file could not be written."""',
            f"        return bool(_lib.{tf}(self._handle, path.encode('utf-8')))",
            "    def get_sed_reference(self, ref):",
            '        """Resolves the colon-path prefix of a reference (e.g. "#tasks:sim1"',
            '        in "#tasks:sim1.model[\'S1\']") to the object it names, or None."""',
            f"        handle = _lib.{gsr}(self._handle, ref.encode('utf-8'))",
            "        return _wrap_sedbase(handle)",
        ]

    decl_lines = [f'_decl("{name}", {argtypes}, {restype})' for name, argtypes, restype in decl_specs]

    lines = []
    lines.append(f"# ---- {class_name} ----")
    lines += decl_lines
    lines.append(f"class {class_name}(SEDBase):")
    lines.append(f'    """Wraps {cpp_qualified_for(class_name)}."""')
    lines.append(f"    def _create(self):")
    lines.append(f"        return _lib.{create_fn}()")
    lines += extra_class_lines
    lines += method_lines
    if register_type:
        lines.append(f'_TYPE_NAME_TO_CLASS["{type_name}"] = {class_name}')
    return "\n".join(lines)


def write_c_api(out_dir, tables):
    header_dir = os.path.join(out_dir, "include")
    source_dir = os.path.join(out_dir, "src")
    os.makedirs(header_dir, exist_ok=True)
    os.makedirs(source_dir, exist_ok=True)

    all_decls, all_defs, includes = [], [], set()
    for class_name in sorted(tables):
        decls, defs, include = generate_c_for_class(class_name, tables[class_name])
        all_decls += [f"// -- {class_name} --"] + decls
        all_defs += [f"// -- {class_name} --"] + defs
        includes.add(include)

    include_lines = "\n".join(f'#include "{inc}"' for inc in sorted(includes))
    note = (
        "// Generated by codegen/generate_ctypes.py from\n"
        "// codegen/spec_attributes/*.json. Do not hand-edit this file; edit the\n"
        "// attribute tables and rebuild - CMake reruns the generator automatically\n"
        "// whenever a table or either generator script changes."
    )

    header = f"""#pragma once
{note}

#include "sed2_c/Runtime.h"

{chr(10).join(all_decls)}
"""
    source = f"""{note}

#include "sed2_c_api.h"

#include <cstddef>
#include <memory>
#include <string>

#include "sed2/core/Json.h"
{include_lines}

{chr(10).join(all_defs)}
"""
    with open(os.path.join(header_dir, "sed2_c_api.h"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(header)
    with open(os.path.join(source_dir, "sed2_c_api.cpp"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(source)


def write_python(out_dir, tables):
    python_dir = os.path.join(out_dir, "python")
    os.makedirs(python_dir, exist_ok=True)

    class_blocks = [generate_python_for_class(name, tables[name]) for name in sorted(tables)]
    content = PY_PREAMBLE + "\n\n" + "\n\n\n".join(class_blocks) + "\n"
    with open(os.path.join(python_dir, "sed2.py"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tables-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    tables = gc.load_tables(args.tables_dir)
    gc.populate_globals(tables)

    write_c_api(args.out_dir, tables)
    write_python(args.out_dir, tables)

    print(f"sed2: generated the C API shim and Python bindings for {len(tables)} class(es) into {args.out_dir}")


if __name__ == "__main__":
    main()
