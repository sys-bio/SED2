---
id: AbstractStochasticSimulation-0013
rule: When the value of maxOutputRows of an AbstractStochasticSimulation is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
check: schema
---

`maxOutputRows` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.
