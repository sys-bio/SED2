---
id: AbstractSimulation-0002
rule: When the value of independentVariable of an AbstractSimulation is provided directly, it must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`independentVariable` is `StringOrRef` in AbstractSimulation: the value, when not a reference, must be a string.
