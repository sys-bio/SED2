---
id: ParameterRange-0002
rule: When the value of modelElement of a ParameterRange is provided directly, it must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
---

`modelElement` is `StringOrRef`: the value, when not a reference, must be a string.
