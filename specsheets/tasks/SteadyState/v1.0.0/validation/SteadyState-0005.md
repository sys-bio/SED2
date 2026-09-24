---
id: SteadyState-0005
rule: When the value of outputModel of a SteadyState is provided directly, it must be a boolean.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean."
severity: error
status: active
---

`outputModel` is `BooleanOrRef`: the value, when not a reference, must be a boolean.
