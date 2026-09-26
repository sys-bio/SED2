---
id: Types-0004
rule: "Every bare identifier in a math expression must be a predefined constant."
message: "The math in attribute '{attr}' of {class} '{id}' uses '{value}', which is not a predefined constant; use a #reference for document values."
severity: error
status: active
check: handwritten
---

SED2 math has no free variables: anything that is not a number, a predefined
constant (pi, exponentiale, true, false, notanumber, infinity), or a function
name must be written as a #reference. This catches the common mistake of
writing 'S1' instead of "#tasks:sim1['S1']".
