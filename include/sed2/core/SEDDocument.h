#pragma once

#include <string>
#include <vector>

#include "sed2/core/AttributeTypes.h"
#include "sed2/generated/SEDDocument.h"
#include "sed2/validation/ValidationError.h"

namespace sed2 {

// The root SED2 object. Adds file/string loading and cross-reference
// resolution on top of the attribute accessors codegen produces from
// codegen/spec_attributes/SEDDocument.json (sed2::generated::SEDDocument) -
// this is the one class in the vertical slice that needs behavior a plain
// attribute table can't express, so it's a small hand-written subclass
// rather than something the generator can produce on its own.
class SEDDocument : public generated::SEDDocument {
public:
    // Reads and parses 'path'. On failure (the file can't be opened, or
    // its contents aren't valid JSON), returns an empty SEDDocument and,
    // if 'errorMessage' is non-null, explains why in it.
    static SEDDocument fromFile(const std::string& path, std::string* errorMessage = nullptr);
    static SEDDocument fromJSONString(const std::string& text, std::string* errorMessage = nullptr);

    // Writes toJSON() to 'path', pretty-printed. Returns false if the file
    // couldn't be written.
    bool toFile(const std::string& path) const;

    // Unlike every other SED2 class, the document root carries no '_type'
    // of its own in the spec (nothing ever needs to discriminate *it* by
    // type - it's the one thing a SED2 parser starts from unconditionally,
    // hence registerType:false in its attribute table too). toJSON()
    // therefore omits the '_type' SEDBase would otherwise always add;
    // getTypeName() still reports "sedDocument" for whatever code finds it
    // useful to ask a SEDBase* what it is.
    Json toJSON() const override;

    // Resolves the colon-path prefix of 'ref' (e.g. "#tasks:sim1" in
    // "#tasks:sim1.model['S1']") to the object it names. Any trailing dot
    // or bracket accessors are not resolved further - see AttributeTypes.h
    // and Design.md's "Cross-references": what they resolve to is only
    // meaningful once the experiment this document describes actually
    // executes, so only their *plausibility* can ever be checked ahead of
    // time (see AttributeTypes::hasSubvalue). Returns nullptr if 'ref'
    // isn't a reference, or its colon path doesn't resolve to anything in
    // this document.
    const SEDBase* getSEDReference(const std::string& ref) const;

    // The root of the parent chain: always itself (see SEDBase::
    // getSEDDocument, which every other class inherits unchanged).
    SEDDocument* getSEDDocument() const override;

    // Runs the JSON Schema pass (SchemaValidator, against
    // spec/sed2.schema.json) followed by the recursive per-class
    // validate() pass, collecting every problem found rather than
    // stopping at the first one (Design.md, "Validation").
    void validate(std::vector<ValidationError>& errors) const override;
};

}  // namespace sed2
