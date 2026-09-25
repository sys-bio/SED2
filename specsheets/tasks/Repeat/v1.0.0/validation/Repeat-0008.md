---
id: Repeat-0008
rule: "Every value in a Repeat's outputVariableMap must reference one of that Repeat's own subTasks, or an output of one."
message: "Entry '{attr}' of the outputVariableMap of {class} '{id}' references '{value}', which is not one of its own subTasks."
severity: error
status: active
---

outputVariableMap defines the columns of the Repeat's [id] output, each
collected from a subTask per iteration. The reference may carry accessors and
indices into the subTask's output (e.g. '#tasks:loop1:subTasks:sim1['S1']'),
checked as usual by SEDBase-0008 through SEDBase-0011.
