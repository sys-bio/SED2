---
id: DrawFromDistribution-0004
rule: When the value of outputPersistent of a DrawFromDistribution is provided directly, it must be a boolean.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean."
severity: error
status: active
---

`outputPersistent` is `BooleanOrRef`: the value, when not a reference, must be a boolean.
