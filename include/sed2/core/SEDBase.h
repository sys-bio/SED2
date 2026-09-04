#pragma once

#include <cstddef>
#include <optional>
#include <string>
#include <vector>

#include "sed2/core/Json.h"
#include "sed2/validation/ValidationError.h"

namespace sed2 {

class SEDDocument;

// A single 'annotations' entry: {"qualifier": "...", "value": "..."}.
struct Annotation {
    std::string qualifier;
    std::string value;
};

// Base class for every SED2 object (the spec's own "SEDBase"). Holds the
// attributes common to all SED2 elements - id, name, description, notes,
// annotations - plus any JSON fields this version of the library doesn't
// recognize, so round-tripping a document never silently drops data as the
// format expands (Design.md: "Its dynamic tree also lets each SED2 class
// keep any unrecognized fields around unchanged").
class SEDBase {
public:
    virtual ~SEDBase() = default;

    const std::string& getId() const;
    void setId(const std::string& id);
    bool isSetId() const;
    void unsetId();

    const std::string& getName() const;
    void setName(const std::string& name);
    bool isSetName() const;
    void unsetName();

    const std::string& getDescription() const;
    void setDescription(const std::string& description);
    bool isSetDescription() const;
    void unsetDescription();

    const std::string& getNotes() const;
    void setNotes(const std::string& notes);
    bool isSetNotes() const;
    void unsetNotes();

    const std::vector<Annotation>& getAnnotations() const;
    void addAnnotation(const Annotation& annotation);
    void insertAnnotation(std::size_t index, const Annotation& annotation);
    bool removeAnnotationAt(std::size_t index);
    std::size_t getNumAnnotations() const;
    bool isSetAnnotations() const;
    void unsetAnnotations();

    // The '_type' discriminator this class writes/expects, e.g.
    // "explicitODESimulation". Every generated class overrides this;
    // RawElement (the forward-compatibility fallback) returns whatever
    // '_type' it was loaded with.
    virtual std::string getTypeName() const = 0;

    // Reads the SEDBase-level attributes from 'json', stashing anything it
    // doesn't recognize. Subclasses override, call SEDBase::fromJSON(json)
    // first, then read their own attributes.
    virtual void fromJSON(const Json& json);

    // Writes the SEDBase-level attributes plus the preserved unrecognized
    // fields. Subclasses override, call SEDBase::toJSON() first, then add
    // their own attributes to the returned object.
    virtual Json toJSON() const;

    // Appends one ValidationError per problem found in this object,
    // recursing into any owned children. Does not consult the JSON Schema
    // (see SchemaValidator for that pass) - only checks that this version
    // of the library was actually able to represent required attributes.
    virtual void validate(std::vector<ValidationError>& errors) const;

    // Names of this class's attributes that are valid dot-accessors in a
    // reference (e.g. ModelImport declares "model", for references like
    // "#tasks:task1.model"). Paired with AttributeTypes::hasSubvalue to
    // check a reference's trailing dot accessor for plausibility. Defaults
    // to none; each generated class's attribute table sets this via its
    // "dotAccessors" field where the UML spec declares one (see
    // spec/numbered-validation-rules.md, V0002).
    virtual std::vector<std::string> getDeclaredDotAccessors() const;

    // True if referencing this class with no trailing dot/bracket accessor
    // (e.g. "#tasks:task1") is itself meaningful. False for classes whose
    // only meaningful output is reached through one of their declared dot
    // accessors (e.g. ModelImport - only "#tasks:task1.model" means
    // anything, not "#tasks:task1" itself). Defaults to true; a generated
    // class's attribute table sets this via its "bareReferenceValid" field
    // where the spec says otherwise.
    virtual bool isBareReferenceValid() const;

    // Non-owning: 'parent' is whichever object's setter/add/insert method
    // just took ownership of this one (see codegen's owned/polymorphicList
    // definitions()), or nullptr for an object nobody has attached to
    // anything yet (e.g. one just default-constructed by test code). Not
    // meant to be called directly outside codegen-generated setters.
    void setParent(SEDBase* parent);
    SEDBase* getParent() const;

    // Walks the parent chain up to the owning SEDDocument, the way a
    // libSBML object walks to its SBMLDocument, stopping at nullptr if
    // this object (or one of its ancestors) was never attached to a
    // document - see AttributeTypes::validateReference, which is the
    // reason this exists: a reference can only be resolved for real once
    // there's a document to resolve it against. sed2::SEDDocument
    // overrides this to return itself.
    virtual SEDDocument* getSEDDocument() const;

protected:
    // Fields present in the source JSON that this class does not model.
    // Preserved verbatim by toJSON().
    Json unrecognizedFields_ = Json::object();

private:
    std::optional<std::string> id_;
    std::optional<std::string> name_;
    std::optional<std::string> description_;
    std::optional<std::string> notes_;
    std::optional<std::vector<Annotation>> annotations_;
    SEDBase* parent_ = nullptr;
};

}  // namespace sed2
