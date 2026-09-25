---
id: SEDBase-0008
rule: "A dot-accessor in a reference must be one the target declares valid."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' uses accessor '{subvalue}', which is not a valid output of its target."
severity: error
status: active
---

For a task target, the accessor must appear in that task class's outputs.json,
and its "valid" field must be true, or be an expression that evaluates to true
against the target's own fields. When the expression cannot be evaluated
statically (it depends on a reference that resolves only at run time), the
rule does not fire.

For a constants, loopVariables, or styles target, no dot-accessor is valid.

The bare [id] form (no accessor) is checked the same way, against outputs.json's
"[id]" entry: referencing a ModelImport as '#tasks:m1' with no .model fires this
rule, with {subvalue} empty.
