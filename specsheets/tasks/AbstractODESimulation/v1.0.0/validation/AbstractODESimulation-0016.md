---
id: AbstractODESimulation-0016
rule: When the value of maxInternalSteps of an AbstractODESimulation is a reference, it must be a reference to an integer.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an integer."
severity: error
status: active
---

`maxInternalSteps` is `IntegerOrRef`: when the value is a reference, it must resolve to an integer.
