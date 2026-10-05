// Hand-written half of the JavaScript (Emscripten) API: the fixed, spec-
// independent entry points. Copied, with its #include/using-namespace lines
// rewritten to match --cpp-namespace, to <out>/js/src/api.cpp by
// generator/emit_js.py. The spec-dependent entry points (library version,
// document version, class names) are generated into src/generated_api.cpp
// by the same emitter - see Design.md's Code Generation section.
//
// Shape, following libantimonyjs: a flat C API (extern "C", exported to
// JavaScript through Emscripten's cwrap), strings in and strings out. Every
// result is JSON text; the returned pointer addresses a buffer that is valid
// until the next call into this API, so the caller (index.js) copies it out
// immediately. SED2 documents are JSON, so unlike libantimonyjs there is no
// separate wire format to invent.
//
//   sed2_validate_document(text)      -> {"ok":true,"problems":[...]} | {"ok":false,"error":"..."}
//   sed2_validate_object(key, text)   -> same; validates one "direct-only" class instance
//   sed2_normalize_document(text)     -> {"ok":true,"text":"..."} | {"ok":false,"error":"..."}
//   sed2_check_math(text)             -> {"ok":true} | {"ok":false,"error":"..."}
//   sed2_rule_catalog()               -> {"<RuleID>":{"rule":...,"message":...,"severity":...},...}
//   sed2_direct_only_keys()           -> ["<RuleID>",...]
//
// A problem is {"ruleId","severity","rule","message","location"}. "ok":false
// means the input could not be processed at all (malformed JSON, a malformed
// math string); validation findings are "ok":true with a non-empty problems
// array.

#include <sed2test/DirectOnly.hpp>
#include <sed2test/Io.hpp>
#include <sed2test/MathAst.hpp>

#include <emscripten.h>

#include <exception>
#include <map>
#include <string>
#include <vector>

using namespace sed2test;

namespace {

std::string g_result;

const char* give(const Json& j) {
    g_result.clear();
    j.dump(g_result);
    return g_result.c_str();
}

Json failure(const std::string& message) {
    Json r = Json::object();
    r["ok"] = false;
    r["error"] = message;
    return r;
}

Json problems_result(const std::vector<ValidationProblem>& problems) {
    Json list = Json::array();
    for (const auto& p : problems) {
        Json o = Json::object();
        o["ruleId"] = p.rule_id;
        o["severity"] = p.severity;
        o["rule"] = p.rule;
        o["message"] = p.message;
        o["location"] = p.location;
        list.push_back(std::move(o));
    }
    Json r = Json::object();
    r["ok"] = true;
    r["problems"] = std::move(list);
    return r;
}

}  // namespace

extern "C" {

EMSCRIPTEN_KEEPALIVE const char* sed2_validate_document(const char* text) {
    try {
        auto doc = read_from_string(text ? text : "");
        return give(problems_result(doc->validate()));
    } catch (const std::exception& e) {
        return give(failure(e.what()));
    } catch (...) {
        return give(failure("unknown error"));
    }
}

EMSCRIPTEN_KEEPALIVE const char* sed2_validate_object(const char* key, const char* text) {
    try {
        register_rules();
        const auto& direct = direct_only_classes();
        auto it = direct.find(key ? key : "");
        if (it == direct.end()) return give(failure(std::string("not a direct-only class key: ") + (key ? key : "")));
        Json raw = Json::parse(text ? text : "");
        std::unique_ptr<SedBase> obj = it->second();
        load_fields(obj.get(), raw);
        return give(problems_result(obj->validate()));
    } catch (const std::exception& e) {
        return give(failure(e.what()));
    } catch (...) {
        return give(failure("unknown error"));
    }
}

EMSCRIPTEN_KEEPALIVE const char* sed2_normalize_document(const char* text) {
    try {
        auto doc = read_from_string(text ? text : "");
        Json r = Json::object();
        r["ok"] = true;
        r["text"] = write_to_string(*doc);
        return give(r);
    } catch (const std::exception& e) {
        return give(failure(e.what()));
    } catch (...) {
        return give(failure("unknown error"));
    }
}

EMSCRIPTEN_KEEPALIVE const char* sed2_check_math(const char* text) {
    try {
        math_parse(text ? text : "");
        Json r = Json::object();
        r["ok"] = true;
        return give(r);
    } catch (const std::exception& e) {
        return give(failure(e.what()));
    } catch (...) {
        return give(failure("unknown error"));
    }
}

EMSCRIPTEN_KEEPALIVE const char* sed2_rule_catalog() {
    register_rules();
    std::map<std::string, RuleCatalog::Entry> sorted(RuleCatalog::catalog().begin(), RuleCatalog::catalog().end());
    Json r = Json::object();
    for (const auto& kv : sorted) {
        Json o = Json::object();
        o["rule"] = kv.second.rule;
        o["message"] = kv.second.message_template;
        o["severity"] = kv.second.severity;
        r[kv.first] = std::move(o);
    }
    return give(r);
}

EMSCRIPTEN_KEEPALIVE const char* sed2_direct_only_keys() {
    Json r = Json::array();
    for (const auto& kv : direct_only_classes()) r.push_back(kv.first);
    return give(r);
}

}  // extern "C"
