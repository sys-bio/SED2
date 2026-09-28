---
id: Types-0002
rule: Every function called in a math expression must be defined in the predefined-functions registry.
message: "The math in attribute '{attr}' of {class} '{id}' calls unknown function '{function}'."
severity: error
status: active
check: handwritten
---

Same rule as specsheets/core/Types/v1.0.0/validation/Types-0002.md; repeated here so the
generator enables the math-grammar checks for this tree. Applies only to a
literal string value (see Types-0001).
