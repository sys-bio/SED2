#include "sed2/core/AttributeTypes.h"

#include <cctype>

#include "sed2/core/RawElement.h"
#include "sed2/core/SEDBase.h"
#include "sed2/core/SEDDocument.h"

namespace sed2 {

bool isReference(const std::string& value) { return !value.empty() && value[0] == '#'; }

namespace {

bool isIdentStart(char c) { return std::isalpha(static_cast<unsigned char>(c)) != 0 || c == '_'; }
bool isIdentChar(char c) { return std::isalnum(static_cast<unsigned char>(c)) != 0 || c == '_'; }

// Reads [A-Za-z_][A-Za-z0-9_]* starting at pos and advances pos past it.
// Leaves pos untouched and returns false if there is no identifier there.
bool readIdentifier(const std::string& s, std::size_t& pos, std::string& out) {
    std::size_t start = pos;
    if (start >= s.size() || !isIdentStart(s[start])) return false;
    std::size_t i = start + 1;
    while (i < s.size() && isIdentChar(s[i])) ++i;
    out = s.substr(start, i - start);
    pos = i;
    return true;
}

// Reads an optionally-signed decimal integer starting at pos and advances
// pos past it. Leaves pos untouched and returns false if there isn't one.
bool readInteger(const std::string& s, std::size_t& pos, long long& out) {
    std::size_t start = pos;
    std::size_t i = start;
    if (i < s.size() && s[i] == '-') ++i;
    std::size_t digitsStart = i;
    while (i < s.size() && std::isdigit(static_cast<unsigned char>(s[i])) != 0) ++i;
    if (i == digitsStart) return false;
    out = std::stoll(s.substr(start, i - start));
    pos = i;
    return true;
}

// Scans the reference grammar
//   #name(:name | .name | [n] | [-n] | ['str'] | [a:b])*
// starting at s[start] ('#'), for as long as it keeps matching - it does
// not require reaching the end of 's'. If 'segmentsOut' is non-null, the
// parsed segments are appended to it. Returns the position just past the
// scanned span, or std::nullopt if there isn't even a minimally valid
// reference at 'start' (e.g. '#' not followed by an identifier, or a
// malformed bracket/colon/dot that was started but not completed).
std::optional<std::size_t> scanReference(const std::string& s, std::size_t start,
                                          std::vector<ReferencePathSegment>* segmentsOut) {
    if (start >= s.size() || s[start] != '#') return std::nullopt;

    std::size_t pos = start + 1;
    std::string rootName;
    if (!readIdentifier(s, pos, rootName)) return std::nullopt;
    if (segmentsOut) {
        ReferencePathSegment root;
        root.kind = ReferencePathSegment::Kind::Colon;
        root.name = rootName;
        segmentsOut->push_back(root);
    }

    while (pos < s.size()) {
        char c = s[pos];
        if (c == ':') {
            std::size_t attempt = pos + 1;
            std::string name;
            if (!readIdentifier(s, attempt, name)) break;  // not part of the reference
            pos = attempt;
            if (segmentsOut) {
                ReferencePathSegment seg;
                seg.kind = ReferencePathSegment::Kind::Colon;
                seg.name = name;
                segmentsOut->push_back(seg);
            }
        } else if (c == '.') {
            std::size_t attempt = pos + 1;
            std::string name;
            if (!readIdentifier(s, attempt, name)) break;
            pos = attempt;
            if (segmentsOut) {
                ReferencePathSegment seg;
                seg.kind = ReferencePathSegment::Kind::Dot;
                seg.name = name;
                segmentsOut->push_back(seg);
            }
        } else if (c == '[') {
            std::size_t attempt = pos + 1;
            if (attempt < s.size() && s[attempt] == '\'') {
                ++attempt;
                std::size_t valueStart = attempt;
                while (attempt < s.size() && s[attempt] != '\'') ++attempt;
                if (attempt >= s.size()) return std::nullopt;  // '[' commits us: unterminated string
                std::string value = s.substr(valueStart, attempt - valueStart);
                ++attempt;  // closing quote
                if (attempt >= s.size() || s[attempt] != ']') return std::nullopt;
                ++attempt;
                pos = attempt;
                if (segmentsOut) {
                    ReferencePathSegment seg;
                    seg.kind = ReferencePathSegment::Kind::IndexString;
                    seg.stringValue = value;
                    segmentsOut->push_back(seg);
                }
            } else {
                long long first = 0;
                if (!readInteger(s, attempt, first)) return std::nullopt;  // '[' commits us
                if (attempt < s.size() && s[attempt] == ':') {
                    ++attempt;
                    long long second = 0;
                    if (!readInteger(s, attempt, second)) return std::nullopt;
                    if (attempt >= s.size() || s[attempt] != ']') return std::nullopt;
                    ++attempt;
                    pos = attempt;
                    if (segmentsOut) {
                        ReferencePathSegment seg;
                        seg.kind = ReferencePathSegment::Kind::IndexSlice;
                        seg.intValue = first;
                        seg.intValue2 = second;
                        segmentsOut->push_back(seg);
                    }
                } else {
                    if (attempt >= s.size() || s[attempt] != ']') return std::nullopt;
                    ++attempt;
                    pos = attempt;
                    if (segmentsOut) {
                        ReferencePathSegment seg;
                        seg.kind = ReferencePathSegment::Kind::IndexInt;
                        seg.intValue = first;
                        segmentsOut->push_back(seg);
                    }
                }
            }
        } else {
            break;  // not part of the reference grammar; stop here
        }
    }
    return pos;
}

}  // namespace

std::optional<std::vector<ReferencePathSegment>> parseReferencePath(const std::string& ref) {
    std::vector<ReferencePathSegment> segments;
    auto end = scanReference(ref, 0, &segments);
    if (!end.has_value() || *end != ref.size()) return std::nullopt;
    return segments;
}

std::optional<std::size_t> scanReferenceLength(const std::string& s, std::size_t start) {
    auto end = scanReference(s, start, nullptr);
    if (!end.has_value()) return std::nullopt;
    return *end - start;
}

bool hasSubvalue(const std::vector<std::string>& declaredDotAccessors, const std::string& accessor) {
    if (accessor.empty()) return false;
    if (accessor[0] == '.') {
        std::string name = accessor.substr(1);
        for (const auto& declared : declaredDotAccessors) {
            if (declared == name) return true;
        }
        return false;
    }
    if (accessor[0] == '[') {
        // Reuses the reference grammar so the two can't drift apart: a
        // bracket accessor is plausible exactly when "#x" + accessor
        // parses as a two-segment reference.
        auto parsed = parseReferencePath("#x" + accessor);
        return parsed.has_value() && parsed->size() == 2;
    }
    return false;
}

namespace {

// Renders one trailing (post-colon-path) segment back into the accessor
// text hasSubvalue expects, e.g. Dot("model") -> ".model",
// IndexString("S1") -> "['S1']".
std::string renderTrailingAccessor(const ReferencePathSegment& segment) {
    switch (segment.kind) {
        case ReferencePathSegment::Kind::Dot:
            return "." + segment.name;
        case ReferencePathSegment::Kind::IndexString:
            return "['" + segment.stringValue + "']";
        case ReferencePathSegment::Kind::IndexInt:
            return "[" + std::to_string(segment.intValue) + "]";
        case ReferencePathSegment::Kind::IndexSlice:
            return "[" + std::to_string(segment.intValue) + ":" + std::to_string(segment.intValue2) + "]";
        case ReferencePathSegment::Kind::Colon:
            return "";  // not a trailing accessor; callers never pass one of these here
    }
    return "";
}

}  // namespace

void validateReference(const SEDBase& owner, const std::string& fieldName, const std::string& value,
                        std::vector<ValidationError>& errors) {
    if (!isReference(value)) return;

    SEDDocument* doc = owner.getSEDDocument();
    if (doc == nullptr) {
        errors.emplace_back("", "Unable to tell whether the referenced '" + value +
                                     "' exists, as no document was provided.",
                             fieldName, ValidationSeverity::Info);
        return;
    }

    const SEDBase* resolved = doc->getSEDReference(value);
    if (resolved == nullptr) {
        errors.emplace_back("", fieldName + ": referenced object '" + value + "' does not exist", fieldName,
                             ValidationSeverity::Error);
        return;
    }

    // The colon path resolved; anything after it (a trailing dot or
    // bracket accessor) can only be checked for plausibility, never
    // resolved to a concrete value (see Design.md, "Cross-references").
    auto segments = parseReferencePath(value);
    if (!segments.has_value()) return;

    // SEDDocument::getSEDReference only walks the first two colon
    // segments (root type + id); a reference can legitimately have more
    // colon segments than that (e.g. "#tasks:repeat:subTasks:sim1"), which
    // this class doesn't resolve any deeper yet. Those extra colon
    // segments are still part of the "bare" colon path, not a dot/bracket
    // accessor, so only a non-Colon segment past index 2 counts as one.
    bool hasTrailingAccessor = false;
    for (std::size_t i = 2; i < segments->size(); ++i) {
        if ((*segments)[i].kind != ReferencePathSegment::Kind::Colon) {
            hasTrailingAccessor = true;
            break;
        }
    }

    // RawElement means 'resolved's "_type" isn't one this library
    // recognizes - its declared dot-accessors and bare-reference-validity
    // are genuinely unknown, so there's nothing to plausibility-check.
    bool resolvedTypeKnown = dynamic_cast<const RawElement*>(resolved) == nullptr;
    if (!resolvedTypeKnown) return;

    if (!hasTrailingAccessor) {
        if (!resolved->isBareReferenceValid()) {
            errors.emplace_back("",
                                 fieldName + ": '" + value + "' refers to a whole " + resolved->getTypeName() +
                                     ", which has no meaningful value on its own - one of its declared "
                                     "subvalues (a dot accessor) is required",
                                 fieldName, ValidationSeverity::Warning);
        }
        return;
    }

    auto declared = resolved->getDeclaredDotAccessors();
    for (std::size_t i = 2; i < segments->size(); ++i) {
        const auto& segment = (*segments)[i];
        if (segment.kind == ReferencePathSegment::Kind::Colon) continue;  // part of the colon path, not an accessor
        std::string accessor = renderTrailingAccessor(segment);
        if (!hasSubvalue(declared, accessor)) {
            errors.emplace_back(
                "", fieldName + ": '" + accessor + "' is not a plausible subvalue accessor in '" + value + "'",
                fieldName, ValidationSeverity::Warning);
        }
    }
}

}  // namespace sed2
