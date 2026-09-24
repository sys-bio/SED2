---
id: ParameterRange-0015
rule: When the value of values of a ParameterRange is a reference, it must be a reference to an array of NumberOrRef objects.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of NumberOrRef objects."
severity: error
status: active
---

`values` is `array of NumberOrRef or SIdRef`: when the value is a reference, it must resolve to an array of NumberOrRef objects.
