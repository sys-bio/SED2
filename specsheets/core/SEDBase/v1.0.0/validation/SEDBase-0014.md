---
id: SEDBase-0014
rule: "An integer or range index into a dimension whose size is sourced as runtime and documents a min should warn when the index requires more entries than min guarantees."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' uses index {subvalue}, which might not exist - this dimension is only guaranteed to have at least {min} entries at runtime."
severity: warning
status: active
check: handwritten
---

Only fires when the target dimension's outputs.json size entry has
`source: "runtime"` and carries a `min`. A bare index `n` needs `min > n`;
a range `[a:b]` needs `min >= b` - both end-exclusive, per the Python-style
range convention (see Grammar). This is a warning, not an error: the index
might still be valid once the simulation actually runs, since `min` is a
guarantee, not the true count. Distinct from SEDBase-0011, which fires as
an error against a dimension whose size is statically known for certain.
