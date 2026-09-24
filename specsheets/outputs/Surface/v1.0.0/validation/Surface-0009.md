---
id: Surface-0009
rule: The z attribute of a Surface, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`z` is `SIdRef` - always a reference, never a literal value.
