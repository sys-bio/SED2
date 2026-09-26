---
id: FluxBalanceAnalysis-0007
rule: When the value of outputModel of a FluxBalanceAnalysis is a reference, it must be a reference to a boolean.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a boolean."
severity: error
status: active
check: ref-type
---

`outputModel` is `BooleanOrRef`: when the value is a reference, it must resolve to a boolean.
