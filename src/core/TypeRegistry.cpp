#include "sed2/core/TypeRegistry.h"

#include "sed2/core/RawElement.h"
#include "sed2/core/SEDBase.h"

namespace sed2 {

TypeRegistry& TypeRegistry::instance() {
    static TypeRegistry registry;
    // Runs once, after 'registry' itself is fully constructed: separating
    // this from the declaration above avoids a generated registration
    // function recursively calling instance() while it's still being
    // initialized. Passing 'registry' directly (rather than each
    // registration function calling instance() itself) is what forces the
    // linker to pull in every generated class's object file - see the
    // registerGeneratedTypes() comment in TypeRegistry.h.
    static bool initialized = (registerGeneratedTypes(registry), true);
    (void)initialized;
    return registry;
}

void TypeRegistry::registerType(const std::string& typeName, SEDFactory factory) {
    factories_[typeName] = std::move(factory);
}

bool TypeRegistry::isRegistered(const std::string& typeName) const {
    return factories_.find(typeName) != factories_.end();
}

std::unique_ptr<SEDBase> TypeRegistry::create(const std::string& typeName, const Json& json) const {
    auto it = factories_.find(typeName);
    if (it == factories_.end()) return nullptr;
    return it->second(json);
}

std::unique_ptr<SEDBase> loadPolymorphicChild(const Json& json) {
    std::string typeName;
    if (json.contains("_type")) typeName = json.at("_type").get<std::string>();

    if (!typeName.empty()) {
        auto object = TypeRegistry::instance().create(typeName, json);
        if (object) return object;
    }

    auto fallback = std::make_unique<RawElement>();
    fallback->fromJSON(json);
    return fallback;
}

}  // namespace sed2
