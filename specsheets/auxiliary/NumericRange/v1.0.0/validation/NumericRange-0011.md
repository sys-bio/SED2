---
id: NumericRange-0011
rule: When the value of values of a NumericRange is provided directly, it must be an array of NumberOrRef objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of NumberOrRef objects."
severity: error
status: active
---

`values` is `array of NumberOrRef or SIdRef`: the value, when not a reference, must be an array of NumberOrRef objects.
