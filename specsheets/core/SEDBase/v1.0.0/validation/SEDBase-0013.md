---
id: SEDBase-0013
rule: "A reference to a Repeat's subTasks, its .range/.index outputs, or one of its loop variables is only legal when the element holding the reference is that Repeat itself, or lies within that Repeat's own subTasks (at any depth, including through a nested Repeat)."
message: "{class} '{id}' references '{value}', which lies inside Repeat '{resolved-value}'; only that Repeat's own subTasks may reference into it."
severity: error
status: active
---

Consolidates three rules that were drafted separately (AbstractTask-0004,
Repeat-0007, Loop-0006) into one, moved to SEDBase rather than AbstractTask
so the same restriction reaches Plots and Reports too, not just other tasks.
A subTask runs once per iteration, and a Repeat's .range/.index and loop
variables only have a value during one, so a reference from outside that
Repeat's own subTasks has no single well-defined value.

This never blocks a Repeat's own outputVariableMap (Repeat-0008),
aggregateOutputVariables (Repeat-0009), or a loopVariable's subsequentValues
(LoopVariable-0004): those are fields declared directly on the Repeat/Loop
itself, not an outside reference reaching in. Nor does it block an ordinary
reference to the Repeat's own output - #tasks:loop1 or #tasks:loop1.aggregates
- from anywhere; that targets the Repeat itself and is governed by
SEDBase-0008 like any other task reference. The only way a subTask's
per-iteration result leaves its Repeat is through one of those two exports.
