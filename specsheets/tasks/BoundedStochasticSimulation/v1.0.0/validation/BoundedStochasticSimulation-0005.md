---
id: BoundedStochasticSimulation-0005
rule: The independentVariableSpan attribute of a BoundedStochasticSimulation must be a SpanInline object.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a SpanInline object."
severity: error
status: active
check: schema
---

`independentVariableSpan` is `SpanInline`: it must be a SpanInline object.
