---
id: SEDBase-0009
rule: "A reference must not apply more bracket indices than its target has dimensions."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' applies {count} indices, but its target has only {expected-count} dimension(s)."
severity: error
status: active
---

Only fires when the target's dimension count is static in outputs.json (a
fixed "dimensions" array, or one whose count is computable from the target's
own literal fields). A "runtime" or "input-file" dimension count never fires
this rule. {count} is the number of indices used; {expected-count} is the
number of dimensions available.
