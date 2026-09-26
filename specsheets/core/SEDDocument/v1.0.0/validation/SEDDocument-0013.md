---
id: SEDDocument-0013
rule: "A constant may only reference constants that appear before it in the constants dictionary."
message: "Constant '{attr}' references '{value}', which is not an earlier constant."
severity: error
status: active
check: handwritten
---

constants is described as coming before tasks, so a constant referencing a
task would break file-order execution. Constants may only reference earlier
constants, the same chronological principle AbstractTask-0003 applies to
tasks.
