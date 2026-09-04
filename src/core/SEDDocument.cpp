#include "sed2/core/SEDDocument.h"

#include <fstream>
#include <sstream>

#include "sed2/validation/SchemaValidator.h"

namespace sed2 {

SEDDocument SEDDocument::fromFile(const std::string& path, std::string* errorMessage) {
    std::ifstream in(path);
    if (!in) {
        if (errorMessage) *errorMessage = "sed2: could not open file: " + path;
        return SEDDocument();
    }
    std::ostringstream buffer;
    buffer << in.rdbuf();
    return fromJSONString(buffer.str(), errorMessage);
}

SEDDocument SEDDocument::fromJSONString(const std::string& text, std::string* errorMessage) {
    SEDDocument document;
    try {
        Json json = Json::parse(text);
        document.fromJSON(json);
    } catch (const std::exception& e) {
        if (errorMessage) *errorMessage = std::string("sed2: could not parse SED2 document: ") + e.what();
    }
    return document;
}

bool SEDDocument::toFile(const std::string& path) const {
    std::ofstream out(path);
    if (!out) return false;
    out << toJSON().dump(2);
    return static_cast<bool>(out);
}

Json SEDDocument::toJSON() const {
    Json json = generated::SEDDocument::toJSON();
    json.erase("_type");
    return json;
}

SEDDocument* SEDDocument::getSEDDocument() const { return const_cast<SEDDocument*>(this); }

const SEDBase* SEDDocument::getSEDReference(const std::string& ref) const {
    auto segments = parseReferencePath(ref);
    if (!segments.has_value() || segments->empty()) return nullptr;

    const auto& root = (*segments)[0];
    if (root.kind != ReferencePathSegment::Kind::Colon) return nullptr;
    if (segments->size() < 2 || (*segments)[1].kind != ReferencePathSegment::Kind::Colon) return nullptr;
    const std::string& id = (*segments)[1].name;

    // Only the colon path is resolved to a pointer; any dot/bracket
    // segments after it are left alone (see the header comment).
    if (root.name == "tasks") return getTask(id);
    if (root.name == "outputs") return getOutput(id);
    if (root.name == "styles") return getStyle(id);
    return nullptr;
}

void SEDDocument::validate(std::vector<ValidationError>& errors) const {
    SchemaValidator schemaValidator;
    schemaValidator.validate(toJSON(), errors);
    generated::SEDDocument::validate(errors);
}

}  // namespace sed2
