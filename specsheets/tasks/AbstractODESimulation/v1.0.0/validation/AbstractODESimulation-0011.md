---
id: AbstractODESimulation-0011
rule: When the value of initialStepSize of an AbstractODESimulation is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
---

`initialStepSize` is `NumberOrRef`: the value, when not a reference, must be a number.
