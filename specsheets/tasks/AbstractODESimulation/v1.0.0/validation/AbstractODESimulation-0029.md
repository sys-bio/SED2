---
id: AbstractODESimulation-0029
rule: When the value of maxBDForder of an AbstractODESimulation is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
---

`maxBDForder` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.
