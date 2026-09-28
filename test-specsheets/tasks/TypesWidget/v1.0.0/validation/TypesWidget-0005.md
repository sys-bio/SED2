---
id: TypesWidget-0005
rule: The settings attribute of a TypesWidget, if present, must be an object or a reference.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object or a reference."
severity: error
status: active
check: schema
---

`settings` is optional (DictOrRef); when present it must be a JSON object (members unconstrained) or an SIdRef string.
