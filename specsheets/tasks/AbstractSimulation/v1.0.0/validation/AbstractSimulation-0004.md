---
id: AbstractSimulation-0004
rule: When the value of independentVariableInit of an AbstractSimulation is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
---

`independentVariableInit` is `NumberOrRef` in AbstractSimulation: the value, when not a reference, must be a number.
