---
id: LoopVariable-0003
rule: The subsequentValues attribute of a LoopVariable, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
check: schema
---

`subsequentValues` is `SIdRef` - always a reference, never a literal value.
