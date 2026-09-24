---
id: AbstractStochasticSimulation-0015
rule: When the value of maxNumSteps of an AbstractStochasticSimulation is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
---

`maxNumSteps` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.
