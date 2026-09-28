---
id: TypesWidget-0001
rule: The enabled attribute of a TypesWidget, if present, must be a boolean or a reference.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean or a reference."
severity: error
status: active
check: schema
---

`enabled` is optional (BooleanOrRef); when present it must be `true`/`false` or an SIdRef string.
