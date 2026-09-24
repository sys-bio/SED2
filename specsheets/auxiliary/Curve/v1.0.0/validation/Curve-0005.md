---
id: Curve-0005
rule: The x attribute of a Curve, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`x` is `SIdRef` - always a reference, never a literal value.
