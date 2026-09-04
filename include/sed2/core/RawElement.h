#pragma once

#include "sed2/core/SEDBase.h"

namespace sed2 {

// Fallback for a child object whose "_type" isn't registered with
// TypeRegistry - a spec class this library doesn't implement yet, or a
// document written by a newer library version using a type this one
// predates. Stores the object's JSON verbatim so documents that use
// classes outside this library's current coverage still load and
// round-trip without losing data (see Design.md's rationale for choosing
// nlohmann::json in the first place, extended here to whole unrecognized
// elements, not just unrecognized attributes).
class RawElement : public SEDBase {
public:
    std::string getTypeName() const override;
    void fromJSON(const Json& json) override;
    Json toJSON() const override;
    void validate(std::vector<ValidationError>& errors) const override;

private:
    std::string typeName_;
    Json raw_ = Json::object();
};

}  // namespace sed2
