---
id: AbstractODESimulation-0020
rule: When the value of minInternalStepSize of an AbstractODESimulation is a reference, it must be a reference to a number.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a number."
severity: error
status: active
check: ref-type
---

`minInternalStepSize` is `NumberOrRef`: when the value is a reference, it must resolve to a number.
