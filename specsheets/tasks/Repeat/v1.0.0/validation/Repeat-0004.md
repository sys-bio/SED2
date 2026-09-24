---
id: Repeat-0004
rule: The aggregateOutputVariables attribute of a Repeat must be an object whose values are AggregationCalculation.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AggregationCalculation."
severity: error
status: active
---

`aggregateOutputVariables` is `object (values: AggregationCalculation)` in Repeat: it must be an object whose values are AggregationCalculation.
