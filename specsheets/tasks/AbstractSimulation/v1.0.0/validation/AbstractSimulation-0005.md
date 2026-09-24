---
id: AbstractSimulation-0005
rule: When the value of independentVariableInit of an AbstractSimulation is a reference, it must be a reference to a number.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a number."
severity: error
status: active
---

`independentVariableInit` is `NumberOrRef` in AbstractSimulation: when the value is a reference, it must resolve to a number.
