---
id: Surface-0005
rule: The x attribute of a Surface, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
check: schema
---

`x` is `SIdRef` - always a reference, never a literal value.
