---
id: SEDBase-0012
rule: "A bracket index into a constant must match the structure of that constant's literal value."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' indexes constant '{resolved-value}' with {subvalue}, which that value does not contain."
severity: error
status: active
check: handwritten
---

Constants have no outputs.json; their shape is simply their literal JSON value.
An integer index requires an array of sufficient length, a label index requires
an object with that key, and any index into a scalar fires this rule. A
constant whose value is itself a reference is followed first.
