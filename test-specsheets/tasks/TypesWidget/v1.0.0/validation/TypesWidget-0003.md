---
id: TypesWidget-0003
rule: The count attribute of a TypesWidget, if present, must be an integer or a reference.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an integer or a reference."
severity: error
status: active
check: schema
---

`count` is optional (IntegerOrRef); when present it must be an integer or an SIdRef string.
