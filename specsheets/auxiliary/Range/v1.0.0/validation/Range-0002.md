---
id: Range-0002
rule: When the value of values of a Range is a reference, it must be a reference to an array of AnyValueOrRef objects.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of AnyValueOrRef objects."
severity: error
status: active
---

`values` is `array of AnyValueOrRef or SIdRef`: when the value is a reference, it must resolve to an array of AnyValueOrRef objects.
