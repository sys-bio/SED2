---
id: AbstractTask-0003
rule: "A task may only reference constants, tasks that appear earlier in the same tasks dictionary, or (for a subTask) the elements listed in this rule's explanation."
message: "{class} '{id}' references '{value}', which is not defined before it; tasks may only depend on earlier tasks."
severity: error
status: active
---

The chronological rule (core-spec.md Section 3), made checkable. For a task
at the top level of SEDDocument.tasks, a reference may target:
- any constant;
- any task that appears earlier in SEDDocument.tasks.

For a subTask of a Repeat R, a reference may additionally target:
- any earlier sibling subTask of R;
- anything that R itself was allowed to reference;
- R itself, or any Repeat enclosing R, but only through .range/.index
  or a loopVariables child (see SEDBase-0013).

A task never references itself. Since everything must be earlier, cycles are
impossible, and the document is always a DAG executable in file order.
