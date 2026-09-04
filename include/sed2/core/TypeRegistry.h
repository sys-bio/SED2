#pragma once

#include <functional>
#include <memory>
#include <string>
#include <unordered_map>

#include "sed2/core/Json.h"

namespace sed2 {

class SEDBase;

using SEDFactory = std::function<std::unique_ptr<SEDBase>(const Json&)>;

// Maps a '_type' string to the factory that constructs and populates that
// class from JSON. Populated by registerGeneratedTypes() (defined in the
// generated Registrations.cpp) the first time instance() runs, so adding a
// class under codegen/spec_attributes never requires touching this registry
// by hand.
class TypeRegistry {
public:
    static TypeRegistry& instance();

    void registerType(const std::string& typeName, SEDFactory factory);
    bool isRegistered(const std::string& typeName) const;

    // Constructs and populates the class registered for 'typeName', or
    // nullptr if 'typeName' isn't registered.
    std::unique_ptr<SEDBase> create(const std::string& typeName, const Json& json) const;

private:
    std::unordered_map<std::string, SEDFactory> factories_;
};

// Registers every generated, registerType:true class into 'registry'.
// Defined in the generated Registrations.cpp, which calls one named
// per-class function for each attribute table - this gives the linker a
// real symbol reference into each generated class's translation unit, so
// none of them can be silently dropped from a static-library link (unlike
// anonymous-namespace static-initializer self-registration, which a linker
// is free to discard if nothing else in the link references that object
// file).
void registerGeneratedTypes(TypeRegistry& registry);

// Builds one child object from 'json': looks up json["_type"] in the
// TypeRegistry and delegates to its factory, or falls back to RawElement
// (preserving the JSON verbatim) if '_type' is missing or unregistered.
std::unique_ptr<SEDBase> loadPolymorphicChild(const Json& json);

}  // namespace sed2
