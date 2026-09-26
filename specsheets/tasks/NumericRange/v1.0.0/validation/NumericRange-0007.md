---
id: NumericRange-0007
rule: When the value of numberOfSteps of a NumericRange is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
check: schema
---

`numberOfSteps` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.
