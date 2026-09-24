---
id: AbstractODESimulation-0028
rule: When the value of useStiffSolver of an AbstractODESimulation is a reference, it must be a reference to a boolean.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a boolean."
severity: error
status: active
---

`useStiffSolver` is `BooleanOrRef`: when the value is a reference, it must resolve to a boolean.
