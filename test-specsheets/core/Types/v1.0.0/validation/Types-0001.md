---
id: Types-0001
rule: A math expression must be a well-formed expression under the SED2 infix grammar.
message: "The math in attribute '{attr}' of {class} '{id}' could not be parsed: '{expr}'. {parse-message}"
severity: error
status: active
check: handwritten
---

Same rule as specsheets/core/Types/v1.0.0/validation/Types-0001.md; repeated here so the
generator enables the math-grammar checks for this tree. Applies only to a
literal string value (see Types-0001).
