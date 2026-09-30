// Reference syntax (Design.md's Cross-references section, core-spec.md
// Section 4): a reference is '#' + a colon-delimited containment path + an
// optional chain of dot-accessors / bracket-indices, e.g.
// "#tasks:loop1:subTasks:sim1.model['S1']". parse_reference() is pure syntax
// (never touches a document) - the C++ port of the reference implementation's
// _parse_reference / ParsedReference / RefIndex (see generator/emit_python.py's
// RUNTIME). Also carries RefFieldInfo, the per-field facts the reference
// dispatcher needs (RefRules.hpp).
//
// Hand-written template (templates/cpp/runtime/Reference.hpp), copied into
// the generated include tree by generator/emit_cpp.py with the literal
// namespace name "libsed2" rewritten to --cpp-namespace. ASCII only.
#pragma once

#include <cctype>
#include <optional>
#include <string>
#include <vector>

#include "PyFormat.hpp"

namespace libsed2 {

class SedBase;

struct RefIndex {
    enum Kind { INT, LABEL, RANGE };
    Kind kind = INT;
    long long ival = 0;                 // INT
    std::string sval;                   // LABEL
    std::optional<long long> a, b;      // RANGE ends (nullopt = open)

    bool is_int() const { return kind == INT; }
    bool is_label() const { return kind == LABEL; }
    bool is_range() const { return kind == RANGE; }

    /// str() of the reference implementation's own `.value` for this index:
    /// an int, the label text, or the tuple "(a, b)" with None for open ends.
    std::string value_str() const {
        if (kind == INT) return std::to_string(ival);
        if (kind == LABEL) return sval;
        return "(" + (a ? std::to_string(*a) : std::string("None")) + ", " +
               (b ? std::to_string(*b) : std::string("None")) + ")";
    }
};

struct Accessor {
    bool is_dot = false;
    std::string name;      // dot accessor name
    RefIndex index;        // bracket index
};

struct ParsedReference {
    std::string raw;
    std::optional<std::string> collection;   // segment right after '#', or nullopt if empty
    std::vector<std::string> path;           // colon-segments after the collection
    std::vector<Accessor> accessors;         // in order

