---
id: Range-0001
rule: When the value of values of a Range is provided directly, it must be an array of AnyValueOrRef objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of AnyValueOrRef objects."
severity: error
status: active
---

`values` is `array of AnyValueOrRef or SIdRef`: the value, when not a reference, must be an array of AnyValueOrRef objects.
