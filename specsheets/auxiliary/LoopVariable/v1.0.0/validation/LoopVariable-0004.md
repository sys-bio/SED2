---
id: LoopVariable-0004
rule: "The subsequentValues of a LoopVariable must reference one of its enclosing Loop's own subTasks, or an output of one."
message: "LoopVariable '{id}' has subsequentValues '{value}', which is not one of its Loop's own subTasks."
severity: error
status: active
---

subsequentValues is the value this loop variable takes on after each
iteration, produced by one of the loop's own subTasks. This is the one place
a reference may point forward in file order (the subTasks are defined after
loopVariables), which AbstractTask-0003 must allow.
