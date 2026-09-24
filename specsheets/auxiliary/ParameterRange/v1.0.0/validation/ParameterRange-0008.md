---
id: ParameterRange-0008
rule: When the value of interval of a ParameterRange is provided directly, it must be a positive number (> 0).
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive number (> 0)."
severity: error
status: active
---

`interval` is `PositiveDoubleOrRef`: the value, when not a reference, must be a positive number (> 0).
