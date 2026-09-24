---
id: ParameterRange-0011
rule: When the value of numberOfSteps of a ParameterRange is a reference, it must be a reference to a positive integer.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a positive integer."
severity: error
status: active
---

`numberOfSteps` is `PositiveIntegerOrRef`: when the value is a reference, it must resolve to a positive integer.
