#include "sed2/core/RawElement.h"

namespace sed2 {

std::string RawElement::getTypeName() const { return typeName_; }

void RawElement::fromJSON(const Json& json) {
    raw_ = json;
    if (json.contains("_type")) typeName_ = json.at("_type").get<std::string>();
    SEDBase::fromJSON(json);
}

Json RawElement::toJSON() const {
    // Returns the object exactly as read rather than SEDBase::toJSON()
    // plus attributes: since this class has no attribute list for this
    // type, reconstructing the object piecemeal risks dropping or
    // reordering fields it doesn't understand.
    return raw_;
}

void RawElement::validate(std::vector<ValidationError>& errors) const {
    (void)errors;  // This library has no model for this type, so nothing to check.
}

}  // namespace sed2
