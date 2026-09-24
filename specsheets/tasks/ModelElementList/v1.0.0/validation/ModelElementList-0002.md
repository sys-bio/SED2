---
id: ModelElementList-0002
rule: The model attribute of a ModelElementList, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`model` is `SIdRef` - always a reference, never a literal value.
