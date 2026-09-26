---
id: Repeat-0010
rule: "An entry in a Repeat's aggregateOutputVariables must not define appliedDimensions."
message: "Entry '{attr}' of the aggregateOutputVariables of {class} '{id}' defines appliedDimensions; the applied dimension is always the Repeat's own iterations."
severity: error
status: active
check: handwritten
---

Stated in Repeat's description.md. Could instead be expressed in the schema
(a dedicated AggregationCalculation variant without appliedDimensions) and
get an x-rule-id; left as a hand-written rule here since the schema currently
reuses AggregationCalculation as-is.
