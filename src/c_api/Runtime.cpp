#include "sed2_c/Runtime.h"

#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#include "sed2/core/Json.h"
#include "sed2/core/SEDBase.h"
#include "sed2/validation/ValidationError.h"

namespace {

thread_local std::string g_lastError;

sed2::Json errorsToJson(const std::vector<sed2::ValidationError>& errors) {
    sed2::Json array = sed2::Json::array();
    for (const auto& e : errors) {
        sed2::Json item = sed2::Json::object();
        item["code"] = e.code;
        item["message"] = e.message;
        item["path"] = e.path;
        item["severity"] = static_cast<int>(e.severity);
        array.push_back(item);
    }
    return array;
}

}  // namespace

namespace sed2_c {

void setLastError(const char* message) { g_lastError = message ? message : ""; }

char* allocString(const std::string& s) {
    char* buf = static_cast<char*>(std::malloc(s.size() + 1));
    if (buf) std::memcpy(buf, s.c_str(), s.size() + 1);
    return buf;
}

}  // namespace sed2_c

SED2_C_API const char* sed2_get_last_error(void) { return g_lastError.c_str(); }

SED2_C_API void sed2_free_string(char* s) { std::free(s); }

SED2_C_API void sed2_SEDBase_destroy(void* handle) { delete static_cast<sed2::SEDBase*>(handle); }

SED2_C_API char* sed2_SEDBase_getTypeName(void* handle) {
    SED2_TRY
    return sed2_c::allocString(static_cast<sed2::SEDBase*>(handle)->getTypeName());
    SED2_CATCH_RETURN(nullptr)
}

SED2_C_API int sed2_SEDBase_fromJSON(void* handle, const char* jsonText) {
    SED2_TRY
    sed2::Json json = sed2::Json::parse(jsonText);
    static_cast<sed2::SEDBase*>(handle)->fromJSON(json);
    return 0;
    SED2_CATCH_RETURN(-1)
}

SED2_C_API char* sed2_SEDBase_toJSON(void* handle) {
    SED2_TRY
    return sed2_c::allocString(static_cast<sed2::SEDBase*>(handle)->toJSON().dump());
    SED2_CATCH_RETURN(nullptr)
}

SED2_C_API char* sed2_SEDBase_validate(void* handle) {
    SED2_TRY
    std::vector<sed2::ValidationError> errors;
    static_cast<sed2::SEDBase*>(handle)->validate(errors);
    return sed2_c::allocString(errorsToJson(errors).dump());
    SED2_CATCH_RETURN(nullptr)
}

SED2_C_API void* sed2_SEDBase_getParent(void* handle) {
    SED2_TRY
    return static_cast<sed2::SEDBase*>(handle)->getParent();
    SED2_CATCH_RETURN(nullptr)
}

SED2_C_API void* sed2_SEDBase_getSEDDocument(void* handle) {
    SED2_TRY
    return static_cast<sed2::SEDBase*>(handle)->getSEDDocument();
    SED2_CATCH_RETURN(nullptr)
}

SED2_C_API char* sed2_SEDBase_getId(void* handle) {
    SED2_TRY
    return sed2_c::allocString(static_cast<sed2::SEDBase*>(handle)->getId());
    SED2_CATCH_RETURN(nullptr)
}
SED2_C_API void sed2_SEDBase_setId(void* handle, const char* value) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->setId(value ? value : "");
    SED2_CATCH_VOID
}
SED2_C_API int sed2_SEDBase_isSetId(void* handle) {
    SED2_TRY
    return static_cast<sed2::SEDBase*>(handle)->isSetId() ? 1 : 0;
    SED2_CATCH_RETURN(0)
}
SED2_C_API void sed2_SEDBase_unsetId(void* handle) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->unsetId();
    SED2_CATCH_VOID
}

SED2_C_API char* sed2_SEDBase_getName(void* handle) {
    SED2_TRY
    return sed2_c::allocString(static_cast<sed2::SEDBase*>(handle)->getName());
    SED2_CATCH_RETURN(nullptr)
}
SED2_C_API void sed2_SEDBase_setName(void* handle, const char* value) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->setName(value ? value : "");
    SED2_CATCH_VOID
}
SED2_C_API int sed2_SEDBase_isSetName(void* handle) {
    SED2_TRY
    return static_cast<sed2::SEDBase*>(handle)->isSetName() ? 1 : 0;
    SED2_CATCH_RETURN(0)
}
SED2_C_API void sed2_SEDBase_unsetName(void* handle) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->unsetName();
    SED2_CATCH_VOID
}

SED2_C_API char* sed2_SEDBase_getDescription(void* handle) {
    SED2_TRY
    return sed2_c::allocString(static_cast<sed2::SEDBase*>(handle)->getDescription());
    SED2_CATCH_RETURN(nullptr)
}
SED2_C_API void sed2_SEDBase_setDescription(void* handle, const char* value) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->setDescription(value ? value : "");
    SED2_CATCH_VOID
}
SED2_C_API int sed2_SEDBase_isSetDescription(void* handle) {
    SED2_TRY
    return static_cast<sed2::SEDBase*>(handle)->isSetDescription() ? 1 : 0;
    SED2_CATCH_RETURN(0)
}
SED2_C_API void sed2_SEDBase_unsetDescription(void* handle) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->unsetDescription();
    SED2_CATCH_VOID
}

SED2_C_API char* sed2_SEDBase_getNotes(void* handle) {
    SED2_TRY
    return sed2_c::allocString(static_cast<sed2::SEDBase*>(handle)->getNotes());
    SED2_CATCH_RETURN(nullptr)
}
SED2_C_API void sed2_SEDBase_setNotes(void* handle, const char* value) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->setNotes(value ? value : "");
    SED2_CATCH_VOID
}
SED2_C_API int sed2_SEDBase_isSetNotes(void* handle) {
    SED2_TRY
    return static_cast<sed2::SEDBase*>(handle)->isSetNotes() ? 1 : 0;
    SED2_CATCH_RETURN(0)
}
SED2_C_API void sed2_SEDBase_unsetNotes(void* handle) {
    SED2_TRY
    static_cast<sed2::SEDBase*>(handle)->unsetNotes();
    SED2_CATCH_VOID
}
