---
id: AbstractODESimulation-0027
rule: When the value of useStiffSolver of an AbstractODESimulation is provided directly, it must be a boolean.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean."
severity: error
status: active
---

`useStiffSolver` is `BooleanOrRef`: the value, when not a reference, must be a boolean.
