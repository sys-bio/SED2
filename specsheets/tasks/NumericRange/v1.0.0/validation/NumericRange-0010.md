---
id: NumericRange-0010
rule: When the value of scale of a NumericRange is a reference, it must be a reference to a valid ScaleType value.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a valid ScaleType value."
severity: error
status: active
check: ref-type
---

`scale` is `ScaleTypeOrRef`: when the value is a reference, it must resolve to a valid ScaleType value.
