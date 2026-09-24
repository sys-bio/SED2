---
id: ParameterRange-0004
rule: When the value of start of a ParameterRange is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
---

`start` is `NumberOrRef`: the value, when not a reference, must be a number.
