---
id: Repeat-0009
rule: "The input of every entry in a Repeat's aggregateOutputVariables must reference one of that Repeat's own subTasks, or an output of one."
message: "Entry '{attr}' of the aggregateOutputVariables of {class} '{id}' has input '{value}', which is not one of its own subTasks."
severity: error
status: active
---

Same as Repeat-0008, for the AggregationCalculation entries that define
[id].aggregates.
