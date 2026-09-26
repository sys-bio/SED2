---
id: NumericRange-0003
rule: When the value of end of a NumericRange is provided directly, it must be a number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a number."
severity: error
status: active
check: schema
---

`end` is `NumberOrRef`: the value, when not a reference, must be a number.
