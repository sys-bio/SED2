---
id: Curve-0006
rule: The xErrorUpper attribute of a Curve, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`xErrorUpper` is `SIdRef` - always a reference, never a literal value.
