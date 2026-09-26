---
id: Surface-0011
rule: When the value of order of a Surface is provided directly, it must be a non-negative integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a non-negative integer."
severity: error
status: active
check: schema
---

`order` is `NonNegativeIntegerOrRef`: the value, when not a reference, must be a non-negative integer.
