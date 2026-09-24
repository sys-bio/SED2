---
id: Curve-0017
rule: The yTo attribute of a Curve, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`yTo` is `SIdRef` - always a reference, never a literal value.
