---
id: ParameterRange-0010
rule: When the value of numberOfSteps of a ParameterRange is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
---

`numberOfSteps` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.
