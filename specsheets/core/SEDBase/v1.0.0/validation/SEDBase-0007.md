---
id: SEDBase-0007
rule: "A reference must not target an AbstractOutput, or anything contained in one."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' targets an output; outputs may never be used as input."
severity: error
status: active
check: handwritten
---

Enforces core-spec.md Section 6: an AbstractOutput is always a final stage
and is never an input to anything else. This includes an output referencing
another output.
