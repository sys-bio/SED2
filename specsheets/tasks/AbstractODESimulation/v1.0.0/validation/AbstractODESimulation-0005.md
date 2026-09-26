---
id: AbstractODESimulation-0005
rule: When the value of absoluteToleranceVector of an AbstractODESimulation is provided directly, it must be an array of numbers.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of numbers."
severity: error
status: active
check: schema
---

`absoluteToleranceVector` is `ListOfNumbersOrRef`: the value, when not a reference, must be an array of numbers.
