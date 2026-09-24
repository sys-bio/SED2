---
id: AbstractODESimulation-0006
rule: When the value of absoluteToleranceVector of an AbstractODESimulation is a reference, it must be a reference to an array of numbers.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of numbers."
severity: error
status: active
---

`absoluteToleranceVector` is `ListOfNumbersOrRef`: when the value is a reference, it must resolve to an array of numbers.
