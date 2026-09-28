---
id: TypesWidget-0004
rule: The items attribute of a TypesWidget, if present, must be an array or a reference.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array or a reference."
severity: error
status: active
check: schema
---

`items` is optional (ArrayOrRef); when present it must be a JSON array (elements unconstrained) or an SIdRef string.
