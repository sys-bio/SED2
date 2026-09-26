---
id: SEDDocument-0014
rule: "An unregistered namespace's <prefix>@version attribute must match the format v#.#.# (major.minor.patch)."
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required format 'v#.#.#'."
severity: error
status: active
check: schema
---

For a registered namespace this is already enforced as a generated schema
pattern (see Design.md's Namespaces section) - the same mechanism as
SEDDocument's own version attribute. An unregistered namespace has no such
generated property, so nothing in the schema constrains its <prefix>@version
attribute's shape; this rule closes that gap by hand, so every
<prefix>@version in the document matches v#.#.# whether or not its
namespace is registered.
