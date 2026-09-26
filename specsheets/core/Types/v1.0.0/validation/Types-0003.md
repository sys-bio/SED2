---
id: Types-0003
rule: "Every function called in a math expression must be given a number of arguments its registry entry allows."
message: "The math in attribute '{attr}' of {class} '{id}' calls '{function}' with {count} arguments; it accepts {expected-count}."
severity: error
status: active
check: handwritten
---

Arity comes from the function's registry entry, including the distrib
functions' alternative argument counts (e.g. normal takes 2 or 4).
