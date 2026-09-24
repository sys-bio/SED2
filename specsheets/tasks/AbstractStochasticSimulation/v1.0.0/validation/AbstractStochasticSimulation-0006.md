---
id: AbstractStochasticSimulation-0006
rule: When the value of variableStepSize of an AbstractStochasticSimulation is a reference, it must be a reference to a boolean.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a boolean."
severity: error
status: active
---

`variableStepSize` is `BooleanOrRef`: when the value is a reference, it must resolve to a boolean.
