#pragma once

#include <string>
#include <vector>

namespace sed2 {

// Named constants and functions predefined for SED2 math expressions:
// MathML's standard set (as used by libsbml), the SBML 'distrib' package's
// distribution functions, and any SED2-spec-only additions (Design.md,
// "Predefined Functions"). This table is a starting seed, not a claim of
// completeness - like spec/numbered-validation-rules.md, it grows as more
// functions are found in the spec.
struct FunctionSignature {
    std::string name;
    int minArgs = 0;
    int maxArgs = 0;  // -1 means unbounded
};

const std::vector<std::string>& predefinedConstants();
const std::vector<FunctionSignature>& predefinedFunctions();

bool isPredefinedConstant(const std::string& name);
bool isPredefinedFunction(const std::string& name);

}  // namespace sed2
