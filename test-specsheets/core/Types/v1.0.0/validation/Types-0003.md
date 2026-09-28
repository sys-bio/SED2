---
id: Types-0003
rule: Every function called in a math expression must be given a number of arguments its registry entry allows.
message: "The math in attribute '{attr}' of {class} '{id}' calls '{function}' with {count} arguments; it accepts {expected-count}."
severity: error
status: active
check: handwritten
---

Same rule as specsheets/core/Types/v1.0.0/validation/Types-0003.md; repeated here so the
generator enables the math-grammar checks for this tree. Applies only to a
literal string value (see Types-0001).
