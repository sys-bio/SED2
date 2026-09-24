---
id: ParameterRange-0012
rule: When the value of scale of a ParameterRange is provided directly, it must be one of 'linear', 'log10'.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not one of {allowed}."
severity: error
status: active
---

`ScaleType` is defined in `core/Types` with the allowed values 'linear', 'log10' (see `core/Types/v1.0.0/schema.json`).