    std::optional<std::string> first_dot() const {
        for (const auto& acc : accessors) if (acc.is_dot) return acc.name;
        return std::nullopt;
    }
    std::vector<RefIndex> indices() const {
        std::vector<RefIndex> out;
        for (const auto& acc : accessors) if (!acc.is_dot) out.push_back(acc.index);
        return out;
    }
};

namespace refparse {

inline std::string strip(const std::string& s) {
    size_t i = 0, j = s.size();
    while (i < j && std::isspace(static_cast<unsigned char>(s[i]))) i++;
    while (j > i && std::isspace(static_cast<unsigned char>(s[j - 1]))) j--;
    return s.substr(i, j - i);
}

/// Python int(text) for a base-10 literal (sign, digits, single underscores
/// between digits); false when text is not one.
inline bool parse_int(const std::string& text, long long& out) {
    std::string t = strip(text);
    size_t i = 0;
    bool neg = false;
    if (i < t.size() && (t[i] == '+' || t[i] == '-')) { neg = t[i] == '-'; i++; }
    if (i >= t.size()) return false;
    long long v = 0;
    bool prev_digit = false;
    for (; i < t.size(); i++) {
        char c = t[i];
        if (c >= '0' && c <= '9') {
            if (v > (9223372036854775807LL - (c - '0')) / 10) v = 9223372036854775807LL / 10;  // saturate
            v = v * 10 + (c - '0');
            prev_digit = true;
        } else if (c == '_' && prev_digit && i + 1 < t.size() && t[i + 1] >= '0' && t[i + 1] <= '9') {
            prev_digit = false;
        } else {
            return false;
        }
    }
    out = neg ? -v : v;
    return true;
}

inline RefIndex parse_index(const std::string& raw_part) {
    std::string part = strip(raw_part);
    RefIndex idx;
    size_t colon = part.find(':');
    if (colon != std::string::npos) {
        std::string a = part.substr(0, colon), b = part.substr(colon + 1);
        long long av = 0, bv = 0;
        bool ok = true;
        std::optional<long long> ra, rb;
        if (!strip(a).empty()) { if (parse_int(a, av)) ra = av; else ok = false; }
        if (!strip(b).empty()) { if (parse_int(b, bv)) rb = bv; else ok = false; }
        if (ok) {
            idx.kind = RefIndex::RANGE;
            idx.a = ra;
            idx.b = rb;
            return idx;
        }
        idx.kind = RefIndex::LABEL;   // not a valid range: never throw
        idx.sval = part;
        return idx;
    }
    if (part.size() >= 2 && part.front() == part.back() && (part.front() == '\'' || part.front() == '"')) {
        idx.kind = RefIndex::LABEL;
        idx.sval = part.substr(1, part.size() - 2);
        return idx;
    }
    long long iv = 0;
    if (parse_int(part, iv)) {
        idx.kind = RefIndex::INT;
        idx.ival = iv;
        return idx;
    }
    idx.kind = RefIndex::LABEL;   // bare unquoted label - lenient fallback
    idx.sval = part;
    return idx;
}

inline std::vector<std::string> split_colon(const std::string& s) {
    std::vector<std::string> out;
    size_t start = 0;
    while (true) {
        size_t p = s.find(':', start);
        if (p == std::string::npos) { out.push_back(s.substr(start)); break; }
        out.push_back(s.substr(start, p - start));
        start = p + 1;
    }
    return out;
}

}  // namespace refparse

inline ParsedReference parse_reference(const std::string& text) {
    ParsedReference pr;
    pr.raw = text;
    std::string body = (!text.empty() && text[0] == '#') ? text.substr(1) : text;
    size_t m = body.find_first_of(".[");
    std::string path_part = m == std::string::npos ? body : body.substr(0, m);
    std::string accessor_part = m == std::string::npos ? std::string() : body.substr(m);
    if (!path_part.empty()) {
        auto segments = refparse::split_colon(path_part);
        pr.collection = segments[0];
        pr.path.assign(segments.begin() + 1, segments.end());
    }
    size_t i = 0, n = accessor_part.size();
    while (i < n) {
        char ch = accessor_part[i];
        if (ch == '.') {
            size_t j = i + 1;
            if (j >= n || !(std::isalpha(static_cast<unsigned char>(accessor_part[j])) || accessor_part[j] == '_')) break;
            size_t k = j + 1;
            while (k < n && (std::isalnum(static_cast<unsigned char>(accessor_part[k])) || accessor_part[k] == '_')) k++;
            Accessor acc;
            acc.is_dot = true;
            acc.name = accessor_part.substr(j, k - j);
            pr.accessors.push_back(acc);
            i = k;
        } else if (ch == '[') {
            size_t close = accessor_part.find(']', i);
            if (close == std::string::npos) break;
            std::string inner = accessor_part.substr(i + 1, close - i - 1);
            size_t start = 0;
            while (true) {
                size_t comma = inner.find(',', start);
                std::string part = inner.substr(start, comma == std::string::npos ? std::string::npos : comma - start);
                if (!refparse::strip(part).empty()) {
                    Accessor acc;
                    acc.is_dot = false;
                    acc.index = refparse::parse_index(part);
                    pr.accessors.push_back(acc);
                }
                if (comma == std::string::npos) break;
                start = comma + 1;
            }
            i = close + 1;
        } else {
            break;
        }
    }
    return pr;
}

/// What every handwritten rule's check() needs to word its message: the
/// referring element's class/id, the attribute, the JSON-pointer location and
/// the field's own value (the reference string, for the reference rules) - the
/// C++ analog of the reference implementation's class_name/id_value/attr/
/// location/value keyword arguments.
struct RuleCtx {
    std::string class_name;
    std::string id_value;
    std::string attr;
    std::string location;
    std::string value;
};

/// Per-field facts the reference dispatcher (RefRules::check_reference_field)
/// needs: the port of the reference implementation's keyword arguments
/// field_kind / ref_type_rule_id / expected_enum / constraints / ref_target.
/// An empty field_kind means "no field-level ref-type rule" (a per-entry
/// DictOrRef reference, an any-kind field).
struct RefFieldInfo {
    std::string field_kind;
    std::optional<std::string> ref_type_rule_id;
    const std::vector<std::string>* expected_enum = nullptr;
    std::optional<double> minimum;
    std::optional<double> exclusive_minimum;
    std::optional<std::string> item_kind;
    std::optional<std::string> ref_target;
};

}  // namespace libsed2
