---
id: SEDBase-0006
rule: "Every colon-delimited segment of a reference must resolve to an existing element."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' does not resolve: no element exists at '{subvalue}'."
severity: error
status: active
check: handwritten
---

Walks the containment tree one colon segment at a time: #tasks:loop1 must name
a key of SEDDocument.tasks; #tasks:loop1:subTasks:sim1 must name a key of
that Repeat's subTasks; #tasks:loop1:loopVariables:x must name a key of that
Loop's loopVariables. Only ID-keyed children can be walked this way; a
segment naming a plain attribute (e.g. #tasks:sim1:model) does not resolve.
This is the check behind getSEDReference() returning null.

{subvalue} is the longest prefix that failed to resolve, e.g.
'#tasks:loop1:subTasks:sim9' when loop1 exists but has no sim9 subTask.
(Uses {subvalue} rather than {location} - which is reserved everywhere else
for the JSON-pointer location of the offending attribute itself, filled in
automatically by make_problem() - to avoid a placeholder collision: this
rule needs a second, independent piece of text in its message, the failed
reference-path prefix, which is exactly what {subvalue} already means for
the other reference rules below (SEDBase-0008 through -0011).)
