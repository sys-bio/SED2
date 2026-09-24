---
id: Curve-0011
rule: When the value of yAxis of a Curve is provided directly, it must be one of 'right' or 'left'.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not one of 'right' or 'left'."
severity: error
status: active
---

`yAxis` is `one of "right", "left" or SIdRef`: the value, when not a reference, must be one of 'right' or 'left'.
