---
id: AbstractStochasticSimulation-0009
rule: When the value of maximumTimeStep of an AbstractStochasticSimulation is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
---

`maximumTimeStep` is `NumberOrRef`: the value, when not a reference, must be a number.
