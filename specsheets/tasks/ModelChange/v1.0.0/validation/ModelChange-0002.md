---
id: ModelChange-0002
rule: The inputModel attribute of a ModelChange, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`inputModel` is `SIdRef` - always a reference, never a literal value.
