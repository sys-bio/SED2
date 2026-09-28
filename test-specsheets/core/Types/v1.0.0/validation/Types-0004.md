---
id: Types-0004
rule: Every bare identifier in a math expression must be a predefined constant.
message: "The math in attribute '{attr}' of {class} '{id}' uses '{value}', which is not a predefined constant; use a #reference for document values."
severity: error
status: active
check: handwritten
---

Same rule as specsheets/core/Types/v1.0.0/validation/Types-0004.md; repeated here so the
generator enables the math-grammar checks for this tree. Applies only to a
literal string value (see Types-0001).
