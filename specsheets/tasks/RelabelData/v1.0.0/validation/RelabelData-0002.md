---
id: RelabelData-0002
rule: The input attribute of a RelabelData, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
check: schema
---

`input` is `SIdRef` - always a reference, never a literal value.
