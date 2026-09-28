// Generated direct-only-class registry (see this file's own generator,
// generator/emit_cpp.py's emit_direct_only_hpp, for what this is and why
// it exists). GENERATED - do not hand-edit; regenerate via
// generator/generate.py.
#pragma once

#include "GeneratedModel.hpp"

#include <functional>
#include <map>
#include <memory>
#include <string>

namespace sed2test {

inline const std::map<std::string, std::function<std::unique_ptr<SedBase>()>>& direct_only_classes() {
    static const std::map<std::string, std::function<std::unique_ptr<SedBase>()>> m = {
        {"FancyWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<FancyWidget>()); }},
        {"MathWidget-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<MathWidget>()); }},
        {"SimpleWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<SimpleWidget>()); }},
        {"TypesWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<TypesWidget>()); }},
        {"SimpleReport-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<SimpleReport>()); }},
        {"Choice-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<Choice>()); }},
        {"WeightedChoice-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<WeightedChoice>()); }},
        {"acme-AcmeWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<AcmeWidget>()); }},
    };
    return m;
}

}  // namespace sed2test
