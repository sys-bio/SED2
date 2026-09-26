---
id: AbstractCurve-0006
rule: When the value of yAxis of an AbstractCurve is provided directly, it must be one of 'right' or 'left'.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not one of 'right' or 'left'."
severity: error
status: active
check: schema
---

`yAxis` is `one of "right", "left" or SIdRef` in AbstractCurveCommon: the value, when not a reference, must be one of 'right' or 'left'.
