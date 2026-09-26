---
id: Calculation-0002
rule: When the value of math of a Calculation is provided directly, it must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`math` is `StringOrRef`: the value, when not a reference, must be a string.
