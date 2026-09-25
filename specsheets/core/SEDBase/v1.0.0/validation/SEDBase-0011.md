---
id: SEDBase-0011
rule: "An integer or range index in a reference must fall within the size of the dimension it indexes."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' uses index {subvalue}, outside the dimension's valid range {min}..{max}."
severity: error
status: active
---

Only fires when that dimension's size is "static" and computable. Negative
indices count from the end (Python-style), so for size n the legal integer
indices are -n..n-1. For a range [a:b], both ends must be within -n..n, and
the range must select at least one element.
