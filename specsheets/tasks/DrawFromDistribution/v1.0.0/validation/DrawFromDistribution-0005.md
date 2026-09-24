---
id: DrawFromDistribution-0005
rule: When the value of outputPersistent of a DrawFromDistribution is a reference, it must be a reference to a boolean.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a boolean."
severity: error
status: active
---

`outputPersistent` is `BooleanOrRef`: when the value is a reference, it must resolve to a boolean.
