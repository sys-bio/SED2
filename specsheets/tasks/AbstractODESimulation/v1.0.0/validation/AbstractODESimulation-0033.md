---
id: AbstractODESimulation-0033
rule: When the value of variableStepSize of an AbstractODESimulation is provided directly, it must be a boolean.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean."
severity: error
status: active
---

`variableStepSize` is `BooleanOrRef`: the value, when not a reference, must be a boolean.
