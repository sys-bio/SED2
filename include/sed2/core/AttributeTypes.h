#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <vector>

#include "sed2/core/Json.h"
#include "sed2/validation/ValidationError.h"

namespace sed2 {

class SEDBase;

using SId = std::string;
using SIdRef = std::string;
using KISAOId = std::string;
using URI = std::string;
using URN = std::string;
using MarkdownString = std::string;

// True if 'value' is a SED2 reference (an SIdRef) rather than a literal
// value, i.e. it starts with '#'. Any attribute documented in the spec as
// "value-or-reference" uses this to tell the two apart at runtime.
bool isReference(const std::string& value);

// One segment of a parsed reference path, e.g. "#tasks:sim1.model['S1']"
// parses to: Colon("tasks"), Colon("sim1"), Dot("model"), IndexString("S1").
// The very first segment (the name right after '#') is also a Colon
// segment - it names the root object being referenced.
struct ReferencePathSegment {
    enum class Kind { Colon, Dot, IndexInt, IndexString, IndexSlice };

    Kind kind = Kind::Colon;
    std::string name;         // Colon / Dot: the identifier
    std::string stringValue;  // IndexString: the quoted key
    long long intValue = 0;   // IndexInt / IndexSlice: start
    long long intValue2 = 0;  // IndexSlice: end
};

// Parses an SIdRef of the form
//   #name(:name | .name | [n] | [-n] | ['str'] | [a:b])*
// into its segments. Returns std::nullopt if 'ref' is not a syntactically
// valid reference (a malformed reference still satisfies isReference(),
// since that only looks at the leading '#' - this is the deeper check).
std::optional<std::vector<ReferencePathSegment>> parseReferencePath(const std::string& ref);

// Scans the longest reference span starting at s[start] (which must be
// '#'), without requiring it to run to the end of 's'. Used by the math
// Lexer, where a reference is embedded inside a larger expression (e.g.
// "#tasks:sim1.value + 1") rather than being the whole string. Returns the
// span's length, or std::nullopt if s[start] isn't the start of even a
// minimally valid reference (bare '#' with no name after it, or similar).
std::optional<std::size_t> scanReferenceLength(const std::string& s, std::size_t start);

// Syntactic plausibility check for one trailing accessor (a single dot
// accessor like ".model", or a single bracket index like "['S1']", "[3]",
// or "[0:5]") against the set of subelement names a class declares as
// valid dot-accessors. Bracket accessors are always syntactically
// plausible; this function checks the accessor's *shape* only - the value
// it resolves to is a run-time quantity that only exists once the
// experiment described by the document actually executes, so it can never
// be resolved to a pointer ahead of time (see Design.md, "Cross-references").
bool hasSubvalue(const std::vector<std::string>& declaredDotAccessors, const std::string& accessor);

// Checks one reference-typed attribute value ('value', read from
// 'fieldName' on 'owner') against the document 'owner' belongs to, and
// appends whatever it finds to 'errors'. A no-op if 'value' isn't a
// reference at all (see isReference). Otherwise:
//   - no document reachable from 'owner' (SEDBase::getSEDDocument returned
//     nullptr, e.g. an object built standalone in a test): appends an Info
//     saying the reference couldn't be checked, not that anything is wrong.
//   - the colon-path prefix doesn't resolve in the document
//     (SEDDocument::getSEDReference returned nullptr): appends an Error.
//   - it resolves to a RawElement (an unrecognized "_type"): nothing
//     further is checked - its declared accessors/bare-reference-validity
//     aren't known.
//   - it resolves with no trailing dot/bracket accessor (a "bare"
//     reference - colon segments beyond the first two, which
//     getSEDReference doesn't walk yet, still count as part of the bare
//     colon path, not an accessor) and the resolved class says a bare
//     reference to it isn't meaningful (SEDBase::isBareReferenceValid):
//     appends a Warning.
//   - it resolves with a trailing accessor that isn't even syntactically
//     well-formed (bracket) or isn't one the resolved class declares
//     (dot - see SEDBase::getDeclaredDotAccessors and V0002): appends a
//     Warning, since a subvalue accessor can only ever be a plausibility
//     check (Design.md, "Cross-references").
void validateReference(const SEDBase& owner, const std::string& fieldName, const std::string& value,
                        std::vector<ValidationError>& errors);

// A value that is either a literal T or a reference to one - any attribute
// the spec documents as a "*OrRef" whose literal form isn't itself a
// string (NumberOrRef, IntegerOrRef, BooleanOrRef; the schema's
// Positive*/NonNegative* variants reuse these too - their extra numeric
// constraint is a JSON Schema range check SchemaValidator already
// enforces, not a distinct C++ type). A string-typed "*OrRef" attribute
// (StringOrRef, SIdRef, KISAOIdOrRef, URIOrRef, ScaleTypeOrRef, ...) needs
// no wrapper at all - it's already a plain std::string, and isReference()
// works directly on it.
template <typename T>
struct ValueOrRef {
    bool isRef = false;
    T value{};
    std::string refValue;

    ValueOrRef() = default;
    ValueOrRef(T v) : isRef(false), value(v) {}

    static ValueOrRef<T> fromReference(std::string ref) {
        ValueOrRef<T> result;
        result.isRef = true;
        result.refValue = std::move(ref);
        return result;
    }

    // Needed by the scalarList remove<Item>(const T&) codegen produces
    // (std::find over a vector<ValueOrRef<T>>); also generally useful for
    // round-trip comparisons in tests.
    friend bool operator==(const ValueOrRef<T>& lhs, const ValueOrRef<T>& rhs) {
        if (lhs.isRef != rhs.isRef) return false;
        return lhs.isRef ? lhs.refValue == rhs.refValue : lhs.value == rhs.value;
    }
    friend bool operator!=(const ValueOrRef<T>& lhs, const ValueOrRef<T>& rhs) { return !(lhs == rhs); }
};

using NumberOrRef = ValueOrRef<double>;
using IntegerOrRef = ValueOrRef<int64_t>;
using BooleanOrRef = ValueOrRef<bool>;

// Lets nlohmann::json (de)serialize a ValueOrRef<T> through the same
// generic json.at(name).get<T>() / json[name] = value codegen already
// uses for every other scalar attribute - found via ADL (nlohmann's
// adl_serializer looks up an unqualified to_json/from_json, and both
// ValueOrRef and these overloads live in namespace sed2).
template <typename T>
void to_json(Json& j, const ValueOrRef<T>& v) {
    if (v.isRef) {
        j = v.refValue;
    } else {
        j = v.value;
    }
}

template <typename T>
void from_json(const Json& j, ValueOrRef<T>& v) {
    if (j.is_string()) {
        v = ValueOrRef<T>::fromReference(j.get<std::string>());
    } else {
        v = ValueOrRef<T>(j.get<T>());
    }
}

}  // namespace sed2
