---
id: Surface-0010
rule: The style attribute of a Surface, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`style` is `SIdRef` - always a reference, never a literal value.
