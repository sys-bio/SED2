---
id: AbstractStochasticSimulation-0011
rule: When the value of nonNegative of an AbstractStochasticSimulation is provided directly, it must be a boolean.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean."
severity: error
status: active
check: schema
---

`nonNegative` is `BooleanOrRef`: the value, when not a reference, must be a boolean.
