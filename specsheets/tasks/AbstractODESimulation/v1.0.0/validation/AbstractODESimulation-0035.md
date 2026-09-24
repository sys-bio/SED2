---
id: AbstractODESimulation-0035
rule: When the value of maxOutputRows of an AbstractODESimulation is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
---

`maxOutputRows` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.
