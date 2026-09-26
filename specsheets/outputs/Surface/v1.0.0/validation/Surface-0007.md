---
id: Surface-0007
rule: The y attribute of a Surface, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
check: schema
---

`y` is `SIdRef` - always a reference, never a literal value.
