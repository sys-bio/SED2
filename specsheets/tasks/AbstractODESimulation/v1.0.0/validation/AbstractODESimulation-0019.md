---
id: AbstractODESimulation-0019
rule: When the value of minInternalStepSize of an AbstractODESimulation is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
check: schema
---

`minInternalStepSize` is `NumberOrRef`: the value, when not a reference, must be a number.
