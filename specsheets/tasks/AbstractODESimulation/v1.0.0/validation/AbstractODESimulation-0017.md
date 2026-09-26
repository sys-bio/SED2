---
id: AbstractODESimulation-0017
rule: When the value of maxInternalStepSize of an AbstractODESimulation is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
check: schema
---

`maxInternalStepSize` is `NumberOrRef`: the value, when not a reference, must be a number.
