---
id: SEDBase-0016
rule: "A reference required to resolve to a model must resolve to a model."
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to {resolved-value}, not a model."
severity: error
status: active
check: handwritten
---

Applies to every field whose schema property carries `"x-ref-target": "model"`
(the `model` attribute of the simulation, FluxBalanceAnalysis, Jacobian,
SteadyState, ParameterScan and ModelElementList classes, and ModelChange's
`inputModel`). A model is a type, like a number or a boolean: a reference
resolves to one only when it names a task output whose outputs.json entry has
"type": "model" (for example #tasks:model1.model). A constant is never a model,
and neither is a task's data output (#tasks:sim1).

A reference that does not resolve at all (SEDBase-0006), targets an output
(SEDBase-0007), or uses an accessor its target does not declare (SEDBase-0008)
fires those rules instead of this one. {resolved-value} describes what the
reference did resolve to, such as "a number", "an array", "an object", or
"a annotatedData value".
