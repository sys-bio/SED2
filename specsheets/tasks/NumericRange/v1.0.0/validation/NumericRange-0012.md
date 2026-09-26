---
id: NumericRange-0012
rule: When the value of values of a NumericRange is a reference, it must be a reference to an array of NumberOrRef objects.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of NumberOrRef objects."
severity: error
status: active
check: ref-type
---

`values` is `array of NumberOrRef or SIdRef`: when the value is a reference, it must resolve to an array of NumberOrRef objects.
