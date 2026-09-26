---
id: AbstractCurve-0004
rule: When the value of order of an AbstractCurve is a reference, it must be a reference to a non-negative integer.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a non-negative integer."
severity: error
status: active
check: ref-type
---

`order` is `NonNegativeIntegerOrRef` in AbstractCurveCommon: when the value is a reference, it must resolve to a non-negative integer.
