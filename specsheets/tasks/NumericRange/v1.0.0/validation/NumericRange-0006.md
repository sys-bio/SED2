---
id: NumericRange-0006
rule: When the value of interval of a NumericRange is a reference, it must be a reference to a positive number (> 0).
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a positive number (> 0)."
severity: error
status: active
check: ref-type
---

`interval` is `PositiveDoubleOrRef`: when the value is a reference, it must resolve to a positive number (> 0).
