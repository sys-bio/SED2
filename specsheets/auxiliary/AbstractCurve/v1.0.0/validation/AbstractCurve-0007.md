---
id: AbstractCurve-0007
rule: When the value of yAxis of an AbstractCurve is a reference, it must be a reference to one of 'right' or 'left'.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not one of 'right' or 'left'."
severity: error
status: active
check: ref-type
---

`yAxis` is `one of "right", "left" or SIdRef` in AbstractCurveCommon: when the value is a reference, it must resolve to one of 'right' or 'left'.
