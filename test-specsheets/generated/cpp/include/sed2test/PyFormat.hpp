// Json alias plus the small "Python-compatible" value helpers the reference
// checks need: Python's str()/repr() of a decoded JSON value (validation
// messages interpolate placeholders with str(), so byte-identical messages
// across the three targets need the same rendering), json.dumps() (used for a
// constant's {resolved-value}), and Python equality/truthiness on decoded
// JSON (outputs.json's expr notation is evaluated with Python semantics in
// the reference implementation).
//
// Hand-written template (templates/cpp/runtime/PyFormat.hpp), copied into
// the generated include tree by generator/emit_cpp.py with the literal
// namespace name "sed2test" rewritten to --cpp-namespace. ASCII only.
#pragma once

#include <jsoncons/json.hpp>

#include <charconv>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <string>

namespace sed2test {

using Json = jsoncons::ojson;

namespace pyfmt {

/// Python's repr(float): shortest round-trip digits, fixed notation for
/// 1e-4 <= |x| < 1e16, otherwise "d.ddde+XX" with at least two exponent digits.
inline std::string float_repr(double v) {
    if (std::isnan(v)) return "nan";
    if (std::isinf(v)) return v < 0 ? "-inf" : "inf";
    if (v == 0.0) return std::signbit(v) ? "-0.0" : "0.0";
    char buf[64];
    auto res = std::to_chars(buf, buf + sizeof(buf), v, std::chars_format::scientific);
    std::string sci(buf, res.ptr);  // e.g. "-1.2345e+02" or "5e-05"
    bool neg = false;
    size_t pos = 0;
    if (sci[0] == '-') { neg = true; pos = 1; }
    size_t epos = sci.find('e');
    std::string mant = sci.substr(pos, epos - pos);
    int exp10 = std::stoi(sci.substr(epos + 1));
    std::string digits;
    for (char c : mant) if (c != '.') digits += c;
    // value = 0.DIGITS * 10^decpt
    int decpt = exp10 + 1;
    std::string out;
    if (decpt > 16 || decpt < -3) {
        out = digits.substr(0, 1);
        if (digits.size() > 1) out += "." + digits.substr(1);
        char eb[16];
        std::snprintf(eb, sizeof(eb), "e%c%02d", exp10 < 0 ? '-' : '+', exp10 < 0 ? -exp10 : exp10);
        out += eb;
    } else if (decpt <= 0) {
        out = "0." + std::string(static_cast<size_t>(-decpt), '0') + digits;
    } else if (static_cast<size_t>(decpt) >= digits.size()) {
        out = digits + std::string(static_cast<size_t>(decpt) - digits.size(), '0') + ".0";
    } else {
        out = digits.substr(0, static_cast<size_t>(decpt)) + "." + digits.substr(static_cast<size_t>(decpt));
    }
    return neg ? "-" + out : out;
}

inline std::string int_str(const Json& v) {
    if (v.is_uint64()) return std::to_string(v.as<uint64_t>());
    return std::to_string(v.as<int64_t>());
}

/// Python repr() of a str.
inline std::string str_repr(const std::string& s) {
    bool has_single = s.find('\'') != std::string::npos;
    bool has_double = s.find('"') != std::string::npos;
    char q = (has_single && !has_double) ? '"' : '\'';
    std::string out(1, q);
    for (unsigned char c : s) {
        if (c == static_cast<unsigned char>(q) || c == '\\') { out += '\\'; out += static_cast<char>(c); }
        else if (c == '\n') out += "\\n";
        else if (c == '\r') out += "\\r";
        else if (c == '\t') out += "\\t";
        else if (c < 0x20 || c == 0x7f) {
            char b[8];
            std::snprintf(b, sizeof(b), "\\x%02x", c);
            out += b;
        } else out += static_cast<char>(c);
    }
    out += q;
    return out;
}

/// Python repr() of a decoded JSON value.
inline std::string repr(const Json& v) {
    if (v.is_null()) return "None";
    if (v.is_bool()) return v.as<bool>() ? "True" : "False";
    if (v.is_string()) return str_repr(v.as<std::string>());
    if (v.is_double()) return float_repr(v.as<double>());
    if (v.is_number()) return int_str(v);
    if (v.is_array()) {
        std::string out = "[";
        bool first = true;
        for (const auto& e : v.array_range()) {
            if (!first) out += ", ";
            first = false;
            out += repr(e);
        }
        return out + "]";
    }
    if (v.is_object()) {
        std::string out = "{";
        bool first = true;
        for (const auto& kv : v.object_range()) {
            if (!first) out += ", ";
            first = false;
            out += str_repr(std::string(kv.key())) + ": " + repr(kv.value());
        }
        return out + "}";
    }
    return "None";
}

/// Python str() of a decoded JSON value: a string is itself, anything else
/// its repr().
inline std::string str(const Json& v) {
    if (v.is_string()) return v.as<std::string>();
    return repr(v);
}

inline void append_u16(std::string& out, unsigned cp) {
    char b[16];
    std::snprintf(b, sizeof(b), "\\u%04x", cp & 0xFFFF);
    out += b;
}

/// Python json.dumps() string quoting (ensure_ascii=True).
inline std::string dumps_string(const std::string& s) {
    std::string out = "\"";
    size_t i = 0, n = s.size();
    while (i < n) {
        unsigned char c = static_cast<unsigned char>(s[i]);
        if (c < 0x80) {
            switch (c) {
                case '"': out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\n': out += "\\n"; break;
                case '\r': out += "\\r"; break;
                case '\t': out += "\\t"; break;
                case '\b': out += "\\b"; break;
                case '\f': out += "\\f"; break;
                default:
                    if (c < 0x20) append_u16(out, c);
                    else out += static_cast<char>(c);
            }
            i++;
            continue;
        }
        unsigned cp = 0;
        size_t len = 1;
        if ((c & 0xE0) == 0xC0) { cp = c & 0x1F; len = 2; }
        else if ((c & 0xF0) == 0xE0) { cp = c & 0x0F; len = 3; }
        else if ((c & 0xF8) == 0xF0) { cp = c & 0x07; len = 4; }
        else { cp = c; len = 1; }
        for (size_t k = 1; k < len && i + k < n; k++) cp = (cp << 6) | (static_cast<unsigned char>(s[i + k]) & 0x3F);
        i += len;
        if (cp >= 0x10000) {
            cp -= 0x10000;
            append_u16(out, 0xD800 + (cp >> 10));
            append_u16(out, 0xDC00 + (cp & 0x3FF));
        } else {
            append_u16(out, cp);
        }
    }
    return out + "\"";
}

/// Python json.dumps() of a decoded JSON value (default separators).
inline std::string dumps(const Json& v) {
    if (v.is_null()) return "null";
    if (v.is_bool()) return v.as<bool>() ? "true" : "false";
    if (v.is_string()) return dumps_string(v.as<std::string>());
    if (v.is_double()) return float_repr(v.as<double>());
    if (v.is_number()) return int_str(v);
    if (v.is_array()) {
        std::string out = "[";
        bool first = true;
        for (const auto& e : v.array_range()) {
            if (!first) out += ", ";
            first = false;
            out += dumps(e);
        }
        return out + "]";
    }
    if (v.is_object()) {
        std::string out = "{";
        bool first = true;
        for (const auto& kv : v.object_range()) {
            if (!first) out += ", ";
            first = false;
            out += dumps_string(std::string(kv.key())) + ": " + dumps(kv.value());
        }
        return out + "}";
    }
    return "null";
}

inline bool is_num(const Json& v) { return v.is_number(); }  // a JSON bool is never a number here

inline double as_double(const Json& v) {
    if (v.is_bool()) return v.as<bool>() ? 1.0 : 0.0;
    return v.as<double>();
}

/// Python == on decoded JSON (bool == int, 1 == 1.0, dicts unordered).
inline bool equal(const Json& a, const Json& b) {
    bool an = a.is_number() || a.is_bool(), bn = b.is_number() || b.is_bool();
    if (an && bn) return as_double(a) == as_double(b);
    if (a.is_null() && b.is_null()) return true;
    if (a.is_string() && b.is_string()) return a.as<std::string>() == b.as<std::string>();
    if (a.is_array() && b.is_array()) {
        if (a.size() != b.size()) return false;
        for (size_t i = 0; i < a.size(); i++) if (!equal(a[i], b[i])) return false;
        return true;
    }
    if (a.is_object() && b.is_object()) {
        if (a.size() != b.size()) return false;
        for (const auto& kv : a.object_range()) {
            if (!b.contains(kv.key()) || !equal(kv.value(), b.at(kv.key()))) return false;
        }
        return true;
    }
    return false;
}

/// Python bool() of a decoded JSON value.
inline bool truthy(const Json& v) {
    if (v.is_null()) return false;
    if (v.is_bool()) return v.as<bool>();
    if (v.is_number()) return v.as<double>() != 0.0;
    if (v.is_string()) return !v.as<std::string>().empty();
    if (v.is_array() || v.is_object()) return v.size() > 0;
    return true;
}

}  // namespace pyfmt

}  // namespace sed2test
