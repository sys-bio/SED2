---
id: AbstractStochasticSimulation-0001
rule: When the value of seed of an AbstractStochasticSimulation is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
---

`seed` is `NumberOrRef`: the value, when not a reference, must be a number.
