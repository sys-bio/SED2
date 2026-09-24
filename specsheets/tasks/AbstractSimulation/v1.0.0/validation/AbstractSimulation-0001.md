---
id: AbstractSimulation-0001
rule: The model attribute of an AbstractSimulation, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
---

`model` is defined as `SIdRef` in AbstractSimulation - always a reference, never a literal value.
