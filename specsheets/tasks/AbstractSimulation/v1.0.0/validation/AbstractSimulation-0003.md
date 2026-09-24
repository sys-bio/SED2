---
id: AbstractSimulation-0003
rule: When the value of independentVariable of an AbstractSimulation is a reference, it must be a reference to a string.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a string."
severity: error
status: active
---

`independentVariable` is `StringOrRef` in AbstractSimulation: when the value is a reference, it must resolve to a string.
