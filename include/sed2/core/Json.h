#pragma once

#include <nlohmann/json.hpp>

namespace sed2 {

// The concrete JSON type used throughout sed2. SED2 documents are
// order-sensitive (attribute order in a document, entry order in
// dictionaries such as 'tasks' or 'constants'), so the library standardizes
// on nlohmann::ordered_json rather than the alphabetizing default
// nlohmann::json, everywhere a document is read, held, or written.
using Json = nlohmann::ordered_json;

}  // namespace sed2
