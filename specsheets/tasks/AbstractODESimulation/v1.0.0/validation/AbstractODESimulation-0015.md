---
id: AbstractODESimulation-0015
rule: When the value of maxInternalSteps of an AbstractODESimulation is provided directly, it must be an integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an integer."
severity: error
status: active
---

`maxInternalSteps` is `IntegerOrRef`: the value, when not a reference, must be an integer.
