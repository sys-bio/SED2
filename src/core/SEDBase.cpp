#include "sed2/core/SEDBase.h"

namespace sed2 {

namespace {
const std::string kEmptyString;
const std::vector<Annotation> kEmptyAnnotations;

// Attribute names SEDBase itself reads out of the JSON object; anything
// else falls through to unrecognizedFields_.
bool isSedBaseAttribute(const std::string& key) {
    return key == "_type" || key == "id" || key == "name" || key == "description" ||
           key == "notes" || key == "annotations";
}
}  // namespace

const std::string& SEDBase::getId() const { return id_.has_value() ? *id_ : kEmptyString; }
void SEDBase::setId(const std::string& id) { id_ = id; }
bool SEDBase::isSetId() const { return id_.has_value(); }
void SEDBase::unsetId() { id_.reset(); }

const std::string& SEDBase::getName() const { return name_.has_value() ? *name_ : kEmptyString; }
void SEDBase::setName(const std::string& name) { name_ = name; }
bool SEDBase::isSetName() const { return name_.has_value(); }
void SEDBase::unsetName() { name_.reset(); }

const std::string& SEDBase::getDescription() const {
    return description_.has_value() ? *description_ : kEmptyString;
}
void SEDBase::setDescription(const std::string& description) { description_ = description; }
bool SEDBase::isSetDescription() const { return description_.has_value(); }
void SEDBase::unsetDescription() { description_.reset(); }

const std::string& SEDBase::getNotes() const { return notes_.has_value() ? *notes_ : kEmptyString; }
void SEDBase::setNotes(const std::string& notes) { notes_ = notes; }
bool SEDBase::isSetNotes() const { return notes_.has_value(); }
void SEDBase::unsetNotes() { notes_.reset(); }

const std::vector<Annotation>& SEDBase::getAnnotations() const {
    return annotations_.has_value() ? *annotations_ : kEmptyAnnotations;
}

void SEDBase::addAnnotation(const Annotation& annotation) {
    if (!annotations_.has_value()) annotations_ = std::vector<Annotation>();
    annotations_->push_back(annotation);
}

void SEDBase::insertAnnotation(std::size_t index, const Annotation& annotation) {
    if (!annotations_.has_value()) annotations_ = std::vector<Annotation>();
    if (index > annotations_->size()) index = annotations_->size();
    annotations_->insert(annotations_->begin() + static_cast<std::ptrdiff_t>(index), annotation);
}

bool SEDBase::removeAnnotationAt(std::size_t index) {
    if (!annotations_.has_value() || index >= annotations_->size()) return false;
    annotations_->erase(annotations_->begin() + static_cast<std::ptrdiff_t>(index));
    return true;
}

std::size_t SEDBase::getNumAnnotations() const {
    return annotations_.has_value() ? annotations_->size() : 0;
}

bool SEDBase::isSetAnnotations() const { return annotations_.has_value() && !annotations_->empty(); }
void SEDBase::unsetAnnotations() { annotations_.reset(); }

void SEDBase::fromJSON(const Json& json) {
    unrecognizedFields_ = Json::object();
    for (auto it = json.begin(); it != json.end(); ++it) {
        if (!isSedBaseAttribute(it.key())) unrecognizedFields_[it.key()] = it.value();
    }

    if (json.contains("id")) setId(json.at("id").get<std::string>());
    if (json.contains("name")) setName(json.at("name").get<std::string>());
    if (json.contains("description")) setDescription(json.at("description").get<std::string>());
    if (json.contains("notes")) setNotes(json.at("notes").get<std::string>());
    if (json.contains("annotations")) {
        for (const auto& entry : json.at("annotations")) {
            Annotation annotation;
            if (entry.contains("qualifier")) annotation.qualifier = entry.at("qualifier").get<std::string>();
            if (entry.contains("value")) annotation.value = entry.at("value").get<std::string>();
            addAnnotation(annotation);
        }
    }
}

Json SEDBase::toJSON() const {
    Json json = unrecognizedFields_;
    json["_type"] = getTypeName();
    if (isSetId()) json["id"] = getId();
    if (isSetName()) json["name"] = getName();
    if (isSetDescription()) json["description"] = getDescription();
    if (isSetNotes()) json["notes"] = getNotes();
    if (isSetAnnotations()) {
        Json annotations = Json::array();
        for (const auto& annotation : getAnnotations()) {
            Json entry = Json::object();
            entry["qualifier"] = annotation.qualifier;
            entry["value"] = annotation.value;
            annotations.push_back(entry);
        }
        json["annotations"] = annotations;
    }
    return json;
}

void SEDBase::validate(std::vector<ValidationError>& errors) const {
    (void)errors;  // SEDBase itself has no required attributes to check.
}

std::vector<std::string> SEDBase::getDeclaredDotAccessors() const { return {}; }

bool SEDBase::isBareReferenceValid() const { return true; }

void SEDBase::setParent(SEDBase* parent) { parent_ = parent; }
SEDBase* SEDBase::getParent() const { return parent_; }

SEDDocument* SEDBase::getSEDDocument() const {
    return parent_ ? parent_->getSEDDocument() : nullptr;
}

}  // namespace sed2
